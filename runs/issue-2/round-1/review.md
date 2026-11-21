## autose review (round 1)

**Verdict: approve**

The pull request fixes the reported TypeError by ensuring that only valid, non-boolean, non-list, and non-None attribute values are processed in the `fenced_code` extension when `codehilite` is not used. The provided tests verify the fix and ensure no regressions.

### What the issue asks for

| requirement | status | evidence |
| --- | --- | --- |
| Fix the TypeError crash in fenced_code when attr_list is enabled and codehilite is disabled, upon encountering boolean or configuration attributes. | met | The issue states that fenced_code crashes when `linenums` is in the attribute list and `codehilite` is off. The fix handles this by filtering out these types. |

### Findings

None.

<details><summary>1 finding(s) dropped by code for missing evidence</summary>

- minor: The fix correctly addresses the TypeError by filtering out None, bool, and list types from the attributes, and converting the remaining values to strings before escaping. This prevents the crash when attributes like `linenums` (which might be boolean or None) are passed to `fenced_code` when `codehilite` is disabled.
</details>

---
Reviewer model `gemini-3.1-flash-lite`, separate job, read-only. It saw only the issue, the diff and the repository at the PR head. A person decides whether to merge.