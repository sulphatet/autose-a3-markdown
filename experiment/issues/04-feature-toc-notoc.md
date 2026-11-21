---
type: feature
title: "toc: let me leave a heading out of the table of contents"
---

I have a few headings ("Changelog", "Footnotes"…) that I don't want in the generated table of contents, but I still want them on the page with their normal id.

Could the `toc` extension skip any heading that has the class `notoc`? With `attr_list` that would look like:

```markdown
[TOC]

# Guide

## Install

## Changelog {.notoc}

## Usage
```

The TOC should list Guide, Install and Usage, but not Changelog. The Changelog heading itself should still be rendered as `<h2 class="notoc" id="changelog">`. It would be nice if `md.toc_tokens` left it out too, so other tools see the same list.
