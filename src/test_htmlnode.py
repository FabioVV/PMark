import unittest
from htmlnode import HTMLNode


class TestHtmlNode(unittest.TestCase):
    def test_attrs_is_none(self):
        nd1 = HTMLNode("h1", "Hello, World!", None, None)
        nd2 = HTMLNode("h1", "Hello, World!", None)
        nd3 = HTMLNode("h1", "Hello, World!")

        self.assertIsNone(nd1.attrs)
        self.assertIsNone(nd2.attrs)
        self.assertIsNone(nd3.attrs)

    def test_format_attrs(self):
        nd1 = HTMLNode(
            "h1", "Hello, World!", None, {"class": "header1", "id": "main-header"}
        )

        self.assertEqual(nd1.attrs_to_html(), ' class="header1" id="main-header"')


if __name__ == "__main__":
    _ = unittest.main()
