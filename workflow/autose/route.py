"""Route job: after review, record the result and decide the next round (ADR-002).

The reviewer has no write access, so this small job (no LLM) saves the review
to the state branch and, if changes were requested and rounds remain, starts
the next round with workflow_dispatch.
"""

import argparse
import json
import os
import shutil
import sys
from pathlib import Path

from . import config, gh
from .state import State


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("--issue", required=True)
    p.add_argument("--round", required=True)
    p.add_argument("--review-dir", required=True)
    p.add_argument("--state", required=True)
    p.add_argument("--variant", default="default")
    a = p.parse_args(argv)
    token = os.environ.pop("GITHUB_TOKEN", None)
    n = int(a.issue)
    review = json.loads((Path(a.review_dir) / "review.json").read_text())
    st = State(a.state, n, config.suffix(a.variant))
    manual = not a.round.isdigit()
    tag = f"pr{review.get('pr')}-{review.get('variant', 'default')}-{os.environ.get('GITHUB_RUN_ID', 'local')}"
    rdir = st.issue_dir / (f"review-manual-{tag}" if manual else f"round-{a.round}")
    rdir.mkdir(parents=True, exist_ok=True)
    for f in ("review.json", "review.md"):
        shutil.copy2(Path(a.review_dir) / f, rdir / f)

    verdict, kind = review["verdict"], review.get("kind")
    if not manual:
        rnd = int(a.round)
        st.stage(rnd, "S6").update(status="passed" if verdict == "approve" else "changes_requested",
                                   verdict=verdict, kind=kind, model=review.get("model"))
        if verdict == "request_changes" and rnd < config.MAX_REVIEW_ROUNDS:
            resume = "S2" if kind == "approach" else "S3"
            gh.gh(["workflow", "run", "autose.yml", "--repo", config.REPO, "--ref", "main",
                   "-f", f"issue={n}", "-f", f"round={rnd + 1}", "-f", f"resume_from={resume}",
                   "-f", f"variant={a.variant or 'default'}"], token)
            msg = (f"Review round {rnd}: **changes requested** (`{kind}`). Starting round {rnd + 1} "
                   f"from stage {resume[1]} ({'Design' if resume == 'S2' else 'Implementation'}).")
        elif verdict == "request_changes":
            msg = (f"Review round {rnd}: **changes requested**, and the {config.MAX_REVIEW_ROUNDS} review rounds are "
                   "used up. The workflow ends here; a person decides whether to merge, fix or close.")
        else:
            msg = f"Review round {rnd}: **approved**. The workflow ends here; a person decides whether to merge."
    else:
        msg = (f"Review-only run on PR #{review.get('pr')} (reviewer `{review.get('model')}`, variant "
               f"`{review.get('variant')}`): **{verdict.replace('_', ' ')}**. No automatic round is started.")
    st.commit_push(f"issue {n} review {a.round}: {verdict}", token)
    if token:
        gh.comment(n, msg + f"\n\nReview: {gh.run_url()}", token)
    print(msg)
    return 0


if __name__ == "__main__":
    sys.exit(main())
