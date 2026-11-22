# python-markdown-toc — Software Requirements Specification
Version: v0.1 | Date: 2026-11-22 | Mode: non-interactive | Status: Draft
> Stakeholder confirmation: NOT obtained — all [I] items unconfirmed (run mode non-interactive)

## 1. Purpose and Scope
### In Scope
- Allowing headings with a specific class (`notoc`) to be excluded from the generated table of contents (`[TOC]`) by the `toc` extension [S].
- Rendering excluded headings normally on the page with their normal IDs and classes (e.g., `<h2 class="notoc" id="changelog">`) [S].
- Omitting excluded headings from `md.toc_tokens` [S].

### Out of Scope / Scope Unknown
- Configuring alternative class names other than `notoc` without further clarification (see Q-1).

## 2. Actors
| ID | Actor | Description | Tag | Source/Link |
|---|---|---|---|---|
| ACT-1 | Markdown Author | Author writing markdown documents using Python-Markdown | [S] | SRC-1.1 |
| ACT-2 | Downstream Tool / Extension | Consumer of `md.toc_tokens` | [S] | SRC-1.7 |

## 3. Functional Requirements
| ID | Requirement (EARS) | Tag | Source / Link | Priority | Readiness |
|---|---|---|---|---|---|
| FR-001 | When the `toc` extension encounters a heading marked with the class `notoc`, the system shall exclude that heading from the generated table of contents. | [S] | SRC-1.4, SRC-1.5 | Must | Needs-Clarification |
| FR-002 | When a heading is excluded from the table of contents via the `notoc` class, the system shall still render the heading itself on the page with its normal id and classes. | [S] | SRC-1.1, SRC-1.6 | Must | Needs-Clarification |
| FR-003 | When a heading is excluded from the table of contents via the `notoc` class, the system shall exclude it from `md.toc_tokens`. | [S] | SRC-1.7 | Must | Needs-Clarification |

### FR-001 acceptance criteria:
- AC-FR-001-1: Given markdown input containing `[TOC]\n\n# Guide\n\n## Changelog {.notoc}`, when parsed with the `toc` and `attr_list` extensions, then the generated table of contents does not contain "Changelog".

### FR-002 acceptance criteria:
- AC-FR-002-1: Given markdown input containing `## Changelog {.notoc}`, when parsed with the `toc` and `attr_list` extensions, then the HTML output contains `<h2 class="notoc" id="changelog">Changelog</h2>`.

### FR-003 acceptance criteria:
- AC-FR-003-1: Given markdown input containing `## Changelog {.notoc}`, when parsed with the `toc` extension, then `md.toc_tokens` does not include the entry for "Changelog".

## 4. Non-Functional Requirements
None.

## 5. Constraints
None.

## 6. Dependencies
| ID | Dependency | Owner | Status |
|---|---|---|---|
| DEP-01 | Python-Markdown `attr_list` extension (for parsing `{.notoc}` syntax in markdown) | Python-Markdown maintainers | Stated |

## 7. Risks
| ID | Risk | L | I | Mitigation / reducing question |
|---|---|---|---|---|
| RSK-01 | Users might expect configurable class names instead of a hardcoded `notoc` string. | M | L | Answer Q-1 |

## 8. Traceability Matrix
- SRC-1.1 → ACT-1, FR-002
- SRC-1.2 → Context
- SRC-1.3 → Context
- SRC-1.4 → FR-001, ASM-1
- SRC-1.5 → FR-001
- SRC-1.6 → FR-002
- SRC-1.7 → ACT-2, FR-003

## 9. Change Log
- v0.1 (2026-11-22): Initial draft extracted from issue SRC-1.

## Appendix A. Source Register
- SRC-1.1: Issue #5: toc: let me leave a heading out of the table of contents
- SRC-1.2: I have a few headings ("Changelog", "Footnotes"…) that I don't want in the generated table of contents, but I still want them on the page with their normal id.
- SRC-1.3: Could the `toc` extension skip any heading that has the class `notoc`?
- SRC-1.4: With `attr_list` that would look like: [TOC] # Guide ## Install ## Changelog {.notoc} ## Usage
- SRC-1.5: The TOC should list Guide, Install and Usage, but not Changelog.
- SRC-1.6: The Changelog heading itself should still be rendered as `<h2 class="notoc" id="changelog">`.
- SRC-1.7: It would be nice if `md.toc_tokens` left it out too, so other tools see the same list.


---
## Pipeline check (stage 1, `checks.check_spec`)

**Check: PASS**

- A1 skill verdict is `NOT READY` (recorded, not blocking)
- no requirement is marked `Ready`; using all acceptance criteria, open questions are treated as assumptions
- 3 testable acceptance criteria: AC-FR-001-1, AC-FR-002-1, AC-FR-003-1
