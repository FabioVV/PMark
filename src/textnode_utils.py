from textnode import TextNode, TextType
from htmlnode import LeafNode
from markdown_utils import extract_markdown_images, extract_markdown_links


def make_text_node(text: str, text_type: TextType, url: str | None = None) -> TextNode:
    return TextNode(text, text_type, url)


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


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    new_nodes: list[TextNode] = []

    for i in old_nodes:
        if i.text_type != TextType.PLAIN_TEXT:
            new_nodes.append(i)
            continue

        text_node: TextNode | None = None
        splitted_str = i.text.split(delimiter)
        if len(splitted_str) == 1:
            raise ValueError("Delimiter not found in text")

        start_del: int = i.text.find(delimiter)
        if (start_del) == -1:
            raise ValueError("Delimiter not found in text")

        end_del: int = i.text.find(delimiter, start_del + len(delimiter))
        if (end_del) == -1:
            raise ValueError("Closing delimiter not found in text")

        text_to_format = i.text[start_del + len(delimiter) : end_del]

        if delimiter == "`" or delimiter == "_" or delimiter == "**":
            text_node = make_text_node(text_to_format, text_type)
        else:
            raise ValueError("Delimiter not supported")

        for x in splitted_str:
            if x == text_to_format:
                new_nodes.append(text_node)
            else:
                new_nodes.append(make_text_node(x, TextType.PLAIN_TEXT))

    return new_nodes


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []

    for i in old_nodes:
        if i.text_type != TextType.PLAIN_TEXT:
            new_nodes.append(i)
            continue

        links = extract_markdown_images(i.text)
        new_nodes.extend(
            [make_text_node(alt, TextType.LINK_TEXT, url) for alt, url in links]
        )

    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []

    for i in old_nodes:
        if i.text_type != TextType.PLAIN_TEXT:
            new_nodes.append(i)
            continue

        links = extract_markdown_links(i.text)
        new_nodes.extend(
            [make_text_node(alt, TextType.LINK_TEXT, url) for alt, url in links]
        )

    return new_nodes
