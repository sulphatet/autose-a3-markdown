"""GitHub access for orchestrator code only. Agents never call this (ADR-005).

Every call names the token it uses, so it is clear which identity acts.
"""

import base64
import json
import os
import subprocess

from . import config

MARKER = "<!-- autose-progress -->"


def gh(args, token, check=True, input=None):
    env = dict(os.environ, GH_PROMPT_DISABLED="1")
    if token:
        env["GH_TOKEN"] = token
    p = subprocess.run(["gh"] + args, env=env, capture_output=True, text=True, input=input)
    if check and p.returncode != 0:
        raise RuntimeError(f"gh {' '.join(args[:3])} failed: {p.stderr.strip()[:500]}")
    return p.stdout


def api(path, token, method="GET", fields=None, check=True):
    args = ["api", "-X", method, path]
    for k, v in (fields or {}).items():
        args += ["-f" if isinstance(v, str) else "-F", f"{k}={v}"]
    out = gh(args, token, check=check)
    return json.loads(out) if out.strip() else {}


def git_auth_env(token):
    """Credentials for one git process via environment (never written to .git/config)."""
    basic = base64.b64encode(f"x-access-token:{token}".encode()).decode()
    env = dict(os.environ)
    env.update({"GIT_CONFIG_COUNT": "1",
                "GIT_CONFIG_KEY_0": "http.https://github.com/.extraheader",
                "GIT_CONFIG_VALUE_0": f"AUTHORIZATION: basic {basic}",
                "GIT_TERMINAL_PROMPT": "0"})
    return env


def git(args, cwd, token=None, check=True):
    env = git_auth_env(token) if token else None
    p = subprocess.run(["git"] + args, cwd=cwd, env=env, capture_output=True, text=True)
    if check and p.returncode != 0:
        raise RuntimeError(f"git {' '.join(args[:2])} failed: {p.stderr.strip()[:500]}")
    return p.stdout.strip()


def issue(number, token):
    d = api(f"repos/{config.REPO}/issues/{number}", token)
    return {"number": number, "title": d["title"], "body": d.get("body") or "",
            "author": d["user"]["login"], "url": d["html_url"]}


def upsert_progress(number, body, token, key=""):
    """Keep one progress comment per issue (and per experiment variant) up to date (ADR-004)."""
    marker = MARKER if not key else f"<!-- autose-progress {key} -->"
    comments = api(f"repos/{config.REPO}/issues/{number}/comments?per_page=100", token)
    mine = [c for c in comments if (c.get("body") or "").startswith(marker + "\n")]
    text = marker + "\n" + body
    if mine:
        api(f"repos/{config.REPO}/issues/comments/{mine[-1]['id']}", token, "PATCH", {"body": text})
    else:
        api(f"repos/{config.REPO}/issues/{number}/comments", token, "POST", {"body": text})


def comment(number, body, token):
    api(f"repos/{config.REPO}/issues/{number}/comments", token, "POST", {"body": body})


def run_url():
    s, r, i = (os.environ.get(k) for k in ("GITHUB_SERVER_URL", "GITHUB_REPOSITORY", "GITHUB_RUN_ID"))
    return f"{s}/{r}/actions/runs/{i}" if s and r and i else "(local run)"
