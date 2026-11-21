# Implementation, attempt 1

Implementer summary: Add pipe-separated link text syntax support (e.g. [[Target Page|text]]) to the wikilinks extension in markdown/extensions/wikilinks.py and add changelog entry in docs/changelog.md.

## Pipeline check (stage 3, `checks.check_build`)

**Check: PASS**

- changed files: ['docs/changelog.md', 'markdown/extensions/wikilinks.py']
- `pip install -e .` passed
- `import + smoke call` passed
- `flake8 markdown`: no new errors (4 pre-existing on the base commit ignored)
