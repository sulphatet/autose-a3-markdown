"""Hidden acceptance tests for issue 02 (indented nested footnote)."""
import unittest
import markdown


class Hidden02(unittest.TestCase):
    def test_h1_indented_nested_definition_rendered(self):
        text = "Main[^1].\n\n[^1]: First\n\n    [^2]: Second\n"
        out = markdown.markdown(text, extensions=["footnotes"])
        self.assertIn('id="fn:2"', out)
        self.assertIn("Second", out)

    def test_h2_reference_to_nested_definition_has_target(self):
        text = "Main[^1].\n\n[^1]: First [^2]\n\n    [^2]: Second\n"
        out = markdown.markdown(text, extensions=["footnotes"])
        self.assertIn('href="#fn:2"', out)
        self.assertIn('id="fn:2"', out)

    def test_h3_unindented_nested_still_works(self):
        text = "Main[^1].\n\n[^1]: First [^2]\n[^2]: Second\n"
        out = markdown.markdown(text, extensions=["footnotes"])
        self.assertIn('id="fn:1"', out)
        self.assertIn('id="fn:2"', out)


if __name__ == "__main__":
    unittest.main()
