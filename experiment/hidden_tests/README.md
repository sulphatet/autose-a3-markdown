# Hidden tests

These tests were kept outside the repository during all experiment runs, so no agent could read them. They were copied here afterwards for grading.

| File | Issue | Tests |
| --- | --- | --- |
| `test_hidden_01_fenced_bool_attrs.py` | #2 | 4 |
| `test_hidden_02_nested_footnote.py` | #3 | 3 |
| `test_hidden_03_wikilink_label.py` | #4 | 3 |
| `test_hidden_04_toc_notoc.py` | #5 | 3 |
| `test_hidden_05_vague_toc.py` | #6 (vague) | 2; they pass on the base commit, because a vague issue has no single correct change |

Run against a PR branch: copy the file into `tests/` and run `python -m unittest tests.<module>`. Results are in `results/results.csv`.
