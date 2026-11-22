"""Hidden acceptance tests for issue 04 (toc notoc class)."""
import unittest
import markdown

SRC = "[TOC]\n\n# Guide\n\n## Install\n\n## Changelog {.notoc}\n\n## Usage\n"


class Hidden04(unittest.TestCase):
    def test_h1_notoc_heading_not_in_toc(self):
        out = markdown.markdown(SRC, extensions=["toc", "attr_list"])
        toc = out.split("</div>")[0]
        self.assertNotIn("Changelog", toc)
        self.assertIn('href="#install"', toc)
        self.assertIn('href="#usage"', toc)

    def test_h2_heading_still_rendered_with_id(self):
        out = markdown.markdown(SRC, extensions=["toc", "attr_list"])
        self.assertIn('<h2 class="notoc" id="changelog">Changelog</h2>', out)

    def test_h3_toc_tokens_skip_it(self):
        md = markdown.Markdown(extensions=["toc", "attr_list"])
        md.convert(SRC)
        names = [c["name"] for c in md.toc_tokens[0]["children"]]
        self.assertEqual(names, ["Install", "Usage"])


if __name__ == "__main__":
    unittest.main()
