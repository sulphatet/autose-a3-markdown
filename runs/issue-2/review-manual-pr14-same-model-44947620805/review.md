## autose review (round manual)

**Verdict: approve**

The pull request correctly fixes the issue where `fenced_code` crashes when boolean/valueless options or options with `None` values (like `linenums`, `guess_lang`, `noclasses`) are present in a fenced code block attribute list without `codehilite`. By filtering out `None` values (`v is not None`), these options are omitted from the output HTML tag attributes rather than crashing during serialization. Appropriate tests are added and pass successfully.

### What the issue asks for

| requirement | status | evidence |
| --- | --- | --- |
| Fix fenced_code crashing when options such as linenums are in an attribute list without codehilite. | met | docs/changelog.md:19 and markdown/extensions/fenced_code.py:161 |

### Findings

None.

---
Reviewer model `gemini-3.5-flash-lite`, separate job, read-only. It saw only the issue, the diff and the repository at the PR head. A person decides whether to merge.