---
type: bug
title: "Footnote definition indented inside another footnote disappears"
upstream: related to Python-Markdown/markdown#1681 (reproduced at 3f2c551; text written independently)
---

When a footnote definition is nested (indented) inside the body of another footnote, it vanishes from the output without any warning.

```python
import markdown

text = """\
Main[^1].

[^1]: First

    [^2]: Second
"""
print(markdown.markdown(text, extensions=["footnotes"]))
```

Only footnote 1 is rendered; the text "Second" is gone and there is no `fn:2` item in the list. If footnote 1 references `[^2]`, I get a link to `#fn:2` that goes nowhere.

If I write `[^2]: Second` without the indentation it works, so I think only the indented form is affected. I'd expect the nested definition to show up as its own footnote, just like the non-indented one.
