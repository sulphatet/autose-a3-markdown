# Reusing the A1 skill in stage 1

Stage 1 reuses the `requirements-spec` skill from A1, version 1.0. The skill text is kept unchanged in `workflow/skills/requirements-spec/SKILL.md`. Everything that differs in the pipeline is set by the stage 1 prompt and by the orchestrator, and is listed here, so the original skill and the changes can be compared.

| # | Skill as written in A1 | In the pipeline | Why | Related ADR |
| --- | --- | --- | --- | --- |
| 1 | Mode is `interactive` when a human is present | Always `non-interactive`. Questions are logged, not asked | The run is headless. Nobody can answer mid-run. | ADR-002 |
| 2 | Step 7 uses the `fetch` MCP tool for external evidence | Tool not provided. `EVIDENCE.md` records "Tool availability: none", which is the skill's own fallback (§7.2 step 3) | An agent that reads untrusted issue text must not have network access. | ADR-005, ADR-009 |
| 3 | Output goes to `specs/<slug>/` with four files | The same four files are written into the run's artifact folder, not into the repository. `SRS.md` is published as `spec.md`, and the other three are uploaded next to it. | The brief names the artifact `spec.md`. Writing to the repo would put the spec in the PR diff, which the reviewer must not see. | ADR-004, ADR-008 |
| 4 | The skill validates itself and sets its own verdict | The verdict is an input. `checks.py` re-checks the structure (V-Q4, Given/When/Then ACs, no TBD, no weasel words) and decides pass/fail. | The same model grading its own work is weak evidence. | ADR-007 |
| 5 | Verdict `NOT READY — CLARIFICATION REQUIRED` ends with a reply listing questions | The run stops at stage 1. The orchestrator posts the open P1 questions as a comment on the issue. | This is how the vague issue is meant to end: explain and stop, without guessing. | ADR-002, ADR-009 |
| 6 | `PARTIALLY READY` lists the Ready items | Passes the check. Only `Ready` requirements and their ACs are handed to design and testing. The others stay listed in `spec.md` as not in scope for this PR. | Implementing guesses breaks the skill's own rule B1. | ADR-003 |
| 7 | The skill reads any input, including notes and RFPs | The only source is the issue title and body, numbered as `SRC-1`. It sits between untrusted-data delimiters. The repository and `ARCHITECTURE.md` are not given to this agent. | The spec should describe what the user asked for, not what the code happens to do. The skill already treats input text as data. | ADR-003, ADR-009 |
| 8 | Step 11 iteration when answers arrive | When the issue is edited after a stop, its input hash changes and the next run starts again at stage 1 (ADR-004). There is no in-place iteration. | Answers arrive by editing the issue or commenting, which starts a new run. | ADR-004 |
| 9 | Technology may appear only if a stakeholder stated it | Unchanged. The issue is about a Python library, so the language and the project are stated facts (`[S]`). | — | — |

The skill is long. For a two-line bug report it makes the stage 1 prompt larger than the issue by a wide margin. That cost is accepted for consistency with A1. Stage 1 token use is reported separately in the results so the cost is visible.
