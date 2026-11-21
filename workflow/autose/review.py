"""Review job: the independent reviewer (ADR-008).

Runs in its own job with `contents: read`. It sees only the issue, the PR
diff and the repository at the PR head. It never sees the spec, the design,
the test report, or any agent's transcript.
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

from . import config, gh, llm
from .agent import AgentStopped, run_agent, submit_decl
from .orchestrator import issue_block, prompt
from .tools import Toolset

SUBMIT = submit_decl(
    "Submit your review.",
    {
        "verdict": {"type": "string", "enum": ["approve", "request_changes"]},
        "kind": {"type": "string", "enum": ["approach", "code", "none"]},
        "summary": {"type": "string"},
        "requirements": {"type": "array", "items": {"type": "object", "properties": {
            "requirement": {"type": "string"},
            "status": {"type": "string", "enum": ["met", "not_met", "cannot_tell"]},
            "evidence": {"type": "string"}}, "required": ["requirement", "status", "evidence"]}},
        "findings": {"type": "array", "items": {"type": "object", "properties": {
            "severity": {"type": "string", "enum": ["blocker", "major", "minor", "nit"]},
            "file": {"type": "string"}, "line": {"type": "integer"},
            "command": {"type": "string"},
            "description": {"type": "string"}, "evidence": {"type": "string"}},
            "required": ["severity", "description", "evidence"]}},
    },
    ["verdict", "kind", "summary", "requirements", "findings"])


def diff_files(diff):
    return set(re.findall(r"^\+\+\+ b/(.+)$", diff, re.M))


def filter_findings(findings, files, commands_run):
    """Code drops findings whose evidence does not hold (ADR-007, ADR-008)."""
    kept, dropped = [], []
    for f in findings:
        ok_file = f.get("file") and f["file"] in files
        ok_cmd = f.get("command") and any(f["command"].strip() in c for c in commands_run)
        (kept if (ok_file or ok_cmd) and (f.get("evidence") or "").strip() else dropped).append(f)
    return kept, dropped


def validate_factory(files, toolset_runs):
    def validate(a):
        reqs = a.get("requirements") or []
        if not reqs:
            return "list at least one requirement from the issue, with status and evidence"
        kept, _ = filter_findings(a.get("findings") or [], files, toolset_runs)
        serious = [f for f in kept if f["severity"] in ("blocker", "major")]
        not_met = [r for r in reqs if r.get("status") != "met"]
        if a.get("verdict") == "approve" and (not_met or serious):
            return ("you approved, but you marked requirements not met or reported blocker/major findings; "
                    "either request changes or correct the entries")
        if a.get("verdict") == "request_changes":
            if not (not_met or [f for f in kept if f["severity"] != "nit"]):
                return ("you requested changes but no requirement is not met and no non-nit finding has valid "
                        "evidence (a file in the diff, or a command you ran). Give evidence or approve.")
            if a.get("kind") not in ("approach", "code"):
                return "kind must be `approach` or `code` when requesting changes"
        return None
    return validate


class RecordingToolset(Toolset):
    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self.commands = []

    def t_run(self, command):
        self.commands.append(command)
        return super().t_run(command)


def render(r, model, rnd, dropped):
    lines = [f"## autose review (round {rnd})", "",
             f"**Verdict: {r['verdict'].replace('_', ' ')}**" + (f" (kind: `{r['kind']}`)" if r['verdict'] != 'approve' else ""),
             "", r.get("summary", ""), "", "### What the issue asks for", "",
             "| requirement | status | evidence |", "| --- | --- | --- |"]
    for q in r["requirements"]:
        lines.append(f"| {q['requirement']} | {q['status']} | {q.get('evidence', '').replace(chr(10), ' ')[:400]} |")
    lines += ["", "### Findings", ""]
    for f in r["findings"] or []:
        where = f"`{f.get('file')}:{f.get('line', '')}`" if f.get("file") else f"`{f.get('command', '')}`"
        lines.append(f"- **{f['severity']}** {where}: {f['description']}\n  - evidence: {f['evidence'][:600]}")
    if not r["findings"]:
        lines.append("None.")
    if dropped:
        lines += ["", f"<details><summary>{len(dropped)} finding(s) dropped by code for missing evidence</summary>",
                  "", "\n".join(f"- {f.get('severity')}: {f.get('description')}" for f in dropped), "</details>"]
    lines += ["", "---", f"Reviewer model `{model}`, separate job, read-only. "
              "It saw only the issue, the diff and the repository at the PR head. A person decides whether to merge."]
    return "\n".join(lines)


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("--pr", required=True)
    p.add_argument("--issue", required=True)
    p.add_argument("--round", default="1")
    p.add_argument("--work", required=True)
    p.add_argument("--out", required=True)
    a = p.parse_args(argv)
    token = os.environ.pop("GITHUB_TOKEN", None)
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    work = Path(a.work).resolve()
    for d in config.ASSIGNMENT_PATHS:      # ADR-003: no assignment material
        t = work / d
        if t.is_dir():
            import shutil
            shutil.rmtree(t)
        elif t.exists():
            t.unlink()

    issue = gh.issue(int(a.issue), token)
    diff = gh.gh(["pr", "diff", a.pr, "--repo", config.REPO], token)
    files = diff_files(diff)
    usage = llm.Usage()
    ts = RecordingToolset(work, "reviewer", SUBMIT, can_run=True)
    user = (issue_block(issue) + f"\n\n# Pull request #{a.pr} diff\n\n```diff\n{diff[:60000]}\n```")
    try:
        r = run_agent("reviewer", config.REVIEWER_MODEL, prompt("review"), user, ts, usage,
                      out / "logs" / "reviewer.jsonl", validate=validate_factory(files, ts.commands))
        r["findings"], dropped = filter_findings(r.get("findings") or [], files, ts.commands)
        note = ""
    except AgentStopped as e:
        # ADR-007: an invalid review after one retry does not block the human.
        r = {"verdict": "approve", "kind": "none", "summary": f"The reviewer could not produce a valid review: {e}. "
             "No automated changes are requested; the human reviewer should look closely.",
             "requirements": [], "findings": []}
        dropped, note = [], "invalid"
    r.update({"round": a.round, "pr": int(a.pr), "model": config.REVIEWER_MODEL,
              "tokens": usage.to_dict(), "note": note, "dropped": dropped})
    (out / "review.json").write_text(json.dumps(r, indent=2))
    body = render(r, config.REVIEWER_MODEL, a.round, dropped)
    (out / "review.md").write_text(body)
    if token:
        flag = "--approve" if r["verdict"] == "approve" else "--request-changes"
        gh.gh(["pr", "review", a.pr, "--repo", config.REPO, flag, "--body-file", str(out / "review.md")], token)
    go = os.environ.get("GITHUB_OUTPUT")
    if go:
        with open(go, "a") as f:
            f.write(f"verdict={r['verdict']}\nkind={r['kind']}\n")
    print(json.dumps({"verdict": r["verdict"], "kind": r["kind"], "tokens": usage.total}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
