"""Role-scoped tools for agents (ADR-005).

Agents never get a shell, git, network or GitHub. Paths are jailed to the
working copy, writes are limited per role, and commands are allow-listed and
run with a scrubbed environment.
"""

import os
import re
import shlex
import subprocess
from pathlib import Path

from . import config

SAFE_ARG = re.compile(r"^[\w./:=,-]+$")
TEXT_SUFFIXES = {".py", ".md", ".txt", ".toml", ".cfg", ".ini", ".yml", ".yaml", ".html", ".json", ".in", ""}


def _allowed_command(argv):
    """Return None if allowed, else the reason it is refused."""
    if not argv or argv[0] not in ("python", "python3"):
        return "only `python -m unittest ...`, `python -m pip install -e .` and `python -m flake8 ...` are allowed"
    rest = argv[1:]
    if rest[:2] == ["-m", "unittest"]:
        extra = rest[2:]
    elif rest == ["-m", "pip", "install", "-e", "."]:
        extra = []
    elif rest[:2] == ["-m", "flake8"]:
        extra = rest[2:]
    else:
        return "command not on the allow-list"
    bad = [a for a in extra if not SAFE_ARG.match(a)]
    if bad:
        return f"argument(s) not allowed: {bad}"
    return None


def scrubbed_env():
    env = {k: os.environ[k] for k in ("PATH", "HOME", "LANG", "LC_ALL") if k in os.environ}
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return env


def run_command(argv, cwd, timeout=config.COMMAND_TIMEOUT):
    """Run an argv list with a scrubbed environment. Returns (exit_code, output)."""
    try:
        p = subprocess.run(argv, cwd=cwd, env=scrubbed_env(), capture_output=True,
                           text=True, timeout=timeout)
        return p.returncode, (p.stdout + p.stderr)
    except subprocess.TimeoutExpired as e:
        out = (e.stdout or "") + (e.stderr or "") if isinstance(e.stdout, str) else ""
        return 124, out + f"\n[killed after {timeout}s]"


def _tail(text, limit=config.TOOL_OUTPUT_LIMIT):
    return text if len(text) <= limit else f"[... {len(text) - limit} characters cut ...]\n" + text[-limit:]


def _decl(name, description, props, required):
    return {"name": name, "description": description,
            "parameters": {"type": "object", "properties": props, "required": required}}


READ_DECLS = [
    _decl("list_dir", "List files and folders in a directory of the repository.",
          {"path": {"type": "string", "description": "Directory relative to the repository root, e.g. 'markdown/extensions'."}},
          ["path"]),
    _decl("read_file", "Read a text file, with line numbers. Use start_line/end_line for long files.",
          {"path": {"type": "string"}, "start_line": {"type": "integer"}, "end_line": {"type": "integer"}},
          ["path"]),
    _decl("search", "Search files for a regular expression. Returns up to 80 matching lines as path:line: text.",
          {"pattern": {"type": "string"}, "path": {"type": "string", "description": "Directory or file to search, default the whole repository."}},
          ["pattern"]),
]
WRITE_DECLS = [
    _decl("write_file", "Create or overwrite a whole file.",
          {"path": {"type": "string"}, "content": {"type": "string"}}, ["path", "content"]),
    _decl("replace_in_file", "Replace one exact, unique piece of text in a file. Include enough surrounding lines to make `old` unique.",
          {"path": {"type": "string"}, "old": {"type": "string"}, "new": {"type": "string"}}, ["path", "old", "new"]),
]
RUN_DECL = _decl(
    "run", "Run an allowed command in the repository root: `python -m unittest <args>`, "
    "`python -m pip install -e .` or `python -m flake8 <paths>`. No shell features.",
    {"command": {"type": "string"}}, ["command"])


class Toolset:
    def __init__(self, root, role, submit_decl, can_read=True, can_run=False):
        self.root = Path(root).resolve()
        self.role = role
        self.write_prefixes = config.WRITE_PATHS.get(role, [])
        self.decls = (list(READ_DECLS) if can_read else [])
        if self.write_prefixes:
            self.decls += WRITE_DECLS
        if can_run:
            self.decls.append(RUN_DECL)
        self.decls.append(submit_decl)
        self.names = {d["name"] for d in self.decls}
        self.files_written = set()

    # path jail
    def _path(self, rel, write=False):
        rel = (rel or ".").strip()
        p = (self.root / rel).resolve()
        if p != self.root and self.root not in p.parents:
            raise PermissionError(f"{rel} is outside the repository")
        relp = p.relative_to(self.root).as_posix() if p != self.root else ""
        if relp.split("/")[0] in (".git", ".github"):
            raise PermissionError(f"{rel} is not accessible")
        if write and not any(relp == w or relp.startswith(w) for w in self.write_prefixes):
            raise PermissionError(f"role {self.role} may only write under {self.write_prefixes}")
        return p, relp

    def call(self, name, args):
        if name not in self.names:
            return f"ERROR: tool {name} is not available to you"
        try:
            return getattr(self, "t_" + name)(**args)
        except TypeError as e:
            return f"ERROR: bad arguments: {e}"
        except (PermissionError, FileNotFoundError, IsADirectoryError, UnicodeDecodeError, ValueError) as e:
            return f"ERROR: {e}"

    def t_list_dir(self, path="."):
        p, _ = self._path(path)
        if not p.is_dir():
            return f"ERROR: {path} is not a directory"
        items = sorted(p.iterdir())
        return "\n".join((i.name + "/" if i.is_dir() else i.name) for i in items
                         if i.name not in (".git", ".github", "__pycache__")) or "(empty)"

    def t_read_file(self, path, start_line=1, end_line=None):
        p, _ = self._path(path)
        lines = p.read_text().splitlines()
        start = max(1, int(start_line or 1))
        end = min(len(lines), int(end_line or start + 399))
        body = "\n".join(f"{i}: {lines[i - 1]}" for i in range(start, end + 1))
        more = f"\n[file has {len(lines)} lines; showing {start}-{end}]" if end < len(lines) or start > 1 else ""
        return _tail(body + more)

    def t_search(self, pattern, path="."):
        rx = re.compile(pattern)
        base, _ = self._path(path)
        files = [base] if base.is_file() else sorted(base.rglob("*"))
        hits = []
        for f in files:
            if not f.is_file() or f.suffix not in TEXT_SUFFIXES:
                continue
            rel = f.relative_to(self.root).as_posix()
            if rel.split("/")[0] in (".git", ".github") or "egg-info" in rel:
                continue
            try:
                for n, line in enumerate(f.read_text().splitlines(), 1):
                    if rx.search(line):
                        hits.append(f"{rel}:{n}: {line.strip()[:200]}")
                        if len(hits) >= 80:
                            return "\n".join(hits) + "\n[stopped at 80 matches]"
            except UnicodeDecodeError:
                continue
        return "\n".join(hits) or "no matches"

    def t_write_file(self, path, content):
        p, relp = self._path(path, write=True)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content)
        self.files_written.add(relp)
        return f"wrote {relp} ({len(content.splitlines())} lines)"

    def t_replace_in_file(self, path, old, new):
        p, relp = self._path(path, write=True)
        text = p.read_text()
        n = text.count(old)
        if n != 1:
            return f"ERROR: `old` occurs {n} times in {relp}; it must occur exactly once"
        p.write_text(text.replace(old, new))
        self.files_written.add(relp)
        return f"replaced text in {relp}"

    def t_run(self, command):
        try:
            argv = shlex.split(command)
        except ValueError as e:
            return f"ERROR: {e}"
        why = _allowed_command(argv)
        if why:
            return f"ERROR: {why}"
        code, out = run_command(argv, self.root)
        return _tail(f"exit code {code}\n{out}")
