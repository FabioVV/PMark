from textnode import TextNode, TextType
from htmlnode import ParentNode, LeafNode, HTMLNode
from textnode_utils import split_nodes_delimiter, split_nodes_link

# node = TextNode("This is text with a _code block_ word", TextType.PLAIN_TEXT)
# new_nodes = split_nodes_delimiter([node], "_", TextType.UNDERLINE_TEXT)

# print(new_nodes)

node = TextNode(
    "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
    TextType.PLAIN_TEXT,
)

links = split_nodes_link([node])
print(links)
