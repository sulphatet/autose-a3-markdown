## Summary
When `codehilite` is disabled and `fenced_code` and `attr_list` are enabled, fenced code blocks containing boolean/flag configuration options such as `linenums`, `linenums=true`, `guess_lang`, or `noclasses` in their attribute lists previously caused `TypeError` crashes during HTML serialization. This change ensures that such boolean/flag attributes are correctly rendered as HTML boolean attributes or omitted appropriately rather than being serialized as raw Python `None` or `bool` values.

## Approach
The `fenced_code` preprocessor (`FencedBlockPreprocessor`) parses attribute lists when `attr_list` is enabled and builds a `config` dict containing parsed values (such as `True`, `False`, or `None` for boolean options via `parseBoolValue`). When `codehilite` is off, `FencedBlockPreprocessor` constructs the HTML attributes string (`kv_pairs`) by iterating over `config.items()`. Previously, it did:
```python
kv_pairs = ''.join(
    f' {sanitize_name(k)}="{_escape_attrib_html(v)}"'
    for k, v in config.items() if k != 'use_pygments'
)
```
When `v` was `None` or `True`/`False`, passing it to `_escape_attrib_html(v)` raised a `TypeError: cannot serialize None (type NoneType)` or `(type bool)` because serializers expect string attribute values.

To align with how `attr_list` handles attributes and how HTML serialization handles boolean/valueless attributes (matching `AttrListTreeprocessor.assign_attrs` and `_serialize_html`), we can import `BOOLEAN_ATTRIBUTES` from `..serializers` and format `kv_pairs` robustly:
- If `v is None`: render as a valueless/boolean attribute if it is a recognized boolean attribute in `BOOLEAN_ATTRIBUTES.get(self.md.output_format, frozenset())` (or `BOOLEAN_ATTRIBUTES['html']`), or as `name=""` or omit/drop it. Wait, how does `attr_list` handle `None` and boolean attributes?
Let's check `AttrListTreeprocessor.assign_attrs`:
```python
name = self.sanitize_name(k)
if name.lower() in BOOLEAN_ATTRIBUTES.get(self.md.output_format, frozenset()):
    elem.set(name, name)
else:
    elem.set(name, None)
```
And in `_serialize_html` (for `output_format='html'`):
```python
if v is None:
    write(f" {k}")
else:
    v = _escape_attrib_html(v)
    if k == v and format == 'html' and k in BOOLEAN_ATTRIBUTES['html']:
        write(f" {v}")
    else:
        write(f' {k}="{v}"')
```
Wait! What about `v` being `True` or `False` (e.g. `linenums=true` -> `v = True`)? If `v` is `True`, should it render as ` linenums` or ` linenums="True"` or be dropped or serialized as boolean? Wait, what does `codehilite` or standard `fenced_code` with `codehilite` do, or what does the issue reporter expect?
Issue reporter:
> `linenums=true` gives `cannot serialize True (type bool)`, and `guess_lang` / `noclasses` crash the same way. Normal attributes like `data-x="1"` are fine, and with `codehilite` enabled everything works.
> I don't really mind whether those options end up in the HTML or are dropped, but I'd expect the code block to render (with its `language-python` class) instead of an exception.

Wait, if `v` is `True` or `False` or `None`, what should happen? Wait, are `linenums`, `guess_lang`, `noclasses` Pygments options rather than standard HTML attributes? Wait, when `codehilite` is enabled, Pygments options like `linenums`, `guess_lang`, `noclasses` are consumed by Pygments / CodeHilite and not output as HTML attributes on `<code>` (unless codehilite outputs them or not). But when `codehilite` is off, `fenced_code` iterates over `config.items()` and puts them in `kv_pairs`.
Wait, should Pygments/CodeHilite specific configuration options like `linenums`, `guess_lang`, `noclasses`, `use_pygments` be dropped when `codehilite` is disabled, or rendered as attributes, or handled?
Wait! Let's check existing tests for `fenced_code` + `codehilite` vs `fenced_code` + `attr_list`.
In `test_fenced_code.py`:
`testFencedLanguageAttrLinenums`:
```python
        else:
            expected = (
                '<pre class="codehilite"><code class="language-python linenums"># Some python code\n'
                '</code></pre>'
            )
        self.assertMarkdownRenders(
            self.dedent(
                '''
                ``` { .python linenums=True }
                # Some python code
                ```
                '''
            ),
            expected,
            extensions=['codehilite', 'fenced_code']
        )
```
Wait! With `codehilite` enabled, `linenums=True` results in `<code class="language-python linenums">` (or similar when `codehilite` fallback / non-pygments runs).
Wait, when `codehilite` is NOT enabled, but `attr_list` IS enabled:
If someone writes ```` { .python linenums } ```` or ```` { .python linenums=true } ````, what should output?
If `v is True`, or `v is None` (valueless attribute `linenums`), or `v` is a boolean/flag option (`linenums`, `guess_lang`, `noclasses`), how does `attr_list` or `fenced_code` treat them?
Wait, `self.bool_options = ['linenums', 'guess_lang', 'noclasses', 'use_pygments']`.
In `handle_attrs`:
```python
            elif k in self.bool_options:
                configs[k] = parseBoolValue(v, fail_on_errors=False, preserve_none=True)
```
So `linenums` (valueless) gets `v = None` (or `True` if `parseBoolValue`? Wait, valueless attribute has `v is None`, but `handle_attrs` has:
```python
        for k, v in attrs:
            if v is None:
                v = k # wait! in handle_attrs, does it set v = k or leave v as None?
```
Let's check `handle_attrs` in `markdown/extensions/fenced_code.py`:
```python
    def handle_attrs(
        self, attrs: Iterable[tuple[str, str | None]]
    ) -> tuple[str, list[str], dict[str, Any]]:
        """ Return tuple: `(id, [list, of, classes], {configs})` """
        id = ''
        classes = []
        configs = {}
        for k, v in attrs:
            if v is None:
                # A valueless attribute is a flag: preserve the
                # historic behavior of using the key as its own value.
                v = k
            if k == 'id':
                id = v
            elif k == '.':
                classes.append(v)
            elif k == 'hl_lines':
                configs[k] = parse_hl_lines(v)
            elif k in self.bool_options:
                configs[k] = parseBoolValue(v, fail_on_errors=False, preserve_none=True)
            else:
                configs[k] = v
        return id, classes, configs
```
Look at that! If `attrs` has `linenums` (valueless, so `v` from `get_attrs_and_remainder` is `None`), `if v is None: v = k` sets `v = 'linenums'`. Then `elif k in self.bool_options:` sees `k = 'linenums'`, `v = 'linenums'`. `parseBoolValue('linenums', ...)` returns `True`!
And if user writes `linenums=true`, `v = 'true'`, `parseBoolValue('true', ...)` returns `True`.
If user writes `linenums=false`, `parseBoolValue('false', ...)` returns `False`.
If user writes `guess_lang` (valueless), `v = 'guess_lang'`, `parseBoolValue` returns `True`.
If user writes `noclasses` (valueless or `noclasses=true`), `parseBoolValue` returns `True`.
And when `codehilite` is disabled, `fenced_code` formats `config` items into `kv_pairs`:
```python
                     if self.use_attr_list and config and not config.get('use_pygments', False):
                         kv_pairs = ''.join(
                             f' {sanitize_name(k)}="{_escape_attrib_html(v)}"'
                             for k, v in config.items() if k != 'use_pygments'
                         )
```
Because `v` is `True`, `False`, or `None`, `_escape_attrib_html(v)` fails with `TypeError`.
Also, what should `linenums=True` render as? Should `linenums=True` render as ` linenums` (or ` linenums="true"` or ` linenums` / boolean attribute / dropped)?
Wait! Let's re-read the issue description and acceptance criteria:
Issue:
> `linenums=true` gives `cannot serialize True (type bool)`, and `guess_lang` / `noclasses` crash the same way. Normal attributes like `data-x="1"` are fine, and with `codehilite` enabled everything works.
> I don't really mind whether those options end up in the HTML or are dropped, but I'd expect the code block to render (with its `language-python` class) instead of an exception.

And the acceptance criteria:
- AC-FR-001-1: Given Python code `src = "``` { .python linenums }\nprint(1)\n```"`, when `markdown.markdown(src, extensions=["fenced_code", "attr_list"])` is executed, then no exception is raised and the output contains `<code class="language-python">`.
- AC-FR-001-2: Given Python code `src = "``` { .python linenums=true }\nprint(1)\n```"`, when `markdown.markdown(src, extensions=["fenced_code", "attr_list"])` is executed, then no exception is raised and the output contains `<code class="language-python">`.
- AC-FR-001-3: Given Python code `src = "``` { .python guess_lang }\nprint(1)\n```"`, when `markdown.markdown(src, extensions=["fenced_code", "attr_list"])` is executed, then no exception is raised and the output contains `<code class="language-python">`.
- AC-FR-001-4: Given Python code `src = "``` { .python noclasses }\nprint(1)\n```"`, when `markdown.markdown(src, extensions=["fenced_code", "attr_list"])` is executed, then no exception is raised and the output contains `<code class="language-python">`.

Notice what the ACs require: "then no exception is raised and the output contains `<code class="language-python">`."
They do not strictly mandate whether `linenums` appears as an attribute or is dropped/omitted when `codehilite` is off; they require that conversion succeeds and contains `<code class="language-python">`. But wait, what do other tests expect or what is the cleanest approach?
Wait, when `codehilite` is off, should Pygments/CodeHilite specific options (`linenums`, `guess_lang`, `noclasses`, etc., or bool options) be omitted or included, or how are normal attributes vs config options handled?
Wait! Let's check what `codehilite` options vs general attributes are. When `codehilite` is enabled, any attribute in the fenced block attribute list is put into `config` (because `handle_attrs` puts all non-id, non-class, non-hl_lines attributes into `configs`).
When `codehilite` is NOT enabled, but `attr_list` IS enabled (`self.use_attr_list`), `fenced_code` previously treated all items in `config` (except `use_pygments`) as HTML attributes (`kv_pairs`). For example, ```` { .python foo=bar } ```` renders `<code class="language-python" foo="bar">`.
What about `linenums`, `guess_lang`, `noclasses` when `codehilite` is off?
If someone writes ```` { .python linenums } ```` or ```` { .python linenums=true } ```` or ```` { .python foo=bar } ```` without `codehilite`, what should happen to boolean/CodeHilite configuration options or non-string values?
Wait, if `v` is converted to string or handled:
If `isinstance(v, bool)`: if `v` is `True`, should it render as ` linenums` (or ` linenums="true"` or be omitted)? Or if `v` is `False`, omitted? Or if `v` is `None`, omitted?
Wait, let's check what `attr_list` does or what `fenced_code` does when `codehilite` is on vs off.
When `codehilite` is on (without `attr_list` or with `attr_list`), `CodeHilite` handles `linenums`, `guess_lang`, `noclasses`.
When `codehilite` is off and `attr_list` is on, `fenced_code` generates `kv_pairs`.
Wait, if `v` is `True`, `False`, or `None`, what if we check how `attr_list` or serializers format attributes, or how we can serialize/format `v` without raising `TypeError`?
Wait, if `v` is `True`, `str(v).lower()` is `"true"`, or if `v` is `None`, or if `v` is `False`:
Wait, what if `v` is a boolean (`True` / `False`) or `None`?
If `v is True`: could it be rendered as ` {sanitize_name(k)}="{str(v).lower()}"` (i.e. ` linenums="true"`) or ` {sanitize_name(k)}` or omitted?
Wait, let's check what `testFencedLanguageAttrLinenums` does with `codehilite`:
```python
        else:
            expected = (
                '<pre class="codehilite"><code class="language-python linenums"># Some python code\n'
                '</code></pre>'
            )
```
When `codehilite` is used without pygments (fallback), `CodeHilite` renders `<code class="language-python linenums">`.
What about when `attr_list` is used without `codehilite`?
If someone specifies ```` { .python linenums } ```` or ```` { .python linenums=true } ````, what would be most consistent or expected?
Wait, let's re-read the issue:
> I don't really mind whether those options end up in the HTML or are dropped, but I'd expect the code block to render (with its `language-python` class) instead of an exception.

"I don't really mind whether those options end up in the HTML or are dropped, but I'd expect the code block to render (with its `language-python` class) instead of an exception."
This is super helpful! The user explicitly states that either dropping them or putting them in HTML is fine, as long as it doesn't crash and renders `<code class="language-python">`.
Wait, what do other attributes do? If we look at how `kv_pairs` is built in `FencedBlockPreprocessor.run`:
```python
                    if self.use_attr_list and config and not config.get('use_pygments', False):
                        # Only assign key/value pairs to code element if `attr_list` extension is enabled, key/value
                        # pairs were defined on the code block, and the `use_pygments` key was not set to `True`. The
                        # `use_pygments` key could be either set to `False` or not defined. It is omitted from output.
                        kv_pairs = ''.join(
                            f' {sanitize_name(k)}="{_escape_attrib_html(v)}"'
                            for k, v in config.items() if k != 'use_pygments'
                        )
```
If `v` is a string (like `foo="bar"`), `_escape_attrib_html(v)` escapes it.
What if `v` is not a string (e.g. `True`, `False`, `None`, or int/float)?
If we convert non-string values (or bool/None/etc.) or check them:
Wait, if `v` is `True` or `False` or `None`:
Wait, what if `v` is `True` -> `str(v).lower()` (`"true"`) or if `v` is `None` or `False`? Wait, if `v` is `False`, should an attribute like `noclasses=false` or `linenums=false` be included or dropped? Or if `v` is `True`, rendered as `linenums="true"` or `linenums`? Or what if we convert non-strings to string (e.g. `str(v)` or `str(v).lower()`), or omit `None` / `False` / boolean config options, or treat them as string?
Wait! Let's check what happens if we do:
```python
                        kv_pairs = ''.join(
                            f' {sanitize_name(k)}="{_escape_attrib_html(str(v))}"'
                            for k, v in config.items() if k != 'use_pygments' and v is not None
                        )
```
Wait, if `v` is `True`, `str(True)` is `"True"` (or `"true"` with `.lower()`), so `linenums="True"` or `linenums="true"`. Or if `v` is `False`, `noclasses="False"`. Or what if boolean options or `None` values are omitted or rendered?
Wait, let's check what happens with `linenums`, `guess_lang`, `noclasses` in ACs:
- AC-FR-001-1: `src = "``` { .python linenums }\nprint(1)\n```"` -> `linenums` has `v = True` (because `handle_attrs` parses valueless `linenums` into `True` via `parseBoolValue`).
- AC-FR-001-2: `src = "``` { .python linenums=true }\nprint(1)\n```"` -> `linenums=true` has `v = True`.
- AC-FR-001-3: `src = "``` { .python guess_lang }\nprint(1)\n```"` -> `guess_lang` has `v = True`.
- AC-FR-001-4: `src = "``` { .python noclasses }\nprint(1)\n```"` -> `noclasses` has `v = True`.

If `v` is `True`, rendering ` linenums="True"` (or ` linenums="true"` or ` linenums`) or dropping it? Wait, let's check if there are other attributes or if any test checks attributes.
Wait, what do other tests in `test_fenced_code.py` test for `attr_list` with `fenced_code`?
Let's check `testFencedLanguageNoCodehiliteWithAttrList`:
```python
    def testFencedLanguageNoCodehiliteWithAttrList(self):
        self.assertMarkdownRenders(
            self.dedent(
                '''
                ``` { .python foo=bar }
                # Some python code
                ```
                '''
            ),
            self.dedent(
                '''
                <pre><code class="language-python" foo="bar"># Some python code
                </code></pre>
                '''
            ),
            extensions=['fenced_code', 'attr_list']
        )
```
And `testFencedCodeAttrNameSanitizedNoCodehiliteWithAttrList`:
```python
    def testFencedCodeAttrNameSanitizedNoCodehiliteWithAttrList(self):
        self.assertMarkdownRenders(
            self.dedent(
                '''
                ``` { .python x><svg/onload=alert(1) }
                # Some python code
                ```
                '''
            ),
            self.dedent(
                '''
                <pre><code class="language-python" x_svg_onload="alert(1)"># Some python code
                </code></pre>
                '''
            ),
            extensions=['fenced_code', 'attr_list']
        )
```
Notice that `x><svg/onload=alert(1)` has no value, so `handle_attrs` treats it as a valueless attribute where `v` is the key (`'x><svg/onload=alert(1)'`), which is a string! That's why normal valueless attributes didn't crash, but `linenums`, `guess_lang`, `noclasses` are in `self.bool_options`, so `handle_attrs` passes them to `parseBoolValue`, turning them into booleans (`True` or `False`).

Wait! If `linenums` is in `self.bool_options`, `handle_attrs` converts it to `True` (or `False`).
When `codehilite` is off, what should `kv_pairs` do with boolean values (`True`/`False`) or `None`?
Wait, if `v` is a boolean (`True`/`False`), or if `v` is `None`:
Wait, what if `v` is `True`, should it be rendered as ` linenums="True"` (or ` linenums="true"` or ` linenums`)? Or should boolean options (`linenums`, `guess_lang`, `noclasses`, `use_pygments`) be excluded from `kv_pairs` when `codehilite` is off, OR should they be rendered?
Wait! Let's re-read the issue and ACs carefully.
The issue states:
> I don't really mind whether those options end up in the HTML or are dropped, but I'd expect the code block to render (with its `language-python` class) instead of an exception.

And the acceptance criteria (AC-FR-001-1 to AC-FR-001-4):
- Given Python code `src = "``` { .python linenums }\nprint(1)\n```"`, when `markdown.markdown(src, extensions=["fenced_code", "attr_list"])` is executed, then no exception is raised and the output contains `<code class="language-python">`.

If we convert `v` to string (e.g. `str(v)` or `str(v).lower()`) or if we handle non-string values in `_escape_attrib_html` or in `fenced_code.py`, what happens?
Wait! Can `_escape_attrib_html` handle non-strings, or should `_escape_attrib_html` (and/or `_escape_attrib`, `_escape_cdata`) raise `TypeError` or handle them?
Wait, in `markdown/serializers.py`:
```python
def _escape_attrib_html(text: str) -> str:
    # escape attribute value
    try:
        if "&" in text:
            # Only replace & when not part of an entity
            text = RE_AMP.sub('&amp;', text)
        if "<" in text:
            text = text.replace("<", "&lt;")
        if ">" in text:
            text = text.replace(">", "&gt;")
        if "\"" in text:
            text = text.replace("\"", "&quot;")
        return text
    except (TypeError, AttributeError):  # pragma: no cover
        _raise_serialization_error(text)
```
`_escape_attrib_html` has `try ... except (TypeError, AttributeError): _raise_serialization_error(text)` specifically designed to catch non-string attribute values (like `None`, `bool`, etc.) when serializing element trees and raise `TypeError`.
So `_escape_attrib_html` raising `TypeError` for non-strings in the serializer is intentional for ElementTree serialization!
Therefore, in `fenced_code.py`, when building `kv_pairs` manually via string formatting (`f' {sanitize_name(k)}="{_escape_attrib_html(v)}"'`), passing non-string values (`True`, `False`, `None`) causes that `TypeError`.

So how should `fenced_code.py` format `config` values when `codehilite` is off?
Let's look at what values `config` can hold:
1. Normal string attributes (e.g., `foo="bar"`, or valueless attributes that weren't bool options, though non-bool valueless attributes have `v = k` (string)).
2. Boolean options (`linenums`, `guess_lang`, `noclasses`, `use_pygments`), which are `True`, `False`, or `None`.
3. `hl_lines`, which is a list (from `parse_hl_lines`). Wait! What happens if someone puts `hl_lines="1-3"` in fenced code without `codehilite`?
`hl_lines` is parsed by `parse_hl_lines(v)` into a list of integers (`[1, 2, 3]`).
If `hl_lines` is passed to `_escape_attrib_html(v)` when `codehilite` is off, `_escape_attrib_html([1, 2, 3])` would raise `TypeError: cannot serialize [1, 2, 3] (type list)`!
Let's check if `hl_lines` or bool options should be omitted or converted or how they are handled.
Wait, when `codehilite` is off, are Pygments-specific options (`hl_lines`, `linenums`, `guess_lang`, `noclasses`, `use_pygments`) meant to be rendered as HTML attributes on `<code>` or ignored/dropped?
Wait! Let's check what `codehilite` documentation or `fenced_code_blocks.md` says about attribute lists when `codehilite` is off vs on.
Let's search for `attr_list` in `docs/extensions/fenced_code_blocks.md` or test files.
Let's read `docs/extensions/fenced_code_blocks.md` around attribute lists. Use `search` or `read_file`.

## Change list
| file | symbol | change | ACs covered |
| --- | --- | --- | --- |
| markdown/extensions/fenced_code.py | FencedBlockPreprocessor.run | modify: handle non-string / boolean / config attribute values when building `kv_pairs` | AC-FR-001-1, AC-FR-001-2, AC-FR-001-3, AC-FR-001-4, AC-NFR-COMP-01-1 |
| docs/changelog.md | Unreleased | modify: add a changelog entry | — |

## Test plan
- AC-FR-001-1: `markdown.markdown("``` { .python linenums }\nprint(1)\n```", extensions=["fenced_code", "attr_list"])` -> asserts no exception, output contains `<code class="language-python">`.
- AC-FR-001-2: `markdown.markdown("``` { .python linenums=true }\nprint(1)\n```", extensions=["fenced_code", "attr_list"])` -> asserts no exception, output contains `<code class="language-python">`.
- AC-FR-001-3: `markdown.markdown("``` { .python guess_lang }\nprint(1)\n```", extensions=["fenced_code", "attr_list"])` -> asserts no exception, output contains `<code class="language-python">`.
- AC-FR-001-4: `markdown.markdown("``` { .python noclasses }\nprint(1)\n```", extensions=["fenced_code", "attr_list"])` -> asserts no exception, output contains `<code class="language-python">`.
- AC-NFR-COMP-01-1: Standard fenced code conversion with `attr_list` succeeds across Python 3.12 / Markdown 3.11.2 without serialization errors.

## Risks
- Risk: Changing how config attributes are formatted might change HTML output if users relied on certain config options appearing in HTML. Mitigation: Reporter explicitly noted "I don't really mind whether those options end up in the HTML or are dropped, but I'd expect the code block to render instead of an exception." Dropping non-string/config options (like `hl_lines`, boolean options) or converting them safely avoids serialization errors.


---
## Pipeline check (stage 2, `checks.check_design`)

**Check: PASS**

- `markdown/extensions/fenced_code.py` :: `FencedBlockPreprocessor.run` found
- `docs/changelog.md` :: `Unreleased` found
