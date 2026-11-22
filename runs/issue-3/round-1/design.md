## Summary
When a footnote definition is nested (indented) inside the body of another footnote, the `FootnoteBlockProcessor` consumes the nested definition lines as part of the outer footnote's body text rather than recognizing and extracting them as separate footnote definitions. This design ensures that nested footnote definitions are correctly parsed, extracted, and registered as independent footnotes.

## Approach
How the change works, where it sits in the pipeline (preprocessor, block processor, tree processor, inline pattern, postprocessor, extension), and why this place. Mention one alternative you rejected.

When `FootnoteBlockProcessor` processes a footnote definition and collects tabbed or continuation blocks (`detectTabbed` or remaining block content), it currently assumes all indented lines belong entirely to the body of the current footnote. If an indented line contains another footnote definition (`[^2]: Second`), `detectTabbed` or the block parser needs to stop or split at the nested footnote definition, extract it, set it via `self.footnotes.setFootnote(id, text)`, and re-insert any remaining content back into `blocks` so that subsequent block processors (or the footnote block processor itself) can process it.

Specifically, in `FootnoteBlockProcessor.detectTabbed` (and when parsing the initial block), when inspecting indented blocks or remaining lines, we check if there is a match for `self.RE`. If found, we split the block before the match (treating the content before as part of the current footnote body) and push the matched footnote definition block back into `blocks` so it is parsed as its own footnote.

Alternative rejected: Recursively parsing footnote bodies during tree processing or postprocessing. This was rejected because footnote definitions are extracted during block parsing before the element tree is built, so block processors are the correct and natural place to parse and separate footnote definitions.

## Change list

| file | symbol | change | ACs covered |
| --- | --- | --- | --- |
| markdown/extensions/footnotes.py | FootnoteBlockProcessor.detectTabbed | modify: check for nested footnote definitions in indented blocks and split at them | AC-FR-001-1, AC-FR-002-1 |
| markdown/extensions/footnotes.py | FootnoteBlockProcessor.run | modify: ensure single-block nested footnotes are also correctly handled if applicable | AC-FR-001-1, AC-FR-002-1 |
| docs/changelog.md | Unreleased | modify: add a changelog entry | — |

## Test plan
For each AC: the Markdown input, the extensions and options, and the exact expected output or behaviour a test should assert.

- **AC-FR-001-1 & AC-FR-002-1**:
  - Input:
    ```markdown
    Main[^1].

    [^1]: First

        [^2]: Second
    ```
  - Extensions: `["footnotes"]`
  - Expected behavior / output: No exception raised, `"Second"` does not vanish silently, and the output includes both footnote 1 and footnote 2 rendered in the footnote list (`<li id="fn:2">`).

## Risks
What existing behaviour could break, and which existing tests cover it.
- Existing complex footnotes (e.g. multi-paragraph footnotes or blockquotes inside footnotes that might resemble footnote definitions or start with similar syntax) could be incorrectly split if not careful. Existing footnote tests (`tests/extensions/extra/footnote.txt` etc.) will verify that standard multi-paragraph and blockquote footnotes continue to render correctly.


---
## Pipeline check (stage 2, `checks.check_design`)

**Check: PASS**

- `markdown/extensions/footnotes.py` :: `FootnoteBlockProcessor.detectTabbed` found
- `markdown/extensions/footnotes.py` :: `FootnoteBlockProcessor.run` found
- `docs/changelog.md` :: `Unreleased` found
