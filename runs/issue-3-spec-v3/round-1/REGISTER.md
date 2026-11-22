## Assumptions   
- ASM-01 | Nested footnote definitions are intended to be processed as separate, top-level footnotes or nested footnotes depending on parser design, but the user explicitly expects "the nested definition to show up as its own footnote, just like the non-indented one" | Derived from SRC-1.12 "I'd expect the nested definition to show up as its own footnote, just like the non-indented one" | FR-001 | Status: Unconfirmed | Confirm via Q-1

## Open Questions 
- Q-1 | Priority P1 | Should an indented footnote definition inside another footnote render as its own separate top-level footnote in the footnotes list, or should it be nested in some other way? | The issue reporter expects it to show up as its own footnote just like the non-indented one (SRC-1.12), but the exact HTML output structure needs clarification | Blocks: FR-001 | Ask whom: Maintainer | Status: Open | Answer: (none)

## Conflicts      
(None)

## Glossary       
- GL-01 | "nested (indented) inside the body of another footnote" | Footnote definition block indented under another footnote definition in Markdown text | Resolved meaning: A footnote definition (`[^2]: ...`) placed with indentation inside the text lines of another footnote definition (`[^1]: ...`) | Q-1

## Confirmation Records 
(None)
