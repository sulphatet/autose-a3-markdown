## autose review (round manual)

**Verdict: approve**

The pull request correctly implements the requested feature for the wikilinks extension. It allows for an optional link text using the [[Target|text]] syntax, while preserving the existing behavior for [[Target]]. The code changes are correct and the provided tests verify the new functionality.

### What the issue asks for

| requirement | status | evidence |
| --- | --- | --- |
| Support [[Target|text]] syntax in wikilinks. | met | markdown/extensions/wikilinks.py:62,81 |
| Plain [[Target]] should keep working exactly as now. | met | tests/test_seed_issue_4_correct.py:12-14 |

### Findings

None.

<details><summary>1 finding(s) dropped by code for missing evidence</summary>

- minor: The PR correctly implements the requested feature to support [[Target|text]] in the wikilinks extension, while maintaining backward compatibility for [[Target]]. The implementation uses a regex that correctly handles the optional label part, and the logic in handleMatch correctly selects the label or the target page as the link text. The provided tests confirm the functionality.
</details>

---
Reviewer model `gemini-3.1-flash-lite`, separate job, read-only. It saw only the issue, the diff and the repository at the PR head. A person decides whether to merge.