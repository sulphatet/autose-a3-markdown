## Assumptions
| ID | Assumption | Basis | Affects | Status | Confirm via Q-n |
|---|---|---|---|---|---|
| ASM-1 | The crash occurs because fenced_code / attr_list passes attributes intended for codehilite into the output element serialization when codehilite is not enabled. | Inferred from issue description ("fenced_code crashes with `linenums` in the attribute list when codehilite is off"). | FR-001 | Unconfirmed | Q-1 |

## Open Questions
| ID | Priority | Question | Why it matters | Blocks | Ask whom | Status | Answer |
|---|---|---|---|---|---|---|---|
| Q-1 | P3 | Whether unrecognized/codehilite-specific attributes like `linenums`, `guess_lang`, or `noclasses` should be dropped entirely from the rendered HTML element or included in some form when codehilite is disabled. | The reporter states "I don't really mind whether those options end up in the HTML or are dropped, but I'd expect the code block to render... instead of an exception." A definitive choice is needed if strict attribute retention is required. | FR-001 | Maintainer / Reporter | Open | |

## Conflicts
*(None)*

## Glossary
*(None)*

## Confirmation Records
*(None)*
