from textnode import TextNode, TextType
from htmlnode import ParentNode, LeafNode, HTMLNode
from textnode_utils import split_nodes_delimiter, split_nodes_link, text_to_textnodes
from markdown_utils import markdown_to_blocks, markdown_to_html_node


def main():
    md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

    node = markdown_to_html_node(md)
    html = node.to_html()
    print(html)


main()
