# Python-Markdown Footnotes Extension — Software Requirements Specification
Version: v0.1 | Date: 2026-11-22 | Mode: non-interactive | Status: Draft
> Stakeholder confirmation: NOT obtained — all [I] items unconfirmed

## 1. Purpose and Scope
### In-scope
- Handling of footnote definitions that are indented inside the body of another footnote when using the `footnotes` extension in Python-Markdown.
- Preventing nested footnote definitions from vanishing without warning.

### Out-of-scope (Stated)
- Non-indented footnote definitions (these already work correctly).

### Scope unknown
- Whether nested footnote definitions should be hoisted to top-level footnotes or handled as nested structures.

## 2. Actors
| ID | Actor | Description | Tag | Source/Link |
|---|---|---|---|---|
| ACT-1 | Python Developer / Markdown User | A user invoking `markdown.markdown()` with the `footnotes` extension. | [S] | SRC-1.3 |

## 3. Functional Requirements
| ID | Requirement (EARS) | Tag | Source / Link | Priority | Readiness |
|---|---|---|---|---|---|
| FR-001 | When `markdown.markdown()` is called with text containing a footnote definition placed inside the body of another footnote, the system shall not cause the nested footnote definition to vanish silently from the output. | [S] | SRC-1.1, SRC-1.2, SRC-1.3 | Must | Needs-Clarification |
| FR-002 | Where a nested footnote definition is provided, the system shall render the nested footnote definition as a footnote in the output. | [I][U] | ASM-1, Q-1 | Must | Needs-Clarification |

### FR-001 acceptance criteria:
- AC-FR-001-1: Given markdown input with a nested footnote definition (`[^1]: First \n\n    [^2]: Second`), when `markdown.markdown(text, extensions=["footnotes"])` is executed, then no exception is raised and the string `"Second"` does not vanish silently without any output or warning.

### FR-002 acceptance criteria:
- AC-FR-002-1: Given markdown input with a nested footnote definition (`[^1]: First \n\n    [^2]: Second`), when `markdown.markdown(text, extensions=["footnotes"])` is executed, then the output includes the rendered footnote corresponding to `[^2]: Second` in the footnote list.

## 4. Non-Functional Requirements
*(None)*

## 5. Constraints
| ID | Constraint | Tag | Source/Link |
|---|---|---|---|
| CON-01 | Must use the `footnotes` extension in Python-Markdown. | [S] | SRC-1.3 |

## 6. Dependencies
| ID | Dependency | Owner | Status |
|---|---|---|---|
| DEP-01 | Python-Markdown library `footnotes` extension | Python-Markdown maintainers | Active |

## 7. Risks
| ID | Risk | L | I | Mitigation / reducing question |
|---|---|---|---|---|
| RSK-01 | Silent data loss of footnote content when authors nest footnote definitions. | H | H | Clarify expected behavior for nested footnote definitions via Q-1. |

## 8. Traceability Matrix
| Source sentence | Items |
|---|---|
| SRC-1.1 | FR-001 |
| SRC-1.2 | FR-001 |
| SRC-1.3 | FR-001, ACT-1, CON-01 |
| SRC-1.4 | FR-001 |
| SRC-1.5 | FR-001 |

| Item | Source / ASM / EV / Q |
|---|---|
| FR-001 | SRC-1.1, SRC-1.2, SRC-1.3, SRC-1.4, SRC-1.5 |
| FR-002 | ASM-1, Q-1 |
| ACT-1 | SRC-1.3 |
| CON-01 | SRC-1.3 |
| ASM-1 | FR-002 |
| Q-1 | FR-002, ASM-1 |

## 9. Change Log
- v0.1: Initial draft created from issue fae6b7ab.

## Appendix A. Source Register
- SRC-1.1: When a footnote definition is nested (indented) inside the body of another footnote, it vanishes from the output without any warning.
- SRC-1.2: Only footnote 1 is rendered; the text "Second" is gone and there is no `fn:2` item in the list.
- SRC-1.3: If footnote 1 references `[^2]`, I get a link to `#fn:2` that goes nowhere.
- SRC-1.4: If I write `[^2]: Second` without the indentation it works, so I think only the indented form is affected.
- SRC-1.5: I'd expect the nested definition to show up as its own footnote, just like the non-indented one.


---
## Pipeline check (stage 1, `checks.check_spec`)

**Check: PASS**

- A1 skill verdict is `NOT READY` (recorded, not blocking)
- no requirement is marked `Ready`; using all acceptance criteria, open questions are treated as assumptions
- 2 testable acceptance criteria: AC-FR-001-1, AC-FR-002-1
