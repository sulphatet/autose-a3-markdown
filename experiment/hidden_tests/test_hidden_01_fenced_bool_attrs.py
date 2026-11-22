"""Hidden acceptance tests for issue 01 (fenced_code boolean attrs). Kept outside the repo until runs finish."""
import unittest
import markdown

EXT = ["fenced_code", "attr_list"]


class Hidden01(unittest.TestCase):
    def test_h1_linenums_flag_does_not_raise(self):
        out = markdown.markdown("``` { .python linenums }\nprint(1)\n```", extensions=EXT)
        self.assertIn('class="language-python"', out)
        self.assertIn("print(1)", out)

    def test_h2_explicit_bool_values_do_not_raise(self):
        for attr in ("linenums=true", 'linenums="1"', "guess_lang", "noclasses", "use_pygments=false"):
            with self.subTest(attr=attr):
                out = markdown.markdown("``` { .python %s }\nx = 1\n```" % attr, extensions=EXT)
                self.assertIn("<pre><code", out)
                self.assertIn("x = 1", out)

    def test_h3_plain_attrs_unchanged(self):
        out = markdown.markdown('``` { .python data-x="1" }\nx\n```', extensions=EXT)
        self.assertEqual(out, '<pre><code class="language-python" data-x="1">x\n</code></pre>')

    def test_h4_with_codehilite_still_works(self):
        out = markdown.markdown("``` { .python linenums }\nprint(1)\n```",
                                extensions=EXT + ["codehilite"])
        self.assertIn("print(1)", out)


if __name__ == "__main__":
    unittest.main()
