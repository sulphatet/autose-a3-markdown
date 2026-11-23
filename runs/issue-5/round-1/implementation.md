# Implementation, attempt 2

Implementer summary: Updated `toc` extension (`TocTreeprocessor.run`) to skip headings containing the `notoc` class from `toc_tokens`, while preserving normal rendering, IDs, and anchors/permalinks on the page. Added changelog entry.

## Pipeline check (stage 3, `checks.check_build`)

**Check: PASS**

- changed files: ['docs/changelog.md', 'markdown/extensions/toc.py']
- `pip install -e .` passed
- `import + smoke call` passed
- `flake8 markdown`: no new errors (4 pre-existing on the base commit ignored)
