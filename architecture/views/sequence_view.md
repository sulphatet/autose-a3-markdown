# Sequence view: a real run

[Run 44942584408](https://github.com/sulphatet/autose-a3-markdown/actions/runs/44942584408), issue #2 (`fenced_code` crashes with `linenums` when codehilite is off). Started by a maintainer's `/autose` comment after the first run (44941261187) had stopped at stage 3. Ended with the approved [PR #9](https://github.com/sulphatet/autose-a3-markdown/pull/9). Every step below appears in the run log.

```mermaid
sequenceDiagram
    autonumber
    actor M as Maintainer
    participant GH as GitHub (issue / PR / CI)
    participant G as gate job
    participant O as build job: orchestrator
    participant ST as autose-state branch
    participant SA as Spec / Design agents
    participant IA as Implementer agent
    participant TA as Tester agent
    participant C as checks.py (code)
    participant R as review job: reviewer agent
    participant RT as route job

    M->>GH: comment "/autose" on issue #2
    GH->>G: issue_comment event
    G->>G: actor is a maintainer, issue has label autose
    G-->>O: run=true, mode=build, round 1, resume_from S1
    O->>ST: load state.json for issue-2
    O->>O: strip assignment folders, lint baseline (4 pre-existing)
    O->>ST: S1 input hash unchanged: reuse spec.md
    O->>ST: S2 input hash unchanged: reuse design.md
    Note over SA: not called: S1 and S2 were reused (ADR-004)
    O->>IA: issue + spec + design + architecture
    IA-->>O: diff (markdown/extensions/fenced_code.py, changelog)
    O->>C: check_build: install, smoke import, new flake8 errors
    C-->>O: pass
    O->>TA: issue + spec ACs (no implementer reasoning)
    TA-->>O: tests/test_autose_issue_2.py
    O->>C: check_test_file, fail-to-pass on base, full suite
    C-->>O: fail: suite fails with this diff
    O->>IA: attempt 2 with failure output only (ADR-002)
    IA-->>O: new diff
    O->>C: check_build, then suite with the same tests
    C-->>O: pass
    O->>GH: push autose/issue-2 with the PAT, open PR #9
    GH->>GH: upstream CI on the PR (14 checks)
    O->>GH: poll check runs until all are green
    O->>ST: save artifacts and state (S1-S5 passed)
    O-->>R: pr=9, head_sha=9114a92
    R->>GH: read issue, PR diff, repository at head
    R-->>R: findings with evidence, schema check, evidence filter
    R->>GH: approve review as github-actions[bot]
    R-->>RT: verdict approve
    RT->>ST: save review.md / review.json
    RT->>GH: update the progress comment; stop (no round 2)
    M->>GH: decides whether to merge (never the workflow)
```

## What the sequence shows

- **Resume (ADR-004):** stages 1 and 2 were reused because their input hashes matched; no model call was made for them.
- **Retry with results only (ADR-002, D1):** the implementer's first attempt failed the suite. The second attempt got the failure output, not the tester's reasoning.
- **Two identities (ADR-005, ADR-012):** the PR is pushed with the PAT, so CI runs and the author differs from the reviewer, which posts with `GITHUB_TOKEN`.
- **Code decides (ADR-007):** every pass/fail step is a `checks.py` call or the CI status, not an agent's opinion.
- **Tokens:** build 1,757,130; review 34,698.
