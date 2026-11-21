## Assumptions
| ID | Assumption | Basis | Affects | Status | Confirm via Q-n |
|---|---|---|---|---|---|
| ASM-1 | The crash occurs because fenced_code / attr_list attempts to serialize boolean or flag attributes (like linenums, guess_lang, noclasses) into XML element attributes where ElementTree does not accept None or bool values. | Inferred from the exception `TypeError: cannot serialize None (type NoneType)` and `bool` when using `linenums` / `linenums=true` / `guess_lang` / `noclasses` without codehilite. | FR-001 | Unconfirmed | Q-1 |

## Open Questions
| ID | Priority | Question | Why it matters | Blocks | Ask whom | Status | Answer |
|---|---|---|---|---|---|---|---|
| Q-1 | P2 | Should attribute options like `linenums`, `guess_lang`, and `noclasses` be dropped from the output HTML element attributes, or should they be serialized into valid attribute representations when codehilite is off? | Determines the exact HTML output structure when these attributes are supplied without codehilite. | FR-001 | Maintainer / Issue Reporter | Open | (Answered by reporter in issue: "I don't really mind whether those options end up in the HTML or are dropped, but I'd expect the code block to render ... instead of an exception") |

## Conflicts
(None)

## Glossary
| ID | Term | Candidate meanings | Resolved meaning | Q-n |
|---|---|---|---|---|
| GL-1 | attr_list | Python-Markdown extension for adding attributes to elements using curly braces. | Python-Markdown extension for adding attributes to elements using curly braces. | none |
| GL-2 | fenced_code | Python-Markdown extension for parsing fenced code blocks. | Python-Markdown extension for parsing fenced code blocks. | none |
| GL-3 | codehilite | Python-Markdown extension for syntax highlighting code blocks using Pygments. | Python-Markdown extension for syntax highlighting code blocks using Pygments. | none |

## Confirmation Records
| Q-n | Who | When | Answer verbatim | Items updated |
|---|---|---|---|---|
| Q-1 | reporter (via ISSUE 79a6d5fb) | 2026-11-21 | "I don't really mind whether those options end up in the HTML or are dropped, but I'd expect the code block to render (with its language-python class) instead of an exception" | FR-001 |
