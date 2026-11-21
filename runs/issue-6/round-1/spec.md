# TOC Overwhelming on Long Pages — Software Requirements Specification
Version: v0.1 | Date: 2026-11-21 | Mode: non-interactive | Status: Draft
> Stakeholder confirmation: NOT obtained — all [I] items unconfirmed. Priority: Must (maintainer label autose).

## 1. Purpose and Scope
### In Scope
- Enhancing the Python-Markdown `toc` extension to address long and overwhelming tables of contents on large pages, as requested in Issue #6. [S][SRC-1.2]

### Out of Scope (Stated)
- None explicitly stated.

### Scope Unknown / Open
- The specific mechanism or feature set required to make the TOC "smarter" and less overwhelming. [Q-1]

## 2. Actors
| ID | Actor | Description | Tag | Source/Link |
|---|---|---|---|---|
| ACT-1 | Documentation Reader | End-user browsing long documentation pages and viewing the table of contents. | [S] | SRC-1.1 |
| ACT-2 | Documentation Author / Maintainer | User configuring Python-Markdown and the `toc` extension for a docs site. | [I] | ASM-1 |

## 3. Functional Requirements
| ID | Requirement (EARS) | Tag | Source / Link | Priority | Readiness |
|---|---|---|---|---|---|
| FR-001 | When generating a table of contents for a document, the `toc` extension shall provide a mechanism to prevent the table of contents from becoming overwhelming on long pages. | [S] | SRC-1.2, SRC-1.3 | Must | Needs-Clarification |
| FR-002 | Where the `toc` extension is used, the system shall provide out-of-the-box usability improvements for handling long tables of contents. | [S] | SRC-1.4 | Must | Needs-Clarification |

### FR-001 acceptance criteria:
- AC-FR-001-1: Given a Markdown document with many headings, when the `toc` extension processes the document, then the resulting TOC output incorporates the unspecified smart handling mechanism `<TBD: Q-1>`.

### FR-002 acceptance criteria:
- AC-FR-002-1: Given a default configuration of the `toc` extension, when rendering a long page, then the TOC output exhibits out-of-the-box usability enhancements `<TBD: Q-2>`.

## 4. Non-Functional Requirements
*(None stated or inferred at this stage)*

## 5. Constraints
*(None stated)*

## 6. Dependencies
| ID | Dependency | Owner | Status |
|---|---|---|---|
| DEP-1 | Python-Markdown `toc` extension codebase | Python-Markdown maintainers | Open |

## 7. Risks
| ID | Risk | L | I | Mitigation / reducing question |
|---|---|---|---|---|
| RSK-1 | Implementing a change to default TOC behavior might break backwards compatibility for existing users relying on current TOC output. | M | H | Clarify whether changes apply by default or via configuration option (Q-2). |

## 8. Traceability Matrix
- SRC-1.1 → ACT-1
- SRC-1.2 → FR-001, In Scope
- SRC-1.3 → FR-001
- SRC-1.4 → FR-002
- Q-1 → FR-001, GL-1, GL-2, ASM-2
- Q-2 → FR-002, ASM-2, RSK-1

## 9. Change Log
- v0.1 (2026-11-21): Initial draft extracted from Issue #6.

## Appendix A. Source Register
- SRC-1.1: "On our docs site the table of contents gets really long and kind of overwhelming for big pages."
- SRC-1.2: "Can the toc extension be smarter about this?"
- SRC-1.3: "Not sure what the best approach is, but it'd be great if it was more usable out of the box."
- SRC-1.4: "(Covered by SRC-1.3 regarding usability out of the box)."


---
## Pipeline check (stage 1, `checks.check_spec`)

**Check: FAIL**

- A1 skill verdict is `NOT READY`: the issue is not specific enough to implement
- V-Q4 is PASS
- no requirement is marked `Ready` in the SRS tables


---
## Stopped at stage 1 (Requirements)

A1 skill verdict is `NOT READY`: the issue is not specific enough to implement; V-Q4 is PASS; no requirement is marked `Ready` in the SRS tables
