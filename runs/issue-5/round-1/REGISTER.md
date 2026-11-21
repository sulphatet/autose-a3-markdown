## Assumptions
| ID | Assumption | Basis | Affects | Status | Confirm via Q-n |
|---|---|---|---|---|---|
| ASM-1 | The requested feature applies when using the `toc` extension alongside the `attr_list` extension (or any mechanism that sets classes on headers). | Inferred from the mention of `attr_list` in the issue description. | FR-001 | Unconfirmed | Q-1 |

## Open Questions
| ID | Priority | Question | Why it matters | Blocks | Ask whom | Status | Answer |
|---|---|---|---|---|---|---|---|
| Q-1 | P2 | Should the class name triggering this behaviour be configurable (e.g. via a config option), or is hardcoding `notoc` sufficient, or both? | Determines whether configuration options need to be added to the `toc` extension. | FR-001 | Maintainer / Author | Open | |
| Q-2 | P3 | Should `md.toc_tokens` exclude excluded headings completely, or is there any case where they should be preserved in tokens with a flag? | The issue states "It would be nice if md.toc_tokens left it out too", but confirmation on whether `md.toc_tokens` should strictly omit them is needed. | FR-002 | Maintainer / Author | Open | |

## Conflicts
*(None)*

## Glossary
| ID | Term | Candidate meanings | Resolved meaning | Q-n |
|---|---|---|---|---|
| GL-1 | `notoc` | 1. A CSS class name that signals the TOC extension to exclude the heading.<br>2. An extension option name.<br>3. A custom attribute marker. | Meaning 1 (CSS class name on the heading element) | — |

## Confirmation Records
*(None)*
