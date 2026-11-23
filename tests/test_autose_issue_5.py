from markdown.test_tools import TestCase
import markdown


class TestAutoseIssue5(TestCase):
    maxDiff = None

    def test_AC_FR_001_1(self):
        self.assertMarkdownRenders(
            self.dedent(
                '''
                [TOC]

                # Guide

                ## Changelog {.notoc}
                '''
            ),
            '<div class="toc">\n'
            '<ul>\n'
            '<li><a href="#guide">Guide</a></li>\n'
            '</ul>\n'
            '</div>\n'
            '<h1 id="guide">Guide</h1>\n'
            '<h2 class="notoc" id="changelog">Changelog</h2>',
            extensions=['toc', 'attr_list']
        )

    def test_AC_FR_002_1(self):
        self.assertMarkdownRenders(
            self.dedent(
                '''
                ## Changelog {.notoc}
                '''
            ),
            '<h2 class="notoc" id="changelog">Changelog</h2>',
            extensions=['toc', 'attr_list']
        )

    def test_AC_FR_003_1(self):
        md = markdown.Markdown(extensions=['toc', 'attr_list'])
        md.convert('## Changelog {.notoc}')
        self.assertEqual(md.toc_tokens, [])
