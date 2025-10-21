from textnode import TextNode, TextType
from htmlnode import ParentNode, LeafNode, HTMLNode
from textnode_utils import split_nodes_delimiter

node = TextNode("This is text with a _code block_ word", TextType.PLAIN_TEXT)
new_nodes = split_nodes_delimiter([node], "_", TextType.UNDERLINE_TEXT)

print(new_nodes)
