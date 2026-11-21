---
type: feature
title: "WikiLinks: support a different link text, like [[Page|text]]"
---

Most wikis let you write `[[Target Page|what the reader sees]]`. With the `wikilinks` extension that syntax isn't recognised at all; `[[Main Page|the home page]]` comes out as literal text.

What I'd like:

```python
markdown.markdown("See [[Main Page|the home page]].", extensions=["wikilinks"])
# <p>See <a class="wikilink" href="/Main_Page/">the home page</a>.</p>
```

So the part before `|` builds the URL exactly like it does today (same `base_url`, `end_url`, `html_class` and `build_url` handling) and the part after `|` is the text of the link. Plain `[[Main Page]]` should keep working exactly as now.
