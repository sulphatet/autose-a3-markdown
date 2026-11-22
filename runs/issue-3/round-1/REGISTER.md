## Assumptions
| ID | Assumption | Basis | Affects | Status | Confirm via Q-n |
|---|---|---|---|---|---|
| ASM-1 | The nested footnote definition should be rendered as its own footnote in the footnote list, rather than being parsed as nested/contained block content within the parent footnote or swallowed silently. | Inferred from issue text ("I'd expect the nested definition to show up as its own footnote, just like the non-indented one") | FR-002 | Unconfirmed | Q-1 |

## Open Questions
| ID | Priority P1-3 | Question | Why it matters | Blocks | Ask whom | Status | Answer |
|---|---|---|---|---|---|---|---|
| Q-1 | P1 | Should a footnote definition nested (indented) inside another footnote be hoisted and rendered as a top-level footnote in the footnotes list, or should it be processed differently? | Determines whether nested footnote definitions should appear in the footnotes list or how they are structured in output HTML. | FR-002 | Maintainer / Issue Reporter | Open | |

## Conflicts
*(None)*

## Glossary
| ID | Term | Candidate meanings | Resolved meaning | Q-n |
|---|---|---|---|---|
| GL-1 | nested (indented) footnote definition | 1. A footnote definition placed within the indented block content of another footnote.<br>2. A sub-footnote belonging exclusively to the parent footnote. | Unresolved | Q-1 |

## Confirmation Records
*(None)*
