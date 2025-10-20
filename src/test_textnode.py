import unittest
from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_text_eq(self):
        nd1 = TextNode("simple node text", TextType.PLAIN_TEXT)
        nd2 = TextNode("simple node text", TextType.PLAIN_TEXT)
        self.assertEqual(nd1, nd2)

    def test_text_ne(self):
        nd1 = TextNode("simple node text", TextType.PLAIN_TEXT)
        nd2 = TextNode("different text", TextType.PLAIN_TEXT)
        self.assertNotEqual(nd1, nd2)

    def test_node_type_ne(self):
        nd1 = TextNode("bold text", TextType.PLAIN_TEXT)
        nd2 = TextNode("bold text", TextType.BOLD_TEXT)
        self.assertNotEqual(nd1, nd2)

    def test_node_type_eq(self):
        nd1 = TextNode("bold text", TextType.BOLD_TEXT)
        nd2 = TextNode("bold text", TextType.BOLD_TEXT)
        self.assertEqual(nd1, nd2)

    def test_url_eq(self):
        nd1 = TextNode("bold text", TextType.BOLD_TEXT)
        nd2 = TextNode("image text", TextType.IMAGE_TEXT, "image/url")
        self.assertNotEqual(nd1.url, nd2.url)

    def test_url_is_none(self):
        nd1 = TextNode("image text", TextType.IMAGE_TEXT, "image/url")
        self.assertIsNotNone(nd1.url)


if __name__ == "__main__":
    _ = unittest.main()
