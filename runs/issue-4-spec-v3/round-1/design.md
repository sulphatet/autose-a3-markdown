## Summary
The `wikilinks` extension is updated to support optional display text using pipe syntax (`[[Target Page|display text]]`). When present, the target page part before the pipe builds the URL and the part after the pipe becomes the inner text of the generated anchor tag, while plain `[[Page]]` links retain their existing behavior.

## Approach
We update `markdown/extensions/wikilinks.py` to match wikilink syntax with an optional pipe and display text component (`[[Target Page(|display text)?]]`). In `WikiLinksInlineProcessor.handleMatch`, we capture both groups (target/label and optional display text). If display text is provided, the anchor element's text uses the display text while the `href` attribute is generated from the target label using existing base URL, end URL, class, and custom `build_url` options; if no display text is provided, both the URL and the anchor text use the target label as before.

We considered an alternative approach where the pipe syntax was handled via a separate inline pattern or via post-processing tree transformation; however, updating the regex and handler in `WikiLinksInlineProcessor` directly is simpler, faster, and integrates cleanly with existing matching and configuration handling without adding pipeline overhead.

## Change list

| file | symbol | change | ACs covered |
| --- | --- | --- | --- |
| markdown/extensions/wikilinks.py | WikiLinkExtension.extendMarkdown | modify: update WIKILINK_RE regex to support optional `\|display text` | AC-FR-001-1, AC-FR-002-1 |
| markdown/extensions/wikilinks.py | WikiLinksInlineProcessor.handleMatch | modify: extract target label and optional display text, setting link text accordingly | AC-FR-001-1, AC-FR-002-1 |
| docs/changelog.md | Unreleased | modify: add a changelog entry under Added or Changed | — |

## Test plan

- **AC-FR-001-1**:
  - Markdown input: `See [[Main Page|the home page]].`
  - Extensions & options: `extensions=["wikilinks"]`
  - Expected output: `<p>See <a class="wikilink" href="/Main_Page/">the home page</a>.</p>`

- **AC-FR-002-1**:
  - Markdown input: `See [[Main Page]].`
  - Extensions & options: `extensions=["wikilinks"]`
  - Expected output: `<p>See <a class="wikilink" href="/Main_Page/">Main Page</a>.</p>`

## Risks
- **Regex matching broadness or incorrect grouping**: Could fail if whitespace around the pipe is not handled correctly. We ensure whitespace handling strips outer spaces appropriately or matches cleanly. Existing test suite (`tests/test_extensions.py`) covers all existing plain wikilinks behaviour.


---
## Pipeline check (stage 2, `checks.check_design`)

**Check: PASS**

- `markdown/extensions/wikilinks.py` :: `WikiLinkExtension.extendMarkdown` found
- `markdown/extensions/wikilinks.py` :: `WikiLinksInlineProcessor.handleMatch` found
- `docs/changelog.md` :: `Unreleased` found
