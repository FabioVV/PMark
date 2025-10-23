import unittest
from textnode import TextNode, TextType
from textnode_utils import text_node_to_html_node


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

    def test_text_to_leafnode(self):
        nd1 = TextNode("text node", TextType.PLAIN_TEXT)
        html_node = text_node_to_html_node(nd1)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "text node")

    def test_img_to_leafnode(self):
        nd1 = TextNode("alt text from img", TextType.IMAGE_TEXT, "image/url")
        html_node = text_node_to_html_node(nd1)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual((html_node.attrs or {}).get("alt"), "alt text from img")

    def test_anchor_to_leafnode(self):
        nd1 = TextNode("text from link", TextType.LINK_TEXT, "www.example.com")
        html_node = text_node_to_html_node(nd1)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual((html_node.attrs or {}).get("href"), "www.example.com")


if __name__ == "__main__":
    _ = unittest.main()
