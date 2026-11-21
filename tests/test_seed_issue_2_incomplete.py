"""Tests for a seeded reviewer-check PR."""

from markdown.test_tools import TestCase
import markdown


class TestFencedBoolAttrs(TestCase):
    def test_linenums_no_crash(self):
        out = markdown.markdown('``` { .python linenums }\nprint(1)\n```', extensions=['fenced_code', 'attr_list'])
        self.assertIn('print(1)', out)
