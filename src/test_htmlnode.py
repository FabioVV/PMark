import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHtmlNode(unittest.TestCase):
    def test_attrs_is_none(self):
        nd1 = HTMLNode("h1", "Hello, World!", None, None)
        nd2 = HTMLNode("h1", "Hello, World!", None)
        nd3 = HTMLNode("h1", "Hello, World!")

        self.assertIsNone(nd1.attrs)
        self.assertIsNone(nd2.attrs)
        self.assertIsNone(nd3.attrs)

    def test_attrs_is_not_none(self):
        nd1 = HTMLNode(
            "h1", "Hello, World!", None, {"class": "header1", "id": "main-header"}
        )

        self.assertIsNotNone(nd1.attrs)

    def test_format_attrs(self):
        nd1 = HTMLNode(
            "h1", "Hello, World!", None, {"class": "header1", "id": "main-header"}
        )

        self.assertEqual(nd1.attrs_to_html(), ' class="header1" id="main-header"')

    def test_leaf_to_h1(self):
        nd1 = LeafNode("h1", "Hello, World!", {"class": "header1", "id": "main-header"})

        self.assertEqual(
            nd1.to_html(), '<h1 class="header1" id="main-header">Hello, World!</h1>'
        )

    def test_parent_node_format(self):
        nd1 = ParentNode(
            "h1",
            [
                LeafNode("b", "Hello, World!"),
                LeafNode(None, "Just some text"),
                LeafNode("span", "Welcome!"),
            ],
            {"style": "font-size:16px; color:blue;"},
        )
        self.assertEqual(
            nd1.to_html(),
            '<h1 style="font-size:16px; color:blue;"><b>Hello, World!</b>Just some text<span>Welcome!</span></h1>',
        )

    def test_parent_node_children(self):
        nd1 = ParentNode(
            "h1",
            [
                LeafNode("b", "Hello, World!"),
                LeafNode(None, "Just some text"),
                LeafNode("span", "Welcome!"),
            ],
            {"style": "font-size:16px; color:blue;"},
        )
        nd2 = ParentNode(
            "article",
            [nd1],
            {"style": "background-color:yellow; color:red;"},
        )

        self.assertEqual(
            nd2.to_html(),
            '<article style="background-color:yellow; color:red;"><h1 style="font-size:16px; color:blue;"><b>Hello, World!</b>Just some text<span>Welcome!</span></h1></article>',
        )

    def test_parent_node_different_children(self):
        nd1 = ParentNode(
            "h1",
            [
                LeafNode("b", "Hello, World!"),
                LeafNode(None, "Just some text"),
                LeafNode("span", "Welcome!"),
            ],
            None,
        )

        nd2 = LeafNode("h3", "This is it.", {"class": "important"})

        nd3 = ParentNode(
            "header",
            [nd1, nd2],
            {"style": "background-color:yellow; color:red;"},
        )

        self.assertEqual(
            nd3.to_html(),
            '<header style="background-color:yellow; color:red;"><h1><b>Hello, World!</b>Just some text<span>Welcome!</span></h1><h3 class="important">This is it.</h3></header>',
        )


if __name__ == "__main__":
    _ = unittest.main()
