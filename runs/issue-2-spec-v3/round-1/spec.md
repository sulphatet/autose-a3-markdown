# Python-Markdown — Software Requirements Specification
Version: v0.1 | Date: 2026-11-22 | Mode: non-interactive | Status: Draft
> Stakeholder confirmation: obtained from maintainer (label autose) — the explicitly requested behaviour is Must.

## 1. Purpose and Scope
### In-scope
- Preventing exceptions (`TypeError: cannot serialize None` or similar serialization errors) when rendering fenced code blocks with attribute lists containing boolean/non-string options like `linenums`, `guess_lang`, or `noclasses` while the `codehilite` extension is disabled.
- Rendering the code block successfully with its appropriate language class (e.g., `class="language-python"`) even when such attributes are present.

### Out-of-scope
- Requiring `codehilite` to be enabled for fenced code block attribute parsing.

### Scope unknown
- Whether unsupported attributes should be rendered into the output HTML or silently stripped.

## 2. Actors
| ID | Actor | Description | Tag | Source/Link |
|---|---|---|---|---|
| ACT-1 | User / Developer | Uses Python-Markdown with `fenced_code` and `attr_list` extensions enabled without `codehilite`. | [S] | SRC-1.1, SRC-1.2 |

## 3. Functional Requirements
| ID | Requirement (EARS) | Tag | Source / Link | Priority | Readiness |
|---|---|---|---|---|---|
| FR-001 | When fenced code blocks are converted using `fenced_code` and `attr_list` extensions without `codehilite`, if attributes such as `linenums`, `guess_lang`, or `noclasses` are present in the attribute list, the system shall render the code block successfully without raising a serialization exception. | [S] | SRC-1.2, SRC-1.4, SRC-1.5, SRC-1.6 | Must | Ready |

**FR-001 acceptance criteria:**
- AC-FR-001-1: Given Markdown input `src = "``` { .python linenums }\nprint(1)\n```"`, when `markdown.markdown(src, extensions=["fenced_code", "attr_list"])` is executed, then no exception is raised and the output contains `<code class="language-python">`.
- AC-FR-001-2: Given Markdown input `src = "``` { .python linenums=true }\nprint(1)\n```"`, when `markdown.markdown(src, extensions=["fenced_code", "attr_list"])` is executed, then no exception is raised and the output contains `<code class="language-python">`.
- AC-FR-001-3: Given Markdown input `src = "``` { .python guess_lang }\nprint(1)\n```"`, when `markdown.markdown(src, extensions=["fenced_code", "attr_list"])` is executed, then no exception is raised and the output contains `<code class="language-python">`.
- AC-FR-001-4: Given Markdown input `src = "``` { .python noclasses }\nprint(1)\n```"`, when `markdown.markdown(src, extensions=["fenced_code", "attr_list"])` is executed, then no exception is raised and the output contains `<code class="language-python">`.

## 4. Non-Functional Requirements
*(None)*

## 5. Constraints
*(None)*

## 6. Dependencies
*(None)*

## 7. Risks
*(None)*

## 8. Traceability Matrix
- SRC-1.1 → ACT-1
- SRC-1.2 → FR-001, AC-FR-001-1
- SRC-1.4 → FR-001, AC-FR-001-2
- SRC-1.5 → FR-001, AC-FR-001-3, AC-FR-001-4
- SRC-1.6 → FR-001

## 9. Change Log
- v0.1 (2026-11-22): Initial draft from issue #954c232a.

## Appendix A. Source Register
- SRC-1.1: Hi! I have `fenced_code` and `attr_list` turned on, but not `codehilite` (I highlight on the client side).
- SRC-1.2: If I put `linenums` in the braces of a fenced block, the whole conversion blows up:
- SRC-1.3: `TypeError: cannot serialize None (type NoneType)`
- SRC-1.4: `linenums=true` gives `cannot serialize True (type bool)`, and `guess_lang` / `noclasses` crash the same way.
- SRC-1.5: Normal attributes like `data-x="1"` are fine, and with `codehilite` enabled everything works.
- SRC-1.6: I don't really mind whether those options end up in the HTML or are dropped, but I'd expect the code block to render (with its `language-python` class) instead of an exception.
- SRC-1.7: Python 3.12, Markdown 3.11.2.


---
## Pipeline check (stage 1, `checks.check_spec`)

**Check: PASS**

- A1 skill verdict is `READY FOR IMPLEMENTATION`
- V-Q4 is PASS
- 1 Ready requirement(s), 4 testable acceptance criteria: AC-FR-001-1, AC-FR-001-2, AC-FR-001-3, AC-FR-001-4
