"""Deterministic stage checks (ADR-007). Code, not an agent, decides pass or fail.

Each check returns a CheckResult. Its `reasons` are written into the stage's
artifact so a reader can see exactly why a stage passed or failed.
"""

import ast
import re
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

from . import config
from .tools import run_command

WEASEL = ["fast", "user-friendly", "secure", "robust", "scalable", "seamless", "etc.",
          "and/or", "as appropriate", "enterprise-grade"]
REQ_ID = r"(?:FR-\d+|NFR-[A-Z]+-\d+)"
AC_ID = re.compile(rf"AC-{REQ_ID}-\d+")


@dataclass
class CheckResult:
    ok: bool
    reasons: list = field(default_factory=list)
    data: dict = field(default_factory=dict)
    format_only: bool = False   # the problem is the artifact's format, not its content

    def md(self):
        head = "PASS" if self.ok else "FAIL"
        return f"**Check: {head}**\n\n" + "\n".join(f"- {r}" for r in self.reasons) + "\n"


def ac_test_name(ac_id):
    return "test_" + ac_id.replace("-", "_")


# ---------------------------------------------------------------- stage 1
def check_spec(srs, validation):
    """Lenient stage 1 check (ADR-015).

    The A1 skill's verdict is recorded but does not decide. The stage passes
    when the spec has at least one testable acceptance criterion. Open
    questions become assumptions that the reviewer and the human can see.
    """
    reasons = []
    verdict = re.search(r"Verdict[^\n]*\n*[^\n]*?(READY FOR IMPLEMENTATION|PARTIALLY READY|NOT READY|ESCALATED TO HUMAN)",
                        validation, re.I)
    v = verdict.group(1).upper() if verdict else None
    if not v:
        return CheckResult(False, ["VALIDATION.md has no recognisable verdict"], {"verdict": None, "acs": {}},
                           format_only=True)
    reasons.append(f"A1 skill verdict is `{v}` (recorded, not blocking)")

    ready = []
    for line in srs.splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if cells and re.fullmatch(REQ_ID, cells[0].strip("*` ")) and any(c.strip("*` ") == "Ready" for c in cells):
            ready.append(cells[0].strip("*` "))

    acs = {}
    for line in srs.splitlines():
        for m in AC_ID.finditer(line):
            acs.setdefault(m.group(0), line[m.end():].strip(" :-*|"))
    mine = {a: t for a, t in acs.items() if any(a.startswith(f"AC-{r}-") for r in ready)} or acs
    if not ready and acs:
        reasons.append("no requirement is marked `Ready`; using all acceptance criteria, open questions "
                       "are treated as assumptions")

    testable = {}
    for a, t in mine.items():
        clean = re.sub(r"`?<TBD[^>]*>`?", "", t, flags=re.I).strip()
        low = clean.lower()
        then = low.split("then", 1)[1] if "then" in low else ""
        concrete = re.search(r"`[^`]+`|\"[^\"]+\"|'[^']+'|\d", then)
        if not (all(w in low for w in ("given", "when")) and concrete):
            reasons.append(f"{a} skipped: its expected result names nothing concrete to check")
            continue
        testable[a] = clean
    ok = bool(testable)
    reasons.append(f"{len(testable)} testable acceptance criteria: " + ", ".join(testable) if ok
                   else "no testable acceptance criterion: the issue gives nothing to implement against")
    return CheckResult(ok, reasons, {"verdict": v, "ready": ready, "acs": testable})


# ---------------------------------------------------------------- stage 2
def _symbols(path):
    try:
        tree = ast.parse(Path(path).read_text())
    except (SyntaxError, UnicodeDecodeError):
        return set()
    names = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            names.add(node.name)
        if isinstance(node, ast.ClassDef):
            for sub in node.body:
                if isinstance(sub, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    names.add(f"{node.name}.{sub.name}")
        if isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name):
                    names.add(t.id)
    return names


def parse_change_list(design):
    rows, in_table, header = [], False, None
    for line in design.splitlines():
        s = line.strip()
        if s.startswith("|"):
            cells = [c.strip().strip("`* ") for c in s.strip("|").split("|")]
            low = [c.lower() for c in cells]
            if header is None and "file" in low and "symbol" in low:
                header, in_table = low, True
                continue
            if in_table and set(s.replace("|", "").strip()) <= set("-: "):
                continue
            if in_table and len(cells) >= len(header):
                rows.append(dict(zip(header, cells)))
        elif in_table and s:
            in_table = False if rows else in_table
    return rows


def check_design(design, root, ac_ids):
    reasons = []
    rows = parse_change_list(design)
    if not rows:
        return CheckResult(False, ["design.md has no Change list table with `file` and `symbol` columns"],
                           format_only=True)
    covered, ok = set(), True
    for r in rows:
        f, sym, change = r.get("file", ""), r.get("symbol", ""), r.get("change", "").lower()
        new_file = "new file" in change or f.endswith("(new)")
        f = f.replace("(new)", "").strip()
        p = Path(root) / f
        if not new_file and not p.is_file():
            ok = False
            reasons.append(f"`{f}` does not exist (mark it `new file` in the change column if it is new)")
            continue
        new_sym = "(new)" in sym or change.startswith("add") or new_file
        sym_clean = sym.replace("(new)", "").replace("()", "").strip()
        if not sym_clean:
            ok = False
            reasons.append(f"row for `{f}` names no symbol")
        elif not new_sym and f.endswith(".py") and sym_clean not in _symbols(p):
            ok = False
            reasons.append(f"`{sym_clean}` is not a function, class, method or module name in `{f}`")
        else:
            reasons.append(f"`{f}` :: `{sym_clean}`" + (" (new)" if new_sym else " found"))
        covered |= set(AC_ID.findall(r.get("acs covered", "") + " " + r.get("acs", "")))
    missing = [a for a in ac_ids if a not in covered]
    if missing:
        ok = False
        reasons.append(f"acceptance criteria not covered by any change: {missing}")
    return CheckResult(ok, reasons, {"rows": rows})


# ---------------------------------------------------------------- stage 3
def changed_files(root, base_sha):
    subprocess.run(["git", "add", "-A", "-N"], cwd=root, check=True, capture_output=True)
    out = subprocess.run(["git", "diff", "--name-only", base_sha], cwd=root, check=True,
                         capture_output=True, text=True).stdout
    return [f for f in out.splitlines() if f]


def flake8_errors(root, target="markdown"):
    """flake8 errors keyed by (path, code, source line), so line shifts do not matter (ADR-013)."""
    _, out = run_command(["python", "-m", "flake8", target], root)
    errs = {}
    for line in out.splitlines():
        m = re.match(r"^(.+?):(\d+):(\d+): (\w+) (.*)$", line)
        if not m:
            continue
        path, ln = m.group(1), int(m.group(2))
        try:
            src = (Path(root) / path).read_text().splitlines()[ln - 1].strip()
        except (OSError, IndexError):
            src = ""
        key = (path, m.group(4), src)
        n = sum(1 for k in errs if k[:3] == key)
        errs[key + (n,)] = line
    return errs


def check_build(root, base_sha, design_files, lint_baseline=None):
    reasons = []
    files = changed_files(root, base_sha)
    src = [f for f in files if f.startswith("markdown/")]
    if not src:
        return CheckResult(False, ["no change under `markdown/`"])
    bad = [f for f in files if any(f == p.rstrip("/") or f.startswith(p) for p in config.FORBIDDEN_DIFF_PATHS)]
    if bad:
        return CheckResult(False, [f"diff touches forbidden paths: {bad}"])
    reasons.append(f"changed files: {files}")
    extra = [f for f in src if f not in design_files]
    if extra:
        reasons.append(f"deviation (recorded, not a failure): files changed outside the design: {extra}")
    if "docs/changelog.md" not in files:
        reasons.append("no `docs/changelog.md` entry; upstream CI (changelog-enforcer) will fail")
        return CheckResult(False, reasons)
    steps = [
        (["python", "-m", "pip", "install", "-q", "-e", "."], "pip install -e ."),
        (["python", "-c", "import markdown; markdown.markdown('# x', extensions=['extra', 'toc'])"], "import + smoke call"),
    ]
    for argv, label in steps:
        code, out = run_command(argv, root)
        if code != 0:
            reasons.append(f"`{label}` failed (exit {code}):\n\n```\n{out[-3000:]}\n```")
            return CheckResult(False, reasons, {"files": files})
        reasons.append(f"`{label}` passed")
    # ADR-013: only lint errors the change introduces count; pre-existing ones are reported, not failed.
    now = flake8_errors(root)
    base = lint_baseline or {}
    new = [v for k, v in now.items() if k not in base]
    if new:
        reasons.append("`flake8 markdown` reports errors introduced by this change:\n\n```\n"
                       + "\n".join(new[:40]) + "\n```")
        return CheckResult(False, reasons, {"files": files})
    reasons.append(f"`flake8 markdown`: no new errors ({len(base)} pre-existing on the base commit ignored)")
    return CheckResult(True, reasons, {"files": files})


# ---------------------------------------------------------------- stage 4
def test_methods(path):
    try:
        tree = ast.parse(Path(path).read_text())
    except SyntaxError as e:
        return None, str(e)
    names = [n.name for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name.startswith("test")]
    return names, None


def check_test_file(root, test_file, ac_ids):
    """Structure of the tester's file (ADR-011: failures here go back to the tester)."""
    p = Path(root) / test_file
    if not p.is_file():
        return CheckResult(False, [f"test file `{test_file}` was not written"], format_only=True)
    names, err = test_methods(p)
    if err:
        return CheckResult(False, [f"test file has a syntax error: {err}"])
    reasons = [f"test methods: {names}"]
    missing = [a for a in ac_ids if not any(ac_test_name(a) in n for n in names)]
    if missing:
        reasons.append("no test named after: " + ", ".join(f"{a} (`{ac_test_name(a)}`)" for a in missing))
    code, out = run_command(["python", "-m", "flake8", test_file], root)
    if code != 0:
        reasons.append(f"flake8 on the test file failed (upstream CI lints tests):\n\n```\n{out[-2000:]}\n```")
    return CheckResult(not missing and code == 0, reasons, {"names": names})


def _module(test_file):
    return test_file[:-3].replace("/", ".")


def run_unittest(root, target):
    return run_command(["python", "-m", "unittest", "-v", target], root)


def parse_unittest(out):
    """Per-test result from `unittest -v` output.

    Uses the `FAIL: name (...)` / `ERROR: name (...)` summary lines, which have a fixed
    format. The verbose progress lines put a test's docstring between its name and
    its result, so they cannot be relied on for the result (found in run 44944052837).
    """
    res = {}
    for m in re.finditer(r"^(test\w+) \([\w.]+\)", out, re.M):
        res.setdefault(m.group(1), "ok")
    for m in re.finditer(r"^(test\w+) \([\w.]+\)(?:\n(?!test)[^\n]*)?? \.\.\. skipped", out, re.M):
        res[m.group(1)] = "skipped"
    for m in re.finditer(r"^(FAIL|ERROR): (test\w+) \(", out, re.M):
        res[m.group(2)] = m.group(1)
    return res


def check_fail_to_pass(base_root, test_file, ac_ids):
    """New tests must fail on the base commit: otherwise they do not test the change."""
    code, out = run_unittest(base_root, _module(test_file))
    per = parse_unittest(out)
    if code == 0:
        return CheckResult(False, ["every new test passes on the base commit, so none of them tests the change"],
                           {"base": per})
    failing = [n for n, r in per.items() if r in ("FAIL", "ERROR")]
    if not failing and ("ImportError" in out or "ModuleNotFoundError" in out or "AttributeError" in out):
        failing = ["(test module fails to import on base)"]
    reasons = [f"{len(failing)} new test(s) fail on base as expected: {failing}"]
    passing = [n for n, r in per.items() if r == "ok"]
    if passing:
        reasons.append(f"pass on base too (regression tests, recorded): {passing}")
    return CheckResult(bool(failing), reasons, {"base": per})


def check_suite(root, test_file):
    reasons = []
    code, out = run_unittest(root, _module(test_file))
    per = parse_unittest(out)
    if code != 0:
        return CheckResult(False, [f"new tests fail on the branch:\n\n```\n{out[-4000:]}\n```"], {"new": per, "log": out})
    reasons.append(f"new tests pass on the branch: {list(per)}")
    code, out = run_command(["python", "-m", "unittest", "discover", "tests"], root)
    summary = out.strip().splitlines()[-3:] if out.strip() else []
    if code != 0:
        return CheckResult(False, reasons + [f"full suite fails:\n\n```\n{out[-4000:]}\n```"], {"new": per, "log": out})
    reasons.append("full suite passes: " + " ".join(summary))
    return CheckResult(True, reasons, {"new": per})
