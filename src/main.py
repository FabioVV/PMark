from textnode import TextNode, TextType
from htmlnode import ParentNode, LeafNode, HTMLNode
from textnode_utils import split_nodes_delimiter, split_nodes_link, text_to_textnodes

# node = TextNode("This is text with a _code block_ word", TextType.PLAIN_TEXT)
# new_nodes = split_nodes_delimiter([node], "_", TextType.UNDERLINE_TEXT)

# print(new_nodes)


nodes = text_to_textnodes(
    "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
)
print(nodes)
