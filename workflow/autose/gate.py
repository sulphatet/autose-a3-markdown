"""Gate job: decide whether this event may start a run (ADR-010).

Reads the event from GITHUB_EVENT_PATH (a file), so issue and comment text
never passes through a shell or a `${{ }}` expression (ADR-009).
"""

import json
import os
import re
import sys

from . import config, gh

TRUSTED_ASSOC = {"OWNER", "MEMBER", "COLLABORATOR"}
TRUSTED_ROLES = {"admin", "maintain", "write", "triage"}


def role(login, token):
    d = gh.api(f"repos/{config.REPO}/collaborators/{login}/permission", token, check=False)
    return (d or {}).get("role_name") or (d or {}).get("permission") or "none"


def decide(event_name, ev, token):
    """Return (run, mode, issue, round, resume_from, pr, reason).

    For review mode, the resume_from slot carries the reviewer variant."""
    no = lambda why: (False, "", "", "", "", "", why)  # noqa: E731
    if event_name == "issues":
        if ev.get("action") != "labeled" or (ev.get("label") or {}).get("name") != config.LABEL:
            return no("not the autose label")
        if "pull_request" in ev["issue"]:
            return no("label on a pull request")
        who = ev["sender"]["login"]
        r = role(who, token)
        if r not in TRUSTED_ROLES:
            return no(f"{who} has role {r}")
        return True, "full", str(ev["issue"]["number"]), "1", "S1", "", f"label added by {who} ({r})"

    if event_name == "issue_comment":
        c = ev["comment"]
        if not (c.get("body") or "").strip().startswith("/autose"):
            return no("comment is not a command")
        if c["user"].get("type") == "Bot" or c["user"]["login"].endswith("[bot]"):
            return no("comment by a bot")
        if c.get("author_association") not in TRUSTED_ASSOC:
            return no(f"author association {c.get('author_association')}")
        num = ev["issue"]["number"]
        if "pull_request" in ev["issue"]:
            pr = gh.api(f"repos/{config.REPO}/pulls/{num}", token)
            ref = pr["head"]["ref"]
            m = (re.fullmatch(re.escape(config.BRANCH_PREFIX) + r"(\d+)", ref)
                 or re.fullmatch(re.escape(config.SEED_PREFIX) + r"(\d+)-[\w-]+", ref))
            if not m:
                return no("pull request was not opened by autose and is not a seeded PR")
            v = re.search(r"variant=([\w-]+)", c["body"])
            variant = v.group(1) if v else "default"
            if variant not in config.REVIEWER_VARIANTS:
                return no(f"unknown reviewer variant {variant}")
            return True, "review", m.group(1), "manual", variant, str(num), f"review-only ({variant}) requested"
        return True, "full", str(num), "1", "S1", "", "run requested by comment"

    if event_name == "workflow_dispatch":
        inp = ev.get("inputs") or {}
        who = ev["sender"]["login"]
        r = role(who, token)
        if r not in TRUSTED_ROLES and who != "github-actions[bot]":
            return no(f"{who} has role {r}")
        rnd = str(inp.get("round") or "1")
        if not rnd.isdigit() or int(rnd) > config.MAX_REVIEW_ROUNDS:
            return no(f"round {rnd} is beyond the review budget")
        rf = inp.get("resume_from") or "S1"
        if rf not in ("S1", "S2", "S3"):
            return no(f"bad resume_from {rf}")
        return True, "full", str(int(inp["issue"])), rnd, rf, "", f"dispatched by {who}"

    return no(f"event {event_name} not handled")


def main():
    ev = json.load(open(os.environ["GITHUB_EVENT_PATH"]))
    result = decide(os.environ["GITHUB_EVENT_NAME"], ev, os.environ.get("GITHUB_TOKEN"))
    keys = ["run", "mode", "issue", "round", "resume_from", "pr", "reason"]
    out = dict(zip(keys, result))
    out["run"] = "true" if out["run"] else "false"
    print(json.dumps(out))
    with open(os.environ["GITHUB_OUTPUT"], "a") as f:
        for k, v in out.items():
            f.write(f"{k}={str(v).replace(chr(10), ' ')}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
