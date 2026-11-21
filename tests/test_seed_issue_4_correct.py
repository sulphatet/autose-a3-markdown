"""Tests for a seeded reviewer-check PR."""

from markdown.test_tools import TestCase


class TestWikiLinkLabel(TestCase):
    def test_label(self):
        self.assertMarkdownRenders('[[Main Page|the home page]]',
                                   '<p><a class="wikilink" href="/Main_Page/">the home page</a></p>',
                                   extensions=['wikilinks'])

    def test_plain(self):
        self.assertMarkdownRenders('[[Main Page]]', '<p><a class="wikilink" href="/Main_Page/">Main Page</a></p>',
                                   extensions=['wikilinks'])
