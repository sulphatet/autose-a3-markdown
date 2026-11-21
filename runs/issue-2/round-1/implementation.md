# Implementation, attempt 5

Implementer summary: Fixed `TypeError` crash in fenced_code when codehilite is disabled and attr_list is enabled with boolean or config attributes like linenums, guess_lang, or noclasses by filtering out None, bool, and list values when formatting attribute key-value pairs.

## Pipeline check (stage 3, `checks.check_build`)

**Check: PASS**

- changed files: ['docs/changelog.md', 'markdown/extensions/fenced_code.py', 'tests/test_autose_issue_2.py']
- `pip install -e .` passed
- `import + smoke call` passed
- `flake8 markdown`: no new errors (4 pre-existing on the base commit ignored)
