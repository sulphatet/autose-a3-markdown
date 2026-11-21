# Architecture Decision Records

One file per decision, in the Nygard format used in A2: Status, Context, Decision, Alternatives considered, Consequences. Each ADR also says what evidence would show that it is wrong.

ADRs are never edited after a run proves them wrong. The old ADR is marked `Superseded by ADR-0xx`, and a new ADR records what was learned.

The decisions and their reasoning are the author's. Claude Code helped write them up from the author's notes. See the AI-use section of the top-level README.

| ADR | Decision | Chosen | Main option rejected | Status |
| --- | --- | --- | --- | --- |
| [001](ADR-001.md) | Splitting the work (D1) | 5 LLM agents with closed contexts, plus a deterministic release script | One agent for every stage | Accepted |
| [002](ADR-002.md) | Control flow (D2) | Coded state machine, with review rounds re-dispatched as new runs | LLM planner that chooses the next stage | Accepted |
| [003](ADR-003.md) | Hand-offs (D3) | Fixed input set per agent, files only, no conversations | Pass the full conversation forward | Accepted |
| [004](ADR-004.md) | State (D4) | `autose-state` branch + run artifacts, deterministic resume by input hash | Commit artifacts to the PR branch | Accepted |
| [005](ADR-005.md) | Tools (D5) | Own tool layer per role, path jail, command allow-list, split GitHub identities | Generic bash tool / GitHub MCP server for agents | Accepted |
| [006](ADR-006.md) | Models (D6) | Gemini 3.5 Flash-Lite for builders, 3.1 Flash-Lite for the reviewer | Stronger Flash/Hydrogen models (unavailable on free tier) | Accepted |
| [007](ADR-007.md) | Checks (D7) | Code decides every pass/fail; LLM output is only an input | LLM judge decides stage passes | Accepted |
| [008](ADR-008.md) | Reviewer independence (D8) | Separate job, model, prompt, identity and inputs; evidence-backed findings | Reviewer as another step in the build job | Accepted |
| [009](ADR-009.md) | Safety and failures (D9) | Layered budgets, retry/fallback, partial artifact + stop, injection containment | Trusting prompt instructions alone | Accepted |
| [010](ADR-010.md) | Triggers (D10) | Label or `/autose` from trusted users; `/autose` on a PR re-runs review only; queued per issue | Any comment author can trigger | Accepted |
