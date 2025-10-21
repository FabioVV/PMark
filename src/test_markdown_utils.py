import unittest
from markdown_utils import extract_markdown_images, extract_markdown_links


class TestMarkdownUtils(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![img text](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("img text", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with an [link text](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual(
            [("link text", "https://i.imgur.com/zjjcJKZ.png")], matches
        )
