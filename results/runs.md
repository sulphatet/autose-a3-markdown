# Runs

Every Actions run, PR and review, with links. Machine-readable version with tokens: [`results.csv`](results.csv). Base: upstream `3f2c551`, plus the workflow commits on `main` at the time of each run (recorded in each run's `state.json` on the `autose-state` branch). Hidden tests: [`experiment/hidden_tests/`](../experiment/hidden_tests/), run by hand on each PR after the run.

## Pipeline runs (default configuration)

| # | Issue | Run | Trigger | Result | PR | Review | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | #2 fenced_code bool attrs | [44941261187](https://github.com/sulphatet/autose-a3-markdown/actions/runs/44941261187) | label | stopped at S3 (token budget) | — | — | Correct fix rejected twice by the lint check (pre-existing flake8 errors on Python 3.12). Led to ADR-013 and ADR-014. 2,005,443 tokens. |
| 2 | #2 | [44942584408](https://github.com/sulphatet/autose-a3-markdown/actions/runs/44942584408) | `/autose` comment (resume) | approved | [#9](https://github.com/sulphatet/autose-a3-markdown/pull/9) | approved, round 1 | S1/S2 reused from run 1 (ADR-004). Hidden tests 4/4. Shallow review: one requirement, evidence restated the issue. |
| 3 | #3 nested footnote | [44943803218](https://github.com/sulphatet/autose-a3-markdown/actions/runs/44943803218) | label | stopped at S1 | — | — | Spec agent raised P1 "is this intended behaviour?" although the issue states the expectation; FR-001 marked Needs-Clarification. Over-strict spec. |
| 4 | #4 wikilink label | [44944052837](https://github.com/sulphatet/autose-a3-markdown/actions/runs/44944052837) | label | stopped at S4 (false) | — | — | **Check bug, not an agent failure:** tests with docstrings were mis-parsed, so "0 tests fail on base" although they did. Fixed in PR #16. S1-S3 passed. |
| 5 | #5 toc notoc | [44944523113](https://github.com/sulphatet/autose-a3-markdown/actions/runs/44944523113) | label | stopped at S1 | — | — | Verdict PARTIALLY READY but all 3 FRs Needs-Clarification (invented P2 "should the class be configurable?"). Code caught the verdict/table mismatch (ADR-007). Over-strict spec. |
| 6 | #6 vague TOC | [44944920851](https://github.com/sulphatet/autose-a3-markdown/actions/runs/44944920851) | label | stopped at S1 (intended) | — | — | NOT READY; P1 question posted on the issue. Correct behaviour for a vague issue. |
| 7 | #4 | [44948076761](https://github.com/sulphatet/autose-a3-markdown/actions/runs/44948076761) | `/autose` comment (resume after parser fix) | approved | [#18](https://github.com/sulphatet/autose-a3-markdown/pull/18) | approved, round 1 | S1/S2 reused; S3 re-ran because S4 had not passed (ADR-004 rule). Hidden tests 3/3. Narrow regex kept, so no regression like seed #13; minor edge: `[[A| ]]` gives an empty link text. |


**Summary:** 2 of the 4 implementable issues (#2, #4) reached an approved PR that passes all hidden tests (7/7). The vague issue (#6) stopped at stage 1 as intended. Under the strict stage 1 check, #3 and #5 never left stage 1 (see E2).

## Seeded reviewer PRs (experiment E1)

| Seed | PR | Label | Variant A (3.1 Flash-Lite) | Variant B (same model) |
| --- | --- | --- | --- | --- |
| issue-4-correct | [#10](https://github.com/sulphatet/autose-a3-markdown/pull/10) | correct | approve ✅ ([run](https://github.com/sulphatet/autose-a3-markdown/actions/runs/44945164670)) | approve ✅ ([run](https://github.com/sulphatet/autose-a3-markdown/actions/runs/44945530897)) |
| issue-4-wrong-url | [#11](https://github.com/sulphatet/autose-a3-markdown/pull/11) | wrong output | approve ❌ missed ([run](https://github.com/sulphatet/autose-a3-markdown/actions/runs/44945768991)) | request_changes ✅ blocker at wikilinks.py:78, kind=code ([run](https://github.com/sulphatet/autose-a3-markdown/actions/runs/44946193137)) |
| issue-5-missing-tokens | [#12](https://github.com/sulphatet/autose-a3-markdown/pull/12) | missing requirement | approve ❌ missed ([run](https://github.com/sulphatet/autose-a3-markdown/actions/runs/44946412728)) | request_changes ✅ major at toc.py:451, kind=code ([run](https://github.com/sulphatet/autose-a3-markdown/actions/runs/44946646270)) |
| issue-4-regression | [#13](https://github.com/sulphatet/autose-a3-markdown/pull/13) | breaks existing | approve ❌ missed ([run](https://github.com/sulphatet/autose-a3-markdown/actions/runs/44946879855)) | approve ❌ missed ([run](https://github.com/sulphatet/autose-a3-markdown/actions/runs/44947166119)) |
| issue-2-incomplete | [#14](https://github.com/sulphatet/autose-a3-markdown/pull/14) | incomplete + weak test | approve ❌ missed ([run](https://github.com/sulphatet/autose-a3-markdown/actions/runs/44947386782)) | approve ❌ missed ([run](https://github.com/sulphatet/autose-a3-markdown/actions/runs/44947620805)) |

**E1 summary:**

| Variant | Defects caught (of 4) | False alarms (of 1 correct) | Routing correct when caught |
| --- | --- | --- | --- |
| A: default, different model (3.1 Flash-Lite) | 0 | 0 | — |
| B: same model as builders (3.5 Flash-Lite) | 2 | 0 | 2/2 |


**Finding:** a negative result for ADR-006. The reviewer on a *different* model caught nothing; the reviewer on the builders' own model caught the two defects that show in the diff itself. Neither caught the regression (#13) or the incomplete fix (#14); catching those needs running inputs, which the reviewer may do (ADR-008) but did not.

## Experiment E2: stage 1 readiness

### Variant B: stricter prompt (spec-v3)

| Issue | v2 (default) S1 | spec-v3 S1 | spec-v3 run | spec-v3 furthest stage | Notes |
| --- | --- | --- | --- | --- | --- |
| #2 | READY | READY (1 FR, 100%) | [45009976703](https://github.com/sulphatet/autose-a3-markdown/actions/runs/45009976703) | stopped S2: model unavailable (503 x6) | infra failure, not a design stop; 705,968 tokens (mostly designer retries) |
| #3 | NOT READY (asked "is it intended?") | NOT READY (0% Ready) | [45010796253](https://github.com/sulphatet/autose-a3-markdown/actions/runs/45010796253) | stopped S1 | P1 Q-1 asks what output structure is wanted, although the issue states it ("show up as its own footnote"); rule 5a did not prevent it; 10,597 tokens |
| #4 | READY | READY | [45011011795](https://github.com/sulphatet/autose-a3-markdown/actions/runs/45011011795) | stopped S5, PR [#19](https://github.com/sulphatet/autose-a3-markdown/pull/19) (CI red) | CI spellcheck failed on the tester's docstrings ("Wikilinks", "ACs") 3 times; routed to implementer, who cannot edit tests; empty CI log fed back. Fixed in PR #21 (ADR-011 amendment). 829,100 tokens |


Stopped after three issues: the prompt change did not remove the false stop on #3.

### Variant A (strict check, ADR-007) vs variant C (lenient check, ADR-015) on the same saved stage 1 outputs

Both checks are code, so they were applied to the *same* spec files saved on the `autose-state` branch. No model variance.

| Issue | Kind | A1 verdict | Strict check (A) | Lenient check (C) |
| --- | --- | --- | --- | --- |
| #2 | bug | READY | pass | pass (4 ACs) |
| #3 | bug | NOT READY | stop | pass (1 AC) |
| #4 | feature | READY | pass | pass (3 ACs) |
| #5 | feature | PARTIALLY READY | stop | pass (2 ACs) |
| #6 | vague | NOT READY | stop (intended) | stop (intended): its ACs are only `<TBD>` |

**Pass rate on clear issues:** A 2/4, C 4/4. **Vague issue let through:** A 0/1, C 0/1.

### Variant C end to end

| Issue | Run | S1 | Outcome | Hidden tests | Tokens | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| #3 | [45012929332](https://github.com/sulphatet/autose-a3-markdown/actions/runs/45012929332) | pass (verdict NOT READY, advisory) | stopped S4 after 3 attempts x 2 designs | 1/3 on final diff (fix not done) | 4,540,387 | correct stop; implementer widened footnote regex to 4 spaces (indented code) and **rewrote docs/changelog.md, deleting 816 lines** - not caught -> changelog guard (PR #22, ADR-007 amendment) |
| #5 | [45015068251](https://github.com/sulphatet/autose-a3-markdown/actions/runs/45015068251) | pass | stopped S3: model unavailable (429) | — | 200,695 | free-tier daily quota exhausted |
| #6 | [45016653708](https://github.com/sulphatet/autose-a3-markdown/actions/runs/45016653708) | — | stopped S1: model unavailable (429) | — | 14,761 | quota; saved-spec check above shows it would stop at S1 |

## Tokens

| Group | Runs | Tokens |
| --- | --- | --- |
| Pipeline (default) | 7 | 4,693,972 |
| E1 reviews | 10 | 515,768 |
| E2 | 6 | 6,301,508 |
| **All** | **23** | **11,511,248** |

About 99% are prompt tokens: every agent turn resends the whole conversation (ADR-014). A review costs 17k-200k tokens; a build that passes first time costs 0.35-1.8M; a build that uses all its retries costs 4.5M.

## Failures of the pipeline itself, found by real runs

| Run | Problem | Fix |
| --- | --- | --- |
| [44941261187](https://github.com/sulphatet/autose-a3-markdown/actions/runs/44941261187) | lint check failed on the unchanged base (Py3.12 flake8) | lint baseline, ADR-013 |
| [44941261187](https://github.com/sulphatet/autose-a3-markdown/actions/runs/44941261187) | 2M token budget too small for retries | 8M, ADR-014 |
| [44944052837](https://github.com/sulphatet/autose-a3-markdown/actions/runs/44944052837) | test parser misread tests with docstrings | PR #16 |
| [44943803218](https://github.com/sulphatet/autose-a3-markdown/actions/runs/44943803218), [44944523113](https://github.com/sulphatet/autose-a3-markdown/actions/runs/44944523113), [45010796253](https://github.com/sulphatet/autose-a3-markdown/actions/runs/45010796253) | strict stage 1 stopped clear issues | lenient check, ADR-015 |
| [45011011795](https://github.com/sulphatet/autose-a3-markdown/actions/runs/45011011795) | test-file spelling failure sent to the implementer; empty CI log | ADR-011 amendment, PR #21 |
| [45012929332](https://github.com/sulphatet/autose-a3-markdown/actions/runs/45012929332) | implementer overwrote the changelog; not caught | changelog guard, ADR-007 amendment, PR #22 |
| 45009976703, 45015068251, 45016653708 | Gemini 503 / 429 quota | none (infrastructure); reported as such (ADR-009) |
