---
type: bug
title: "fenced_code crashes with `linenums` in the attribute list when codehilite is off"
upstream: related to Python-Markdown/markdown#1713 (reproduced at 3f2c551; text written independently)
---

Hi! I have `fenced_code` and `attr_list` turned on, but not `codehilite` (I highlight on the client side). If I put `linenums` in the braces of a fenced block, the whole conversion blows up:

```python
import markdown
src = "``` { .python linenums }\nprint(1)\n```"
markdown.markdown(src, extensions=["fenced_code", "attr_list"])
```

```
TypeError: cannot serialize None (type NoneType)
```

`linenums=true` gives `cannot serialize True (type bool)`, and `guess_lang` / `noclasses` crash the same way. Normal attributes like `data-x="1"` are fine, and with `codehilite` enabled everything works.

I don't really mind whether those options end up in the HTML or are dropped, but I'd expect the code block to render (with its `language-python` class) instead of an exception.

Python 3.12, Markdown 3.11.2.
