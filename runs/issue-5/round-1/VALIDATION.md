## Run info
Date: 2026-11-22 | Mode: non-interactive | Tools available: none | Tools used: none
Input sources: SRC-1 (Issue #5)

## Check results
| Check ID | Description | Result | Details / offending IDs |
|---|---|---|---|
| V-C1 | Every Step 5 checklist item is covered, gap->Q, or N/A with reason | PASS | — |
| V-C2 | Every FR and NFR has at least one acceptance criterion (or TBD placeholder) | PASS | — |
| V-C3 | At least one actor exists, and every FR names or implies an actor | PASS | — |
| V-C4 | Every glossary term has a resolved meaning or an open question | PASS | GL-1 has open question Q-1 |
| V-K1 | No two requirements contradict each other | PASS | — |
| V-K2 | Terms are used with one meaning only | PASS | — |
| V-K3 | IDs are unique and follow §3.1; every referenced ID exists | PASS | — |
| V-T1 | Every [S] item cites a SRC-n.s and quotes it | PASS | — |
| V-T2 | Every [I] item links an ASM-n; every [E] links EV-n; [U] links Q/CNF; [C] links confirmation record | PASS | — |
| V-T3 | Every source sentence maps to >= 1 item, or is marked context only | PASS | — |
| V-T4 | No item is tagged [S]/[C] without support (anti-hallucination check) | PASS | — |
| V-F1 | No requirement asks for something impossible or self-contradictory | PASS | — |
| V-F2 | Every requirement depending on external system/regulation has DEP or EV | PASS | — |
| V-F3 | Every stated constraint is compatible with every Must requirement | PASS | — |
| V-Q1 | No unquantified weasel words in requirements | PASS | — |
| V-Q2 | Every NFR has a metric, threshold, and measurement method | N/A | No NFRs defined |
| V-Q3 | Every requirement is atomic | PASS | — |
| V-Q4 | Every acceptance criterion is observable pass/fail by a tester without asking author | PASS | — |

## Readiness summary
- Total FR + NFR: 3
- Ready: 0
- Needs-Clarification: 3 (FR-001, FR-002, FR-003 depend on open questions / non-interactive mode)
- Blocked: 0
- Deferred: 0
- Percentage Ready: 0%
- Tags: [S]: 3, [C]: 0, [I]: 0, [E]: 0, [U]: 0

## Open P1 questions
- Q-1: Should the class name used to exclude headings from the TOC be configurable, or strictly hardcoded to `notoc` as requested?

## Verdict: NOT READY — CLARIFICATION REQUIRED

## Self-check of boundaries (B1-B5)
- B1 (No invention): PASS
- B2 (No silent promotion): PASS
- B3 (No silent conflict resolution): PASS
- B4 (Domain-agnostic): PASS
- B5 (Honesty over completeness): PASS
