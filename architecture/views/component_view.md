# Component view

Agents, their tools, and who calls whom. Solid arrows are calls. Dotted arrows are files handed over (ADR-003). Every agent is called by the orchestrator, and no agent calls another agent (ADR-002).

```mermaid
flowchart TB
    subgraph GH[GitHub]
        ISSUE[Issue + label / comment]
        PR[Pull request]
        CI[Upstream CI<br/>tox matrix, lint, changelog]
        STATE[(autose-state branch)]
        ART[(Run artifacts)]
    end

    subgraph GATE[job: gate — no secrets, issues:read]
        G[gate.py<br/>actor + trigger check]
    end

    subgraph BUILD[job: build — GITHUB_TOKEN contents/issues write; PAT only in release step]
        ORCH[orchestrator.py<br/>state machine, budgets, resume]
        CHK[checks.py<br/>deterministic stage checks]
        LLM[llm.py<br/>Gemini client: retry, fallback, token count]
        TOOLS[tools.py<br/>role-scoped tools, path jail,<br/>command allow-list, scrubbed env]
        SPEC[Spec agent<br/>A1 skill]
        DES[Designer]
        IMP[Implementer]
        TST[Tester]
        REL[release.py<br/>no LLM]
    end

    subgraph REVIEW[job: review — contents:read, pull-requests:write, no PAT]
        RORCH[review.py]
        REV[Reviewer agent<br/>gemini-4-hydrogen]
        RTOOLS[read-only tools + optional run]
    end

    GEM[(Gemini API)]

    ISSUE -->|event| G -->|issue no., mode| ORCH
    ORCH --> SPEC & DES & IMP & TST
    SPEC & DES & IMP & TST --> LLM --> GEM
    SPEC & DES & IMP & TST -. tool calls .-> TOOLS
    ORCH --> CHK
    ORCH --> REL -->|PAT: push, gh pr create| PR --> CI
    REL -->|gh pr checks --watch| CI
    ORCH -->|state.json + artifacts| STATE & ART
    ORCH -->|progress comment| ISSUE

    SPEC -. spec.md .-> DES -. design.md .-> IMP -. diff.patch .-> TST
    CHK -. failure output only .-> IMP

    PR -->|needs: build| RORCH --> REV --> GEM
    REV -. tool calls .-> RTOOLS
    RORCH -->|gh pr review approve / request-changes| PR
    RORCH -->|request_changes and round < 2:<br/>workflow_dispatch resume_from S2/S3| G
```

## Tools per component

| Component | Tools | Provided by |
| --- | --- | --- |
| Spec agent | `submit` only | `tools.py` (Gemini function declarations) |
| Designer | `list_dir`, `read_file`, `search`, `submit` | `tools.py` |
| Implementer | read tools, `write_file`/`replace_in_file` (source), `run` (build, tests), `submit` | `tools.py` |
| Tester | read tools, `write_file` (`tests/` only), `run` (tests), `submit` | `tools.py` |
| Reviewer | read tools, `run` (optional), `submit` | `tools.py`, in the review job |
| Orchestrator / release / review driver | `gh` CLI, `git` | runner, with job-scoped tokens |
