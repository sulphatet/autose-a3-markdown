## autose review (round 1)

**Verdict: approve**

The pull request correctly implements the requested feature to exclude headings with the `notoc` class from the table of contents and `md.toc_tokens`, while preserving the heading's rendering in the document. Tests verify the functionality.

### What the issue asks for

| requirement | status | evidence |
| --- | --- | --- |
| The `toc` extension should skip any heading that has the class `notoc`. | met | markdown/extensions/toc.py:414-416 |
| The `md.toc_tokens` should leave out headings with the `notoc` class. | met | tests/test_autose_issue_5.py:39-43 |
| The heading itself should still be rendered with its normal id and class. | met | tests/test_autose_issue_5.py:10-25 |

### Findings

None.

---
Reviewer model `gemini-3.1-flash-lite`, separate job, read-only. It saw only the issue, the diff and the repository at the PR head. A person decides whether to merge.