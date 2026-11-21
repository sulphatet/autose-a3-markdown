# Implementation, attempt 2

Implementer summary: Resolved fenced_code crash when linenums, guess_lang, noclasses, or other non-string/boolean config options are present in attribute lists with codehilite disabled by filtering non-string config values from kv_pairs in FencedBlockPreprocessor.run. Added changelog entry.

## Pipeline check (stage 3, `checks.check_build`)

**Check: FAIL**

- changed files: ['docs/changelog.md', 'markdown/extensions/fenced_code.py']
- `pip install -e .` passed
- `import + smoke call` passed
- `flake8 markdown` failed (exit 1):

```
markdown/postprocessors.py:90:40: E201 whitespace after '{'
markdown/postprocessors.py:90:57: E202 whitespace before '}'
markdown/postprocessors.py:90:65: E201 whitespace after '{'
markdown/postprocessors.py:90:82: E202 whitespace before '}'

```
