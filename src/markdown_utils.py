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
    """Converts the markdown text to a list of sections(blocks) with leading and trailing whitespace removed"""
    md_blocks = md_text.split("\n\n")
    return [block.strip() for block in md_blocks]


def extract_markdown_title(md_text: str) -> str:
    """Extracts the first level one header (# ...) it finds from the markdown text to be used as the page title.\n If no level one header is found, returns 'untitled'"""
    text: list[str] = md_text.split("\n")
    for line in text:
        _line = line.strip()
        if _line.startswith("#"):
            return _line.lstrip("#").strip()
    return "untitled"


def markdown_to_html_node(md_text: str) -> HTMLNode:
    """Converts markdown text to a single parent HTMLNode containing all the markdown as children nodes.\n The parent is a <div>."""
    blocks = markdown_to_blocks(md_text)

    html_node: HTMLNode = HTMLNode("div")

    for block in blocks:
        btype = block_to_block_type(block)

        match btype:
            case BlockType.PARAGRAPH:
                text_node = text_to_textnodes(block)
                children = text_nodes_to_children_nodes(text_node)
                html_node.add_child(HTMLNode("p", "", children))

            case BlockType.CODE:
                text_node = make_text_node(block, TextType.CODE_TEXT)
                children = text_node_to_html_node(text_node)
                html_node.add_child(HTMLNode("code", "", [children]))

            case BlockType.QUOTE:
                text_node = text_to_textnodes(block)
                children = text_nodes_to_children_nodes(text_node)
                html_node.add_child(HTMLNode("blockquote", "", children))

            case BlockType.HEADING:
                heading_level = len(block) - len(block.lstrip("#"))
                text_node = text_to_textnodes(block)
                children = text_nodes_to_children_nodes(text_node)
                html_node.add_child(HTMLNode(f"h{heading_level}", "", children))

            case BlockType.ORDERED_LIST:
                text_node = text_to_textnodes(block)
                children = text_nodes_to_children_nodes(text_node)
                html_node.add_child(HTMLNode("ol", "", children))

            case BlockType.UNORDERED_LIST:
                text_node = text_to_textnodes(block)
                children = text_nodes_to_children_nodes(text_node)
                html_node.add_child(HTMLNode("ul", "", children))

    return html_node
