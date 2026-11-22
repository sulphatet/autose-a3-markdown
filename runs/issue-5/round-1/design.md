## Summary
The `toc` extension is updated to skip any heading whose `class` attribute includes `notoc` (e.g. `class="notoc"` or `class="foo notoc bar"`), excluding it from the generated table of contents (`md.toc` and `md.toc_tokens`) while leaving the heading itself rendered normally on the page with its assigned id and classes.

## Approach
In `markdown/extensions/toc.py`, within `TocTreeprocessor.run`, when iterating over elements and processing matching header tags, we check whether the heading element has a `class` attribute containing `notoc` as a whitespace-separated token. If it contains `notoc`, we still ensure it receives a unique id (if not already present), add any anchor/permalink if configured, but skip appending it to `toc_tokens` (and thus it won't appear in the generated table of contents).
This fits naturally into `TocTreeprocessor.run` because `TocTreeprocessor` runs after `attr_list` (priority 5 vs `attr_list`'s priority 8), meaning `attr_list` has already populated `el.attrib['class']` when processing header attributes like `{.notoc}`.
An alternative approach of intercepting or filtering earlier in preprocessors or block processors was rejected because header IDs and attribute lists are fully resolved during the tree processing stage.

## Change list

| file | symbol | change | ACs covered |
| --- | --- | --- | --- |
| markdown/extensions/toc.py | TocTreeprocessor.run | modify: skip headings containing the `notoc` class from `toc_tokens` | AC-FR-001-1, AC-FR-002-1, AC-FR-003-1 |
| docs/changelog.md | Unreleased | modify: add a changelog entry | — |

## Test plan

- **AC-FR-001-1**:
  - Input: `[TOC]\n\n# Guide\n\n## Changelog {.notoc}`
  - Extensions & Options: `['toc', 'attr_list']`
  - Expected behaviour: The generated HTML contains `<div class="toc">` which lists "Guide" but does not contain "Changelog".

- **AC-FR-002-1**:
  - Input: `## Changelog {.notoc}`
  - Extensions & Options: `['toc', 'attr_list']`
  - Expected behaviour: The generated HTML contains `<h2 class="notoc" id="changelog">Changelog</h2>`.

- **AC-FR-003-1**:
  - Input: `## Changelog {.notoc}`
  - Extensions & Options: `['toc']` (or `['toc', 'attr_list']`)
  - Expected behaviour: `md.toc_tokens` does not include the entry for "Changelog".

## Risks
- Existing documents without `notoc` will have their classes checked (`el.get('class', '').split()`), which has negligible performance impact and does not affect normal headings. Covered by existing tests in `tests/test_syntax/extensions/test_toc.py`.


---
## Pipeline check (stage 2, `checks.check_design`)

**Check: PASS**

- `markdown/extensions/toc.py` :: `TocTreeprocessor.run` found
- `docs/changelog.md` :: `Unreleased` found
