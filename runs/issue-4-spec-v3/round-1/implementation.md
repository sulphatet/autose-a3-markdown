# Implementation, attempt 6

Implementer summary: Implemented support for pipe syntax in the wikilinks extension ([[Target Page|display text]]) alongside existing plain wikilinks behaviour, preserving all configuration options.

## Pipeline check (stage 3, `checks.check_build`)

**Check: PASS**

- changed files: ['docs/changelog.md', 'markdown/extensions/wikilinks.py', 'tests/test_autose_issue_4.py']
- `pip install -e .` passed
- `import + smoke call` passed
- `flake8 markdown`: no new errors (4 pre-existing on the base commit ignored)
