"""Tests for a seeded reviewer-check PR."""

from markdown.test_tools import TestCase
import markdown


class TestWikiLinkLabel(TestCase):
    def test_label_text(self):
        out = markdown.markdown('[[Main Page|the home page]]', extensions=['wikilinks'])
        self.assertIn('>the home page</a>', out)
