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

## E2: to be decided (planned: ADR-001, separate tester vs implementer writes its own tests)
