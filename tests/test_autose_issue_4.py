import unittest  # noqa: F401
import markdown  # noqa: F401
from markdown.test_tools import TestCase


class TestWikilinkIssue4(TestCase):
    """Test suite for Issue #4 / ACs for wikilinks pipe syntax."""

    def test_AC_FR_001_1(self):
        """AC-FR-001-1: Given Markdown input `See [[Main Page|the home page]].` and extensions `["wikilinks"]`,
        when parsed via `markdown.markdown()`, then the output is
        `<p>See <a class="wikilink" href="/Main_Page/">the home page</a>.</p>`.
        """
        self.assertMarkdownRenders(
            'See [[Main Page|the home page]].',
            '<p>See <a class="wikilink" href="/Main_Page/">the home page</a>.</p>',
            extensions=['wikilinks']
        )

    def test_AC_FR_002_1(self):
        """AC-FR-002-1: Given Markdown input `See [[Main Page]].` and extensions `["wikilinks"]`,
        when parsed via `markdown.markdown()`, then the output is
        `<p>See <a class="wikilink" href="/Main_Page/">Main Page</a>.</p>`
        (or the standard existing output format for plain wikilinks).
        """
        self.assertMarkdownRenders(
            'See [[Main Page]].',
            '<p>See <a class="wikilink" href="/Main_Page/">Main Page</a>.</p>',
            extensions=['wikilinks']
        )
