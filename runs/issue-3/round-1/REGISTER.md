## Assumptions
| ID | Assumption | Basis | Affects | Status | Confirm via Q-n |
|---|---|---|---|---|---|
| ASM-1 | Nested footnote definitions are intended to be processed as valid footnote definitions regardless of indentation inside another footnote body. | Inferred from SRC-1.6 | FR-001 | Unconfirmed | Q-1 |

## Open Questions
| ID | Priority | Question | Why it matters | Blocks | Ask whom | Status | Answer |
|---|---|---|---|---|---|---|---|
| Q-1 | P1 | Should footnote definitions nested (indented) inside the body of another footnote be parsed and rendered as standalone footnotes? | Determines whether the reported disappearance is a bug requiring a fix or intended behavior. | FR-001 | Maintainer / Author | Open | |

## Conflicts
*(None)*

## Glossary
| ID | Term | Candidate meanings | Resolved meaning | Q-n |
|---|---|---|---|---|---|
| GL-1 | nested (indented) footnote definition | A footnote definition placed within the indentation block of another footnote body | Unresolved | Q-1 |

## Confirmation Records
*(None)*
