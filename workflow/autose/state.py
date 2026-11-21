"""Run state on the `autose-state` branch, and deterministic resume (ADR-004).

Layout on the branch:
    runs/issue-<n>/state.json
    runs/issue-<n>/round-<r>/<artifacts>

A stage is reused on restart only if it passed and the hash of its inputs is
unchanged. The first stage that differs, and every stage after it, runs again.
"""

import hashlib
import json
import shutil
from pathlib import Path

from . import config
from .gh import git

STAGES = ["S1", "S2", "S3", "S4", "S5", "S6"]


def sha(*parts):
    h = hashlib.sha256()
    for p in parts:
        h.update((p if isinstance(p, bytes) else str(p).encode()))
        h.update(b"\x00")
    return h.hexdigest()


def file_sha(path):
    p = Path(path)
    return sha(p.read_bytes()) if p.is_file() else "missing"


class State:
    def __init__(self, state_dir, issue):
        self.dir = Path(state_dir)
        self.issue = issue
        self.issue_dir = self.dir / "runs" / f"issue-{issue}"
        self.path = self.issue_dir / "state.json"
        self.data = json.loads(self.path.read_text()) if self.path.is_file() else {
            "issue": issue, "base_sha": None, "rounds": {}, "tokens": {}}

    def round_dir(self, r):
        return self.issue_dir / f"round-{r}"

    def stage(self, r, s):
        return self.data["rounds"].setdefault(str(r), {}).setdefault(s, {"status": "pending", "attempts": 0})

    def reusable(self, r, s, input_hash):
        st = self.stage(r, s)
        return st.get("status") == "passed" and st.get("input_hash") == input_hash

    def invalidate_from(self, r, s):
        for later in STAGES[STAGES.index(s):]:
            st = self.stage(r, later)
            if st.get("status") == "passed":
                st["status"] = "pending"

    def save_artifacts(self, r, out_dir):
        """Copy the round's artifacts (not transcripts) into the state branch folder."""
        dest = self.round_dir(r)
        dest.mkdir(parents=True, exist_ok=True)
        for f in Path(out_dir).iterdir():
            if f.is_file():
                shutil.copy2(f, dest / f.name)

    def write(self):
        self.issue_dir.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(self.data, indent=2, sort_keys=True) + "\n")

    def commit_push(self, message, token):
        """Commit and push the state branch. Different issues use different folders,
        and runs for one issue are serialised by the concurrency group (ADR-010)."""
        self.write()
        if token is None:
            return
        git(["add", "-A"], self.dir)
        if not git(["status", "--porcelain"], self.dir):
            return
        git(["-c", "user.name=autose-bot", "-c", "user.email=autose-bot@users.noreply.github.com",
             "commit", "-q", "-m", message], self.dir)
        for _ in range(3):
            try:
                git(["push", "-q", "origin", f"HEAD:refs/heads/{config.STATE_BRANCH}"], self.dir, token)
                return
            except RuntimeError:
                git(["pull", "-q", "--rebase", "origin", config.STATE_BRANCH], self.dir, token, check=False)
        raise RuntimeError("could not push the state branch")
