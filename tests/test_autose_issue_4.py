from markdown.test_tools import TestCase


class TestAutoseIssue4(TestCase):
    def test_AC_FR_001_1(self):
        self.assertMarkdownRenders(
            'See [[Main Page|the home page]].',
            '<p>See <a class="wikilink" href="/Main_Page/">the home page</a>.</p>',
            extensions=['wikilinks']
        )

    def test_AC_FR_002_1(self):
        self.assertMarkdownRenders(
            'See [[Main Page]].',
            '<p>See <a class="wikilink" href="/Main_Page/">Main Page</a>.</p>',
            extensions=['wikilinks']
        )

    def test_AC_FR_003_1(self):
        self.assertMarkdownRenders(
            'See [[Main Page|the home page]].',
            '<p>See <a class="wikilink" href="/Main_Page/">the home page</a>.</p>',
            extensions=['wikilinks']
        )
