## autose review (round manual)

**Verdict: request changes** (kind: `code`)

The pull request implements support for `[[Target|text]]` in wikilinks, but has a critical bug: `label` passed to `build_url` includes the `|text` part (e.g. `Main Page|the home page`), leading to an incorrect URL. `label` needs to be split before calling `build_url`.

### What the issue asks for

| requirement | status | evidence |
| --- | --- | --- |
| The part before | builds the URL exactly like it does today (same base_url, end_url, html_class and build_url handling) | not_met | markdown/extensions/wikilinks.py:78 |
| The part after | is the text of the link | met | markdown/extensions/wikilinks.py:81 |
| Plain [[Main Page]] keeps working exactly as now | met | tests/test_seed_issue_4_wrong_url.py:10 |

### Findings

- **blocker** `markdown/extensions/wikilinks.py:78`: When using `[[Target Page|the home page]]`, `label = m.group(1).strip()` is passed to `build_url`, meaning `build_url` receives `'Main Page|the home page'` instead of just `'Main Page'`, resulting in an incorrect URL containing the pipe and label text.
  - evidence: markdown/extensions/wikilinks.py:78

---
Reviewer model `gemini-3.5-flash-lite`, separate job, read-only. It saw only the issue, the diff and the repository at the PR head. A person decides whether to merge.