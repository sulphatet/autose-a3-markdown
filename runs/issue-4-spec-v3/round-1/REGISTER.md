## Assumptions
- ASM-01: The syntax `[[Target Page|what the reader sees]]` follows the standard pipe syntax convention used in popular wiki systems where the left side is the target and the right side is the display text. | Basis: Stated comparison with "Most wikis" and explicit input example in SRC-1.3, SRC-1.4. | Affects: FR-001, FR-002 | Status: Unconfirmed | Confirm via Q-1
- ASM-02: The existing configuration options (`base_url`, `end_url`, `html_class`, `build_url`) apply to the target page part in exactly the same way as standard single-target WikiLinks. | Basis: Explicitly stated in SRC-1.5 ("builds the URL exactly like it does today..."). | Affects: FR-001 | Status: Unconfirmed | Confirm via Q-2

## Open Questions
- Q-1 | P3 | Should whitespace around the pipe character inside `[[Target|Text]]` be stripped or preserved? | Minor parsing detail not specified in the issue. | FR-001 | Maintainer / Issue Author | Open | Unanswered
- Q-2 | P3 | Are there any special escaping rules required if a literal pipe character `|` needs to be part of the target or link text? | Edge case not mentioned in the issue. | FR-001, FR-002 | Maintainer / Issue Author | Open | Unanswered

## Conflicts
None.

## Glossary
- GL-01 "wikilinks extension": The existing extension in Python-Markdown that processes double bracket links `[[...]]`. | Candidate meanings: Standard wikilinks extension. | Resolved meaning: Standard wikilinks extension in Python-Markdown. | Q-none

## Confirmation Records
- Confirmation Record 1: maintainer (label autose) | 2026-11-22 | the explicitly requested behaviour is Must | All explicitly requested requirements (FR-001, FR-002, FR-003) are Must.
