## Assumptions
| ID | Assumption | Basis | Affects | Status | Confirm via Q-n |
|---|---|---|---|---|---|
| ASM-1 | The requested feature applies specifically to the `toc` extension in Python-Markdown. | SRC-1.4 | All requirements | Unconfirmed | Q-1 |

## Open Questions
| ID | Priority P1-3 | Question | Why it matters | Blocks | Ask whom | Status | Answer |
|---|---|---|---|---|---|---|---|
| Q-1 | P1 | Should the class name used to exclude headings from the TOC be configurable, or strictly hardcoded to `notoc` as requested? | Determines whether configuration options for the class name need to be added to the TOC extension. | FR-001 | Maintainer / Reporter | Open | — |
| Q-2 | P2 | Should headings excluded via `.notoc` also be excluded from `md.toc_tokens` globally or only when generated? | Determines the exact behavior of `md.toc_tokens` integration. | FR-003 | Maintainer / Reporter | Open | — |

## Conflicts
None.

## Glossary
| ID | Term | Candidate meanings | Resolved meaning | Q-n |
|---|---|---|---|---|
| GL-1 | `notoc` | 1. A CSS class recognized by the toc extension to omit headings from the table of contents.<br>2. A marker that completely removes the heading from rendering. | Pending confirmation | Q-1 |

## Confirmation Records
None.
