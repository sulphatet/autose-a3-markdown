# Python-Markdown — Software Requirements Specification
Version: v0.1 | Date: 2026-11-21 | Mode: non-interactive | Status: Draft
> Stakeholder confirmation: obtained from issue text (maintainer label autose -> Must; reporter statement on option handling)

## 1. Purpose and Scope
### In-scope
- Preventing exceptions (`TypeError`) when converting Markdown with `fenced_code` and `attr_list` extensions enabled (and `codehilite` disabled) containing attribute modifiers such as `linenums`, `linenums=true`, `guess_lang`, or `noclasses` in fenced code block attribute lists.
- Rendering the fenced code block (including language classes such as `class="language-python"`) successfully without crashing.

### Out-of-scope
- Changing behavior when `codehilite` is enabled.
- Supporting syntax highlighting features natively without `codehilite`.

### Scope unknown
- None.

## 2. Actors
| ID | Actor | Description | Tag | Source/Link |
|---|---|---|---|---|
| ACT-1 | User / Developer | Invokes `markdown.markdown()` with specific extensions and input Markdown containing fenced code blocks with attribute lists. | [S] | SRC-1.2, SRC-1.3 |

## 3. Functional Requirements
| ID | Requirement (EARS) | Tag | Source / Link | Priority | Readiness |
|---|---|---|---|---|---|
| FR-001 | When `markdown.markdown()` is called with extensions `fenced_code` and `attr_list` (and without `codehilite`), and a fenced code block contains boolean or flag attributes such as `linenums`, `linenums=true`, `guess_lang`, or `noclasses` in its attribute list, the system shall render the fenced code block successfully without raising a `TypeError` exception. | [S][C] | SRC-1.4, SRC-1.6, SRC-1.7 | Must | Ready |

### FR-001 acceptance criteria:
- AC-FR-001-1: Given Python code `src = "``` { .python linenums }\nprint(1)\n```"`, when `markdown.markdown(src, extensions=["fenced_code", "attr_list"])` is executed, then no exception is raised and the output contains `<code class="language-python">`.
- AC-FR-001-2: Given Python code `src = "``` { .python linenums=true }\nprint(1)\n```"`, when `markdown.markdown(src, extensions=["fenced_code", "attr_list"])` is executed, then no exception is raised and the output contains `<code class="language-python">`.
- AC-FR-001-3: Given Python code `src = "``` { .python guess_lang }\nprint(1)\n```"`, when `markdown.markdown(src, extensions=["fenced_code", "attr_list"])` is executed, then no exception is raised and the output contains `<code class="language-python">`.
- AC-FR-001-4: Given Python code `src = "``` { .python noclasses }\nprint(1)\n```"`, when `markdown.markdown(src, extensions=["fenced_code", "attr_list"])` is executed, then no exception is raised and the output contains `<code class="language-python">`.

## 4. Non-Functional Requirements
| ID | Requirement (EARS) | Tag | Source / Link | Priority | Readiness |
|---|---|---|---|---|---|
| NFR-COMP-01 | The system shall remain fully compatible with Python 3.12 and Markdown 3.11.2 environment behavior when processing code blocks. | [S] | SRC-1.11 | unassigned | Ready |

### NFR-COMP-01 acceptance criteria:
- AC-NFR-COMP-01-1: Given Python 3.12 and Markdown 3.11.2, when standard fenced code conversion runs with `attr_list`, execution succeeds without environment-specific serialization errors.

## 5. Constraints
| ID | Constraint | Tag | Source/Link |
|---|---|---|---|
| CON-1 | The solution must resolve the crash specifically when `codehilite` is off and `fenced_code` and `attr_list` are enabled. | [S] | SRC-1.2, SRC-1.3, SRC-1.5 |

## 6. Dependencies
| ID | Dependency | Owner | Status |
|---|---|---|---|
| DEP-1 | Python-Markdown core libraries (`fenced_code`, `attr_list`) | Python-Markdown maintainers | Active |

## 7. Risks
| ID | Risk | L | I | Mitigation / reducing question |
|---|---|---|---|---|
| RSK-1 | Dropping or converting boolean attributes might alter expected output for custom extensions relying on those attributes. | M | L | Handled as acceptable per reporter preference ("I don't really mind whether those options end up in the HTML or are dropped"). |

## 8. Traceability Matrix
| Source / Item | Maps to |
|---|---|
| SRC-1.1 | Issue title |
| SRC-1.2, SRC-1.3 | ACT-1, FR-001, CON-1 |
| SRC-1.4, SRC-1.5 | FR-001, CON-1 |
| SRC-1.6, SRC-1.7 | FR-001 (AC-FR-001-1 to AC-FR-001-4) |
| SRC-1.8, SRC-1.9 | FR-001 |
| SRC-1.10 | RSK-1 |
| SRC-1.11 | NFR-COMP-01 |
| FR-001 | SRC-1.2, SRC-1.3, SRC-1.4, SRC-1.6, SRC-1.7, SRC-1.8, SRC-1.9, Q-1 |
| NFR-COMP-01 | SRC-1.11 |

## 9. Change Log
- v0.1 (2026-11-21): Initial SRS draft derived from ISSUE 79a6d5fb.

## Appendix A. Source Register
- SRC-1.1: `Issue #2: fenced_code crashes with linenums in the attribute list when codehilite is off`
- SRC-1.2: `Hi! I have fenced_code and attr_list turned on, but not codehilite (I highlight on the client side).`
- SRC-1.3: `If I put linenums in the braces of a fenced block, the whole conversion blows up:`
- SRC-1.4: `import markdown`
- SRC-1.5: `src = "``` { .python linenums }\nprint(1)\n```"`
- SRC-1.6: `markdown.markdown(src, extensions=["fenced_code", "attr_list"])`
- SRC-1.7: `TypeError: cannot serialize None (type NoneType)`
- SRC-1.8: `linenums=true gives cannot serialize True (type bool), and guess_lang / noclasses crash the same way.`
- SRC-1.9: `Normal attributes like data-x="1" are fine, and with codehilite enabled everything works.`
- SRC-1.10: `I don't really mind whether those options end up in the HTML or are dropped, but I'd expect the code block to render (with its language-python class) instead of an exception.`
- SRC-1.11: `Python 3.12, Markdown 3.11.2.`


---
## Pipeline check (stage 1, `checks.check_spec`)

**Check: PASS**

- A1 skill verdict is `READY FOR IMPLEMENTATION`
- V-Q4 is PASS
- 2 Ready requirement(s), 5 testable acceptance criteria: AC-FR-001-1, AC-FR-001-2, AC-FR-001-3, AC-FR-001-4, AC-NFR-COMP-01-1
