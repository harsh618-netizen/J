import unittest

from markdown_toc_generator import build_toc, extract_headings, slugify


class TestMarkdownTocGenerator(unittest.TestCase):
    def test_extracts_headings_but_skips_fenced_code(self):
        markdown = "# Title\n\n```\n# Not a heading\n```\n## Section\n"
        self.assertEqual(extract_headings(markdown), [(1, "Title"), (2, "Section")])

    def test_duplicate_slugs_get_unique_anchors(self):
        toc = build_toc([(1, "Intro"), (1, "Intro")])
        self.assertIn("(#intro)", toc)
        self.assertIn("(#intro-1)", toc)

    def test_slugify(self):
        self.assertEqual(slugify("Hello, World!"), "hello-world")


if __name__ == "__main__":
    unittest.main()
