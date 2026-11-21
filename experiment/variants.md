# Decision experiments: variants

## E1: reviewer model (tests ADR-006 and ADR-008)

**Question:** does a reviewer on a *different* model catch more planted defects, with fewer false alarms, than a reviewer on the *same* model as the builders?

| Variant | Reviewer model | Trigger |
| --- | --- | --- |
| A (ADR-006 as chosen) | `gemini-3.1-flash-lite` | `/autose` on a seeded PR |
| B (same model) | `gemini-3.5-flash-lite` (the builders' model) | `/autose variant=same-model` |

Everything else is identical: prompt, inputs (issue + diff + repository at PR head), tools, evidence rules, job. Each of the 5 seeded PRs is reviewed under both variants. The real pipeline PRs (issues #2-#6) are reviewed under variant A by the workflow itself.

**Measures:**
- detection: `request_changes` on a defective PR, with a finding that names the planted defect;
- false alarm: `request_changes` on the correct PR;
- routing: `kind` matches the label;
- findings dropped by code for missing evidence.

## E2: stage 1 readiness rule (tests the A1 adaptation and ADR-007's stage 1 check)

**Why:** in the first round of runs, the A1 skill under prompt v2 stopped two clear issues at stage 1:
- #3: "is this intended behaviour?";
- #5: an invented question about configurability, with all requirements marked Needs-Clarification.

The vague issue #6 stopped as intended.

**Question:** does a stricter readiness rule let clear issues through without letting the vague one through?

| Variant | Stage 1 prompt | Trigger |
| --- | --- | --- |
| A (current default) | `workflow/prompts/spec.md` (v2) | label `autose` / `/autose` |
| B | `workflow/prompts/spec_v3.md`: v2 plus rule 5a. An `[S]` requirement with a testable AC is Ready unless a P1 question blocks it; P2/P3 never block; never ask whether reported behaviour is "intended". | `/autose variant=spec-v3` on the issue |

Everything after stage 1 is identical: models, prompts, checks, budgets, reviewer. Variant B runs keep separate state (`runs/issue-<n>-spec-v3/`), branches (`autose/issue-<n>-spec-v3`), PRs and progress comments, so variant A's results are never overwritten. Both variants run on all five issues (#2-#6) at the same base commit.

**Measures:**
- stage 1 pass rate per issue;
- whether #6 (vague) still stops at stage 1, which is the safety side of the trade-off;
- for issues that get through, the stage reached and the hidden-test results;
- stage 1 tokens.
