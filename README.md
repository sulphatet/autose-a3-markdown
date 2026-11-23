# AutoSE Assignment 3: Agentic SDLC Workflow

Syed Affan Daimi, 2025701010

A GitHub Actions workflow in which agents turn an issue into a tested and reviewed pull request. A person always makes the merge decision.

- **Fork of:** https://github.com/Python-Markdown/markdown
- **Pinned commit:** `3f2c5510bd8d64a73ec18342f740371bcde9b20c` ("Avoid rescanning for a comment close after unclosed comments"). The upstream README was moved to `README.upstream.md`.
- **Models (ADR-006):** `gemini-3.5-flash-lite` for the spec, design, implementation and test agents; `gemini-3.1-flash-lite` for the independent reviewer. Gemini API free tier.
- **Report:** `report.pdf`. **Demo video:** [`demo.mp4`](demo.mp4) (4 min)
- **Results:** [`results/runs.md`](results/runs.md) (every run, PR and review) and [`results/results.csv`](results/results.csv). 25 runs, 11.8M tokens in total.

## How to trigger it

You need triage or write access to this repository.

| Action | Effect |
| --- | --- |
| Add the label `autose` to an issue | Full run: stages 1-6 |
| Comment `/autose` on an issue | Full run, or resume from saved state |
| Comment `/autose` on a pull request opened by autose, or on a seeded PR (`autose-seed/issue-<n>-<tag>`) | Review only, against the PR's latest commit. Add `variant=same-model` to use the builders' model (experiment E1). |
| Actions → autose → Run workflow (`issue`, `round`, `resume_from`) | Manual run; also how review rounds are started |

You can follow a run in four places:
- the progress comment on the issue;
- the Actions run, with its artifacts `autose-issue-<n>-round-<r>`;
- the pull request and its review;
- the `autose-state` branch, under `runs/issue-<n>/`.

## Layout

| Path | What it is |
| --- | --- |
| `.github/workflows/autose.yml` | The workflow (a copy is in `workflow/autose.yml`) |
| `workflow/autose/` | Agent code: orchestrator (state machine), Gemini client, tools, checks, release, review, gate, route |
| `workflow/prompts/` | One prompt per agent |
| `workflow/skills/requirements-spec/SKILL.md` | The A1 skill, unchanged; how it is used is in `architecture/a1_skill_adaptation.md` |
| `workflow/context/ARCHITECTURE.md` | The A2 architecture document, given to the design, implementation and test agents |
| `architecture/decisions/` | ADR-001 ... ADR-012 |
| `architecture/views/` | Component view, sequence view, stage map |
| `experiment/` | The 5 issues, hidden tests (added after all runs), seeded reviewer PRs, variants |
| `results/` | `results.csv`, `runs.md` |

## Secrets

`GEMINI_API_KEY` (Gemini free tier) and `AUTOSE_PAT`, a fine-grained token limited to this repository with Contents and Pull requests read/write. Both are repository secrets and are deleted after grading.

## AI use

Claude Code (Claude Opus) was used substantially:

- **Discussing the design:** it laid out options and trade-offs for each decision. The author made every decision.
- **Writing up the ADRs:** it turned the author's decisions and reasoning into ADR text. The author reviewed and edited them.
- **Writing the agent code, prompts and workflow:** the author reviewed them.
- **Drafting the five issue texts and hidden tests:** the author reviewed them.

All runs, PRs and reviews linked in `results/runs.md` are real.
