# Seeded reviewer-check PRs

Five pull requests with known ground truth: four have planted defects and one is correct. They test whether the reviewer agent (ADR-008) catches defects without inventing problems. `labels.csv` holds the ground truth. Each `.diff` is the PR's change against `main`.

The reviewer is triggered with a comment on the PR. It reads only the issue named in the branch (`autose-seed/issue-<n>-<tag>`) and the diff:

- `/autose`: default reviewer (`gemini-3.1-flash-lite`, a different model from the builders)
- `/autose variant=same-model`: the builders' model (`gemini-3.5-flash-lite`)

These PRs are never merged.
