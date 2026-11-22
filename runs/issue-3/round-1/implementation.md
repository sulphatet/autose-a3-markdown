# Implementation, attempt 6

Implementer summary: Fixed footnote definition indentation bug where nested footnotes disappeared without warning, and added release notes entry to docs/changelog.md under [Unreleased].

## Pipeline check (stage 3, `checks.check_build`)

**Check: PASS**

- changed files: ['docs/changelog.md', 'markdown/extensions/footnotes.py', 'tests/test_autose_issue_3.py']
- `pip install -e .` passed
- `import + smoke call` passed
- `flake8 markdown`: no new errors (4 pre-existing on the base commit ignored)
