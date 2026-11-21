## autose review (round manual)

**Verdict: request changes** (kind: `code`)

The pull request implements skipping headings with the class `notoc` for the generated TOC HTML, but leaves them in `md.toc_tokens` because `self.md.toc_tokens = toc_tokens` assigns the unfiltered `toc_tokens` instead of `visible`.

### What the issue asks for

| requirement | status | evidence |
| --- | --- | --- |
| Skip headings with class notoc in table of contents | met | tests/test_seed_issue_5_missing_tokens.py:10 |
| It would be nice if md.toc_tokens left it out too, so other tools see the same list. | not_met | markdown/extensions/toc.py:451 |

### Findings

- **major** `markdown/extensions/toc.py:451`: `self.md.toc_tokens` is assigned `toc_tokens` before filtering out `notoc` headings, so `md.toc_tokens` still includes `notoc` headings unlike the TOC HTML output.
  - evidence: markdown/extensions/toc.py:451

---
Reviewer model `gemini-3.5-flash-lite`, separate job, read-only. It saw only the issue, the diff and the repository at the PR head. A person decides whether to merge.