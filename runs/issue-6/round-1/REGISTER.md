## Assumptions
| ID | Assumption | Basis | Affects | Status | Confirm via Q-n |
|---|---|---|---|---|---|
| ASM-1 | The docs site uses Python-Markdown and its built-in `toc` extension. | Issue context ("toc extension") | FR-001, FR-002 | Unconfirmed | Q-1 |
| ASM-2 | "Smarter about this" refers to reducing visual clutter or length of the generated TOC on long pages by default or via configuration. | Issue text ("gets really long and kind of overwhelming", "smarter about this") | FR-001, FR-002 | Unconfirmed | Q-2 |

## Open Questions
| ID | Priority | Question | Why it matters | Blocks | Ask whom | Status | Answer |
|---|---|---|---|---|---|---|---|
| Q-1 | P1 | Which specific features or configuration options (e.g., collapsible nesting, depth limiting, filtering, or UI controls) are expected to make the TOC "smarter" and less overwhelming? | Without knowing the desired feature or behavior, implementation cannot begin. | FR-001, FR-002 | Maintainer / Issue Reporter | Open | |
| Q-2 | P2 | Should this "smarter" behavior be enabled by default out of the box or require explicit configuration parameters in the `toc` extension? | Determines whether existing users' default TOC output changes. | FR-002 | Maintainer / Issue Reporter | Open | |

## Conflicts
*(None)*

## Glossary
| ID | Term | Candidate meanings | Resolved meaning | Q-n |
|---|---|---|---|---|
| GL-1 | overwhelming | 1. Too many heading levels shown at once; 2. Too many total items listed; 3. Lack of collapsible/expandable sections. | Unresolved | Q-1 |
| GL-2 | smarter | 1. Automatically collapsing nested levels beyond a certain depth; 2. Providing a maximum depth default; 3. UI-based folding/unfolding. | Unresolved | Q-1 |

## Confirmation Records
*(None)*