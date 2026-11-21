# toc-exclude-class — Software Requirements Specification
Version: v0.1 | Date: 2026-11-21 | Mode: non-interactive | Status: Draft
> Stakeholder confirmation: NOT obtained — all [I] items unconfirmed; maintainer label `autose` confirms explicitly requested behaviour is Must.

## 1. Purpose and Scope
### In Scope
- Allowing headings with the CSS class `notoc` to be excluded from the generated table of contents (`toc` extension) while retaining them on the rendered page with their normal ID and classes (specifically including `class="notoc"`). [S]
- Ensuring `md.toc_tokens` also omits headings marked with `notoc`. [S]

### Out of Scope / Scope Unknown
- Configuring custom class names other than `notoc` (unspecified / open question Q-1).

## 2. Actors
| ID | Actor | Description | Tag | Source/Link |
|---|---|---|---|---|
| ACT-1 | Markdown Author | A user writing Markdown documents processed by Python-Markdown with the `toc` extension. | [S] | SRC-1.1 |

## 3. Functional Requirements
| ID | Requirement (EARS) | Tag | Source / Link | Priority | Readiness |
|---|---|---|---|---|---|
| FR-001 | When generating a table of contents, the `toc` extension shall skip any heading that has the class `notoc`. | [S] | SRC-1.2, SRC-1.5 | Must | Needs-Clarification |
| FR-002 | When building the table of contents tokens structure, `md.toc_tokens` shall omit any heading that has the class `notoc`. | [S] | SRC-1.6 | Must | Needs-Clarification |
| FR-003 | When rendering a heading with the class `notoc`, the system shall still render the heading element on the page with its normal ID and classes (e.g. `<h2 class="notoc" id="changelog">`). | [S] | SRC-1.1, SRC-1.4 | Must | Needs-Clarification |

### FR-001 Acceptance Criteria
- AC-FR-001-1: Given Markdown input `[TOC]\n\n# Guide\n\n## Install\n\n## Changelog {.notoc}\n\n## Usage`, when processed with `toc` and `attr_list` extensions enabled, then the output HTML table of contents shall list Guide, Install, and Usage, but not Changelog.

### FR-002 Acceptance Criteria
- AC-FR-002-1: Given Markdown input containing a heading with `{.notoc}`, when processed with `toc` and `attr_list` extensions, then `md.toc_tokens` shall not contain an entry for that heading.

### FR-003 Acceptance Criteria
- AC-FR-003-1: Given Markdown input `## Changelog {.notoc}`, when processed with `toc` and `attr_list` extensions, then the rendered heading in the HTML body shall be `<h2 class="notoc" id="changelog">Changelog</h2>` (or equivalent attribute ordering).

## 4. Non-Functional Requirements
*(None)*

## 5. Constraints
*(None)*

## 6. Dependencies
| ID | Dependency | Owner | Status |
|---|---|---|---|
| DEP-01 | `attr_list` extension (or equivalent mechanism supplying classes to headers) | Python-Markdown core / maintainers | Active |

## 7. Risks
*(None)*

## 8. Traceability Matrix
- SRC-1.1 -> ACT-1, FR-003
- SRC-1.2 -> FR-001
- SRC-1.3 -> (Context)
- SRC-1.4 -> FR-003
- SRC-1.5 -> FR-001, AC-FR-001-1
- SRC-1.6 -> FR-002

## 9. Change Log
- v0.1: Initial draft from Issue #2853d762.

## Appendix A. Source Register
- SRC-1.1: I have a few headings ("Changelog", "Footnotes"…) that I don't want in the generated table of contents, but I still want them on the page with their normal id.
- SRC-1.2: Could the `toc` extension skip any heading that has the class `notoc`?
- SRC-1.3: With `attr_list` that would look like:
- SRC-1.4: The Changelog heading itself should still be rendered as `<h2 class="notoc" id="changelog">`.
- SRC-1.5: The TOC should list Guide, Install and Usage, but not Changelog.
- SRC-1.6: It would be nice if `md.toc_tokens` left it out too, so other tools see the same list.


---
## Pipeline check (stage 1, `checks.check_spec`)

**Check: FAIL**

- A1 skill verdict is `PARTIALLY READY`
- V-Q4 is PASS
- no requirement is marked `Ready` in the SRS tables


---
## Stopped at stage 1 (Requirements)

A1 skill verdict is `PARTIALLY READY`; V-Q4 is PASS; no requirement is marked `Ready` in the SRS tables
