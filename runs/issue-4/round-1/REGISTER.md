## Assumptions
- ASM-01: The Python-Markdown library structure, configuration options (`base_url`, `end_url`, `html_class`, `build_url`), and the existing implementation of the `wikilinks` extension remain the architecture for parsing and rendering links. | Basis: Stated facts about the existing `wikilinks` extension in the issue. | Affects: FR-001, FR-002, FR-003 | Status: Unconfirmed | Confirm via Q-01

## Open Questions
- Q-01 | P3 | Should any edge cases like escaped pipes `\|` or empty link text `[[Page|]]` be supported, and if so, how? | Detail | Affects: FR-001 | Ask whom: Maintainer / Issue reporter | Status: Open | Answer: [unanswered]

## Conflicts
- None

## Glossary
- GL-01 | wikilinks extension | An extension in Python-Markdown that parses `[[Page Name]]` syntax into HTML anchor tags. | Resolved meaning: The existing `wikilinks` extension with the requested addition of pipe syntax `[[Target|Text]]`. | Q-01

## Confirmation Records
- Confirmation Record: who = "maintainer (label autose)", answer = "the explicitly requested behaviour is Must"
