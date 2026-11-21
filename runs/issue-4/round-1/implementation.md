# Implementation, attempt 2

Implementer summary: Added support for custom link text syntax `[[Target Page|link text]]` in the wikilinks extension while preserving existing URL building rules and backward compatibility for plain `[[Main Page]]` wikilinks. Updated changelog.

## Pipeline check (stage 3, `checks.check_build`)

**Check: PASS**

- changed files: ['docs/changelog.md', 'markdown/extensions/wikilinks.py']
- `pip install -e .` passed
- `import + smoke call` passed
- `flake8 markdown`: no new errors (4 pre-existing on the base commit ignored)
