## Summary
The `wikilinks` extension is updated to support pipe-separated link text syntax (`[[Target Page|what the reader sees]]`), while preserving existing URL building rules and backward compatibility for plain `[[Main Page]]` wikilinks.

## Approach
We update the regex pattern in `WikiLinkExtension.extendMarkdown()` and the matching logic in `WikiLinksInlineProcessor.handleMatch()` within `markdown/extensions/wikilinks.py`. 
Specifically:
1. The regex `WIKILINK_RE` is updated from `r'\[\[([\w0-9_ -]+)\]\]'` to something that supports an optional pipe and link text, e.g., `r'\[\[([\w0-9_ -]+)(?:\|([^\]]+))?\]\]'`. Alternatively, or to be robust against characters allowed in target pages and link text, `r'\[\[([^\]\|]+)(?:\|([^\]]+))?\]\]'` or similar. Wait, let's check what characters are allowed currently: `[\w0-9_ -]+`. If target page can contain those or any character except `|` and `]`, let's see: `[\w0-9_ -]+` or `[^\]\|]+`. If we use `r'\[\[([\w0-9_ -]+)(?:\|([^\]]+))?\]\]'`, group 1 captures the target page (retaining existing behavior for the URL target and default link text) and group 2 (if present) captures the link text. Wait, what if someone puts spaces or other characters in link text or target page? Let's check existing `WIKILINK_RE`: `r'\[\[([\w0-9_ -]+)\]\]'`. For the target page part, keeping `[\w0-9_ -]+` (or `[^\]\|]+`) maintains exact backward compatibility for URL building. If group 2 is present and stripped, it becomes the text content of the anchor tag (`a.text = link_text.strip()`). If group 2 is absent, the target page label is used as the link text (just like before).
2. We place this change in `markdown/extensions/wikilinks.py`, which is the dedicated module for the `wikilinks` extension.
3. Alternative rejected: Implementing a separate inline pattern or preprocessor. Extending the existing `WikiLinksInlineProcessor` keeps the implementation simple, performant, and tightly coupled with existing configuration and metadata handling.

## Change list

| file | symbol | change | ACs covered |
| --- | --- | --- | --- |
| markdown/extensions/wikilinks.py | WikiLinkExtension.extendMarkdown | modify: update WIKILINK_RE regex to capture optional pipe and link text | AC-FR-001-1, AC-FR-002-1, AC-FR-003-1 |
| markdown/extensions/wikilinks.py | WikiLinksInlineProcessor.handleMatch | modify: use captured link text if present, falling back to target label | AC-FR-001-1, AC-FR-002-1, AC-FR-003-1 |
| docs/changelog.md | Unreleased | modify: add changelog entry for wikilinks pipe syntax support | — |

## Test plan
- AC-FR-001-1 / AC-FR-003-1:
  - Input: `See [[Main Page|the home page]].`
  - Extensions: `["wikilinks"]`
  - Expected output: `<p>See <a class="wikilink" href="/Main_Page/">the home page</a>.</p>`
- AC-FR-002-1:
  - Input: `See [[Main Page]].`
  - Extensions: `["wikilinks"]`
  - Expected output: `<p>See <a class="wikilink" href="/Main_Page/">Main Page</a>.</p>`

## Risks
- Risk of breaking existing wikilinks if regex changes incorrectly. Covered by existing tests (`testBasicWikilinks`, `testWikilinkWhitespace`, `testSimpleSettings`, `testComplexSettings`, `testWikilinksMetaData`, `testURLCallback`).


---
## Pipeline check (stage 2, `checks.check_design`)

**Check: PASS**

- `markdown/extensions/wikilinks.py` :: `WikiLinkExtension.extendMarkdown` found
- `markdown/extensions/wikilinks.py` :: `WikiLinksInlineProcessor.handleMatch` found
- `docs/changelog.md` :: `Unreleased` found
