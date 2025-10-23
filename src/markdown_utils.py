from htmlnode import HTMLNode, ParentNode
from markdown_blocks import block_to_block_type, BlockType
from textnode_utils import (
    text_to_textnodes,
    text_nodes_to_children_nodes,
    text_node_to_html_node,
    make_text_node,
    TextType,
)


def markdown_to_blocks(md_text: str) -> list[str]:
    md_blocks = md_text.split("\n\n")
    return [block.strip() for block in md_blocks]


def markdown_to_html_node(md_text: str) -> HTMLNode:
    blocks = markdown_to_blocks(md_text)

    html_node: HTMLNode = HTMLNode("div")

    for block in blocks:
        btype = block_to_block_type(block)

        match btype:
            case BlockType.PARAGRAPH:
                text_node = text_to_textnodes(block)
                children = text_nodes_to_children_nodes(text_node)
                node: HTMLNode = HTMLNode("p", "", children)
                html_node.add_child(node)

            case BlockType.CODE:
                text_node = make_text_node(text_node.text, TextType.CODE_TEXT)
                children = text_node_to_html_node(text_node)
                node: HTMLNode = HTMLNode("code", "", [children])
                html_node.add_child(node)

            case BlockType.QUOTE:
                text_node = text_to_textnodes(block)
                children = text_nodes_to_children_nodes(text_node)
                node: HTMLNode = HTMLNode("blockquote", "", children)
                html_node.add_child(node)

            case BlockType.HEADING:
                heading_level = len(block) - len(block.lstrip("#"))
                text_node = text_to_textnodes(block)
                children = text_nodes_to_children_nodes(text_node)
                node: HTMLNode = HTMLNode(f"h{heading_level}", "", children)
                html_node.add_child(node)

            case BlockType.ORDERED_LIST:
                text_node = text_to_textnodes(block)
                children = text_nodes_to_children_nodes(text_node)
                node: HTMLNode = HTMLNode("ol", "", children)
                html_node.add_child(node)

            case BlockType.UNORDERED_LIST:
                text_node = text_to_textnodes(block)
                children = text_nodes_to_children_nodes(text_node)
                node: HTMLNode = HTMLNode("ul", "", children)
                html_node.add_child(node)

    return html_node
