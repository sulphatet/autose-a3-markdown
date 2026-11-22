# Python-Markdown — Software Requirements Specification
Version: v0.1 | Date: 2026-11-22 | Mode: non-interactive | Status: Draft
> Stakeholder confirmation: obtained from maintainer (label autose) — explicitly requested behaviour is Must; no stakeholder conversation conducted for open questions.

## 1. Purpose and Scope
### In-scope [S]
- Supporting pipe syntax `[[Target Page|what the reader sees]]` in the `wikilinks` extension.
- Preserving existing URL building behavior (`base_url`, `end_url`, `html_class`, `build_url`) for the target part before the `|`.
- Using the text after the `|` as the rendered link text.
- Keeping plain `[[Page]]` links working exactly as they currently do.

### Out-of-scope [S]
- None explicitly stated.

### Scope unknown / Open questions
- Edge case handling for whitespace around the pipe and literal pipe escaping (Q-1, Q-2).

## 2. Actors
| ID | Actor | Description | Tag | Source/Link |
|---|---|---|---|---|
| ACT-01 | Markdown User / Developer | A user calling `markdown.markdown()` with the `wikilinks` extension. | [S] | SRC-1.4 |

## 3. Functional Requirements
| ID | Requirement (EARS) | Tag | Source / Link | Priority | Readiness |
|---|---|---|---|---|---|
| FR-001 | When the `wikilinks` extension processes a WikiLink containing a pipe character in the format `[[Target Page|display text]]`, the system shall generate an anchor tag where the href is built from the target page part using existing configuration options (`base_url`, `end_url`, `html_class`, `build_url`) and the inner text of the anchor is the display text part. | [S] | SRC-1.1, SRC-1.3, SRC-1.5 | Must | Ready |
| FR-002 | While processing WikiLinks, the system shall keep plain `[[Page]]` links working exactly as they currently do. | [S] | SRC-1.2, SRC-1.6 | Must | Ready |

### FR-001 acceptance criteria:
- AC-FR-001-1: Given Markdown input `See [[Main Page|the home page]].` and extensions `["wikilinks"]`, when parsed via `markdown.markdown()`, then the output is `<p>See <a class="wikilink" href="/Main_Page/">the home page</a>.</p>`.

### FR-002 acceptance criteria:
- AC-FR-002-1: Given Markdown input `See [[Main Page]].` and extensions `["wikilinks"]`, when parsed via `markdown.markdown()`, then the output is `<p>See <a class="wikilink" href="/Main_Page/">Main Page</a>.</p>` (or the standard existing output format for plain wikilinks).

## 4. Non-Functional Requirements
None specified in the source.

## 5. Constraints
| ID | Constraint | Tag | Source/Link |
|---|---|---|---|
| CON-01 | Must maintain backward compatibility with existing plain `[[Page]]` syntax and configuration options (`base_url`, `end_url`, `html_class`, `build_url`). | [S] | SRC-1.5, SRC-1.6 |

## 6. Dependencies
| ID | Dependency | Owner | Status |
|---|---|---|---|
| DEP-01 | Python-Markdown `wikilinks` extension codebase | Python-Markdown maintainers | Active |

## 7. Risks
| ID | Risk | L | I | Mitigation / reducing question |
|---|---|---|---|---|
| RSK-01 | Parsing ambiguity if target names or link texts contain pipe characters or special markdown formatting. | L | M | Add robust regex parsing and clarify via Q-2. |

## 8. Traceability Matrix
- SRC-1.1 → FR-001
- SRC-1.2 → FR-002
- SRC-1.3 → FR-001
- SRC-1.4 → FR-001, AC-FR-001-1
- SRC-1.5 → FR-001, CON-01
- SRC-1.6 → FR-002, CON-01

## 9. Change Log
- v0.1 (2026-11-22): Initial draft from Issue #4.

## Appendix A. Source Register
- SRC-1.1: Issue #4: WikiLinks: support a different link text, like [[Page|text]]
- SRC-1.2: Most wikis let you write `[[Target Page|what the reader sees]]`.
- SRC-1.3: With the `wikilinks` extension that syntax isn't recognised at all; `[[Main Page|the home page]]` comes out as literal text.
- SRC-1.4: What I'd like: `markdown.markdown("See [[Main Page|the home page]].", extensions=["wikilinks"]) # <p>See <a class="wikilink" href="/Main_Page/">the home page</a>.</p>`
- SRC-1.5: So the part before `|` builds the URL exactly like it does today (same `base_url`, `end_url`, `html_class` and `build_url` handling) and the part after `|` is the text of the link.
- SRC-1.6: Plain `[[Main Page]]` should keep working exactly as now.


---
## Pipeline check (stage 1, `checks.check_spec`)

**Check: PASS**

- A1 skill verdict is `READY FOR IMPLEMENTATION`
- V-Q4 is PASS
- 2 Ready requirement(s), 2 testable acceptance criteria: AC-FR-001-1, AC-FR-002-1
