import unittest
from src.markdown_utils import (
    markdown_to_blocks,
)
from src.markdown_blocks import block_to_block_type, BlockType
from src.textnode_utils import (
    extract_markdown_images,
    extract_markdown_links,
    extract_markdown_title,
)


class TestMarkdownUtils(unittest.TestCase):
    def test_extract_markdown_title(self):
        matches = extract_markdown_title(
            """
             # Title bruh
             - Wow, this is some markdown!
             # hmmmm this is not the title!
            """
        )
        self.assertEqual("Title bruh", matches)

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

    def test_markdown_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""

        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_blocks_type(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""

        blocks = markdown_to_blocks(md)
        self.assertEqual(block_to_block_type(blocks[0]), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(blocks[1]), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(blocks[2]), BlockType.UNORDERED_LIST)
