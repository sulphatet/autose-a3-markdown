from markdown.test_tools import TestCase
import markdown


class TestAutoSeIssue2(TestCase):
    def test_AC_FR_001_1(self):
        src = "``` { .python linenums }\nprint(1)\n```"
        self.assertMarkdownRenders(
            src,
            "<pre><code class=\"language-python\">print(1)\n</code></pre>",
            extensions=["fenced_code", "attr_list"]
        )

    def test_AC_FR_001_2(self):
        src = "``` { .python linenums=true }\nprint(1)\n```"
        self.assertMarkdownRenders(
            src,
            "<pre><code class=\"language-python\">print(1)\n</code></pre>",
            extensions=["fenced_code", "attr_list"]
        )

    def test_AC_FR_001_3(self):
        src = "``` { .python guess_lang }\nprint(1)\n```"
        self.assertMarkdownRenders(
            src,
            "<pre><code class=\"language-python\">print(1)\n</code></pre>",
            extensions=["fenced_code", "attr_list"]
        )

    def test_AC_FR_001_4(self):
        src = "``` { .python noclasses }\nprint(1)\n```"
        self.assertMarkdownRenders(
            src,
            "<pre><code class=\"language-python\">print(1)\n</code></pre>",
            extensions=["fenced_code", "attr_list"]
        )

    def test_AC_NFR_COMP_01_1(self):
        src = "``` { .python linenums }\nprint(1)\n```"
        html = markdown.markdown(src, extensions=["fenced_code", "attr_list"])
        self.assertIn('<code class="language-python">', html)
        self.assertNotIn('TypeError', html)
