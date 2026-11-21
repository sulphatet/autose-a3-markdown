# Python-Markdown — Software Requirements Specification
Version: v0.1 | Date: 2026-11-21 | Mode: non-interactive | Status: Draft
> Stakeholder confirmation: NOT obtained — all [I] items unconfirmed

## 1. Purpose and Scope
### In-scope
- Handling of footnote definitions that are indented inside the body of another footnote when using the `footnotes` extension.
### Out-of-scope (stated)
- Non-indented footnote definitions (which currently work correctly per SRC-1.5).
### Scope unknown
- Whether nested footnote definitions should be rendered as standalone footnotes or nested HTML structures (Q-1).

## 2. Actors
| ID | Actor | Description | Tag | Source/Link |
|---|---|---|---|---|
| ACT-1 | Python-Markdown User | A developer using the `markdown` library with the `footnotes` extension. | [S] | SRC-1.2, SRC-1.3 |

## 3. Functional Requirements
| ID | Requirement (EARS) | Tag | Source / Link | Priority | Readiness |
|---|---|---|---|---|---|
| FR-001 | When a footnote definition is indented inside the body of another footnote, the system shall process and render the nested footnote definition instead of causing it to vanish without warning. | [S][I] | SRC-1.1, SRC-1.6 | Must | Needs-Clarification |

### FR-001 acceptance criteria:
- AC-FR-001-1: Given Markdown input containing a footnote definition indented inside another footnote body (e.g., `[^1]: First\n\n    [^2]: Second`), when rendered with `markdown.markdown(text, extensions=["footnotes"])`, then both footnote definitions appear in the output list.
- AC-FR-001-2: Given Markdown input where footnote 1 references an indented footnote `[^2]`, when rendered, then the generated link to `#fn:2` resolves successfully to an existing footnote item in the list.

## 4. Non-Functional Requirements
*(None)*

## 5. Constraints
| ID | Constraint | Tag | Source/Link |
|---|---|---|---|
| CON-01 | Python language and Python-Markdown library must be used. | [S] | SRC-1.2 |

## 6. Dependencies
| ID | Dependency | Owner | Status |
|---|---|---|---|
| DEP-01 | Python-Markdown `footnotes` extension | Python-Markdown maintainers | Active |

## 7. Risks
| ID | Risk | L | I | Mitigation / reducing question |
|---|---|---|---|---|
| RSK-01 | Changes to footnote parsing might alter behavior for existing indented content blocks inside footnotes. | M | M | Ensure robust test coverage for block parsing inside footnotes. |

## 8. Traceability Matrix
- SRC-1.1 -> FR-001
- SRC-1.2 -> ACT-1, CON-01
- SRC-1.3 -> FR-001, ACT-1
- SRC-1.4 -> FR-001
- SRC-1.5 -> Out-of-scope
- SRC-1.6 -> FR-001, ASM-1, Q-1

## 9. Change Log
- v0.1: Initial draft from issue #3.

## Appendix A. Source Register
- SRC-1.1: When a footnote definition is nested (indented) inside the body of another footnote, it vanishes from the output without any warning.
- SRC-1.2: `import markdown`
- SRC-1.3: `text = """\nMain[^1].\n\n[^1]: First\n\n    [^2]: Second\n"""`
- SRC-1.4: `print(markdown.markdown(text, extensions=["footnotes"]))`
- SRC-1.5: Only footnote 1 is rendered; the text "Second" is gone and there is no `fn:2` item in the list. If footnote 1 references `[^2]`, I get a link to `#fn:2` that goes nowhere.
- SRC-1.6: If I write `[^2]: Second` without the indentation it works, so I think only the indented form is affected. I'd expect the nested definition to show up as its own footnote, just like the non-indented one.


---
## Pipeline check (stage 1, `checks.check_spec`)

**Check: FAIL**

- A1 skill verdict is `NOT READY`: the issue is not specific enough to implement
- V-Q4 is PASS
- no requirement is marked `Ready` in the SRS tables


---
## Stopped at stage 1 (Requirements)

A1 skill verdict is `NOT READY`: the issue is not specific enough to implement; V-Q4 is PASS; no requirement is marked `Ready` in the SRS tables
