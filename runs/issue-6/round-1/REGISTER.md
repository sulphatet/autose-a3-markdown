## Assumptions
| ID | Assumption | Basis | Affects | Status | Confirm via Q-n |
|---|---|---|---|---|---|
| ASM-01 | The user is referring to the built-in `toc` extension in Python-Markdown. | Inferred from "toc extension" mention in the issue. | FR-001 | Unconfirmed | Q-01 |

## Open Questions
| ID | Priority | Question | Why it matters | Blocks | Ask whom | Status | Answer |
|---|---|---|---|---|---|---|---|
| Q-01 | P1 | Is "toc extension" referring specifically to Python-Markdown's `toc` extension? | Determines whether this requirement applies to the Python-Markdown library. | FR-001 | Stakeholder / Issue reporter | Open | |
| Q-02 | P1 | What specific behavior or feature is expected to make the TOC "smarter" or more usable out of the box (e.g., depth limiting, collapsible headings, scrolling, filtering)? | The request is entirely open-ended ("Not sure what the best approach is"). Without specific requirements, no concrete implementation can be built or verified. | FR-001, NFR-USE-01 | Stakeholder / Issue reporter | Open | |

## Conflicts
(None)

## Glossary
| ID | Term | Candidate meanings | Resolved meaning | Q-n |
|---|---|---|---|---|
| GL-01 | smarter | 1. Limiting maximum heading depth by default.<br>2. Collapsing nested sub-lists.<br>3. Providing interactive filtering/scrolling UI. | Unresolved | Q-02 |
| GL-02 | overwhelming | 1. Too many items displayed at once.<br>2. Too many nesting levels shown.<br>3. Lack of collapsible sections. | Unresolved | Q-02 |

## Confirmation Records
(None)
