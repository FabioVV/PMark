from src.htmlnode import HTMLNode  # , ParentNode
from src.markdown_blocks import block_to_block_type, block_to_li_list, BlockType
from src.textnode_utils import (
    text_to_textnodes,
    text_nodes_to_children_nodes,
    text_nodes_to_children_li_nodes,
    text_node_to_html_node,
    make_text_node,
)
from src.textnode import TextType


def markdown_to_blocks(md_text: str) -> list[str]:
    """Converts the markdown text to a list of sections(blocks) with leading and trailing whitespace removed"""
    md_blocks = md_text.split("\n\n")
    return [block.strip() for block in md_blocks]


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
                if block.startswith("```") and block.endswith(
                    "```"
                ):  # FIXME: this can be done more elegantly
                    block = block[3 : len(block) - 3].strip()

                text_node = make_text_node(block, TextType.CODE_TEXT)
                children = text_node_to_html_node(text_node)

                html_node.add_child(
                    HTMLNode("pre", "", [HTMLNode("code", "", [children])])
                )

            case BlockType.QUOTE:
                block = "".join(
                    [line.lstrip(">").strip() for line in block.split("\n")]
                )
                text_node = text_to_textnodes(block)
                children = text_nodes_to_children_nodes(text_node)
                html_node.add_child(HTMLNode("blockquote", "", children))

            case BlockType.HEADING:
                heading_level = len(block) - len(block.lstrip("#"))
                text_node = text_to_textnodes(block.lstrip("#").strip())
                children = text_nodes_to_children_nodes(text_node)
                html_node.add_child(HTMLNode(f"h{heading_level}", "", children))

            case BlockType.ORDERED_LIST:
                block = [
                    line.lstrip(f"{idx + 1}. ").strip() + "\n"
                    for idx, line in enumerate(block.split("\n"))
                ]
                li_nodes: list[HTMLNode] = block_to_li_list(block)

                html_node.add_child(HTMLNode("ol", "", li_nodes))

            case BlockType.UNORDERED_LIST:
                block = [line.lstrip("-") + "\n" for line in block.split("\n")]
                li_nodes: list[HTMLNode] = block_to_li_list(block)

                html_node.add_child(HTMLNode("ul", "", li_nodes))

    return html_node
