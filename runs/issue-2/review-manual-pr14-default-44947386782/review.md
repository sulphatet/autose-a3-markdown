## autose review (round manual)

**Verdict: approve**

The PR fixes the reported crash by ensuring that only valid string attributes are added to the code block when `codehilite` is not enabled. The fix is correct and safe.

### What the issue asks for

| requirement | status | evidence |
| --- | --- | --- |
| The fenced_code extension should not crash when attributes like `linenums` are present in the attribute list, even if `codehilite` is not enabled. | met | The issue is that `linenums` (and other boolean attributes) are parsed into `None` (or other non-string types) by `parseBoolValue` when `attr_list` is used, and then passed to `_escape_attrib_html` which expects a string, causing a crash. The fix in `fenced_code.py` filters out these `None` values. |

### Findings

None.

<details><summary>1 finding(s) dropped by code for missing evidence</summary>

- minor: The fix correctly addresses the issue by filtering out `None` values when generating key-value pairs for the code block attributes, preventing the `TypeError` during serialization.
</details>

---
Reviewer model `gemini-3.1-flash-lite`, separate job, read-only. It saw only the issue, the diff and the repository at the PR head. A person decides whether to merge.