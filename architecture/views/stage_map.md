# Stage map

| # | Stage | Agent | Model (ADR-006) | Artifact | Check (ADR-007) | Decided by | On failure |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Requirements | Spec agent (A1 skill) | gemini-3.5-flash-lite | `spec.md` (+ `REGISTER.md`, `VALIDATION.md`, `EVIDENCE.md`) | A1 verdict READY / PARTIALLY READY, V-Q4 PASS, every Ready AC in Given/When/Then, no TBD or weasel words | `checks.py` | Stop; post the P1 open questions on the issue |
| 2 | Design | Designer | gemini-3.5-flash-lite | `design.md` | Change-list table; files exist; symbols found by `ast`; every Ready AC covered | `checks.py` | Back to designer once for format; then stop |
| 3 | Implementation | Implementer | gemini-3.5-flash-lite | `diff.patch` | Non-empty diff in allowed paths; `pip install -e .`; import + smoke call; `flake8 markdown` | `checks.py` | Retry within budget; then stop |
| 4 | Testing | Tester writes tests; code runs them | gemini-3.5-flash-lite | `test_report.md` | One test per Ready AC; new tests fail on base and pass on branch; full `unittest` suite passes | `checks.py` | Back to S3 (≤ 3), then S2 once, then stop |
| 5 | Release | `release.py` (no LLM) | — | `pr.md` + PR link | PR is `OPEN`; every CI check green | `checks.py` via `gh` | CI red → back to S3 with the job log |
| 6 | Review | Reviewer (separate job) | gemini-3.1-flash-lite | `review.md` (+ `review.json`) | Valid schema; findings have evidence; approve, or 2 rounds used | `review.py` | `kind=approach` → new run from S2; `kind=code` → from S3; at most 2 rounds |
| — | Merge | Human | — | — | — | Maintainer | — |
