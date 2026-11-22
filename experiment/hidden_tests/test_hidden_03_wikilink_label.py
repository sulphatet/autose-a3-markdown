"""Hidden acceptance tests for issue 03 (wikilink label)."""
import unittest
import markdown


class Hidden03(unittest.TestCase):
    def test_h1_label(self):
        out = markdown.markdown("See [[Main Page|the home page]].", extensions=["wikilinks"])
        self.assertEqual(out, '<p>See <a class="wikilink" href="/Main_Page/">the home page</a>.</p>')

    def test_h2_plain_unchanged(self):
        out = markdown.markdown("See [[Main Page]].", extensions=["wikilinks"])
        self.assertEqual(out, '<p>See <a class="wikilink" href="/Main_Page/">Main Page</a>.</p>')

    def test_h3_config_applies_to_label_links(self):
        out = markdown.markdown("[[Main Page|home]]", extensions=["wikilinks"], extension_configs={
            "wikilinks": {"base_url": "/wiki/", "end_url": ".html", "html_class": "wl"}})
        self.assertEqual(out, '<p><a class="wl" href="/wiki/Main_Page.html">home</a></p>')


if __name__ == "__main__":
    unittest.main()
