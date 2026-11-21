"""Tests for a seeded reviewer-check PR."""

from markdown.test_tools import TestCase
import markdown


class TestNoToc(TestCase):
    def test_notoc_not_in_toc(self):
        out = markdown.markdown('[TOC]\n\n# A\n\n## B {.notoc}\n\n## C', extensions=['toc', 'attr_list'])
        self.assertNotIn('href="#b"', out)
        self.assertIn('href="#c"', out)
