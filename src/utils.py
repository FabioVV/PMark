from textnode import TextNode, TextType
from htmlnode import LeafNode


def text_node_to_html_node(txt_node: TextNode) -> LeafNode:
    match txt_node.text_type:
        case TextType.PLAIN_TEXT:
            return LeafNode(None, txt_node.text)
        case TextType.BOLD_TEXT:
            return LeafNode("b", txt_node.text)
        case TextType.ITALIC_TEXT:
            return LeafNode("i", txt_node.text)
        case TextType.UNDERLINE_TEXT:
            return LeafNode("u", txt_node.text)
        case TextType.STRIKETHROUGH_TEXT:
            return LeafNode("s", txt_node.text)
        case TextType.CODE_TEXT:
            return LeafNode("code", txt_node.text)
        case TextType.LINK_TEXT:
            return LeafNode("a", txt_node.text, {"href": txt_node.url or "#"})
        case TextType.IMAGE_TEXT:
            return LeafNode(
                "img", "", {"src": txt_node.url or "", "alt": txt_node.text}
            )
        case _:
            raise ValueError(f"Unexpected TextType: {txt_node.text_type}")
