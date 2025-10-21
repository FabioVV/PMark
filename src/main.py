from textnode import TextNode, TextType
from htmlnode import ParentNode, LeafNode, HTMLNode

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
    "article",
    [nd1, nd2],
    {"style": "background-color:yellow; color:red;"},
)

with open("out.html", "w", encoding="utf-8") as f:
    _ = f.write(nd3.to_html())
