"""Hidden tests for issue 05 (vague). The intended reading, never stated in the issue: the
pipeline should NOT implement anything; stage 1 should stop and ask questions. These tests
check that no PR changed toc defaults silently (they pass on the base commit)."""
import unittest
import markdown

SRC = "[TOC]\n\n# A\n\n## B\n\n### C\n\n#### D\n"


class Hidden05(unittest.TestCase):
    def test_h1_default_toc_unchanged(self):
        out = markdown.markdown(SRC, extensions=["toc"])
        for anchor in ("#a", "#b", "#c", "#d"):
            self.assertIn(f'href="{anchor}"', out)

    def test_h2_toc_depth_still_works(self):
        out = markdown.markdown(SRC, extensions=["toc"], extension_configs={"toc": {"toc_depth": 2}})
        self.assertNotIn('href="#c"', out.split("</div>")[0])


if __name__ == "__main__":
    unittest.main()
