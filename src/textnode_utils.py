from re import findall

from textnode import TextNode, TextType
from htmlnode import LeafNode


DELIMITERS = {
    "**": TextType.BOLD_TEXT,
    "_": TextType.UNDERLINE_TEXT,
    "`": TextType.CODE_TEXT,
}
MARKDOWN_IMAGES_REGEX = r"!\[(.*?)\]\((.*?)\)"
MARKDOWN_LINKS_REGEX = r"\[(.*?)\]\((.*?)\)"


def extract_markdown_images(md_text: str) -> list[tuple[str, str]]:
    return findall(MARKDOWN_IMAGES_REGEX, md_text)


def extract_markdown_links(md_text: str) -> list[tuple[str, str]]:
    return findall(MARKDOWN_LINKS_REGEX, md_text)


def extract_markdown_title(md_text: str) -> str:
    """Extracts the first level one header (# ...) it finds from the markdown text to be used as the page title.\n If no level one header is found, returns 'untitled'"""
    text: list[str] = md_text.split("\n")
    for line in text:
        _line = line.strip()
        if _line.startswith("#"):
            return _line.lstrip("#").strip()
    return "untitled"


def make_text_node(text: str, text_type: TextType, url: str | None = None) -> TextNode:
    return TextNode(text, text_type, url)


def text_nodes_to_children_nodes(nodes: list[TextNode]) -> list[LeafNode]:
    return [text_node_to_html_node(node) for node in nodes]


def text_node_to_html_node(txt_node: TextNode) -> LeafNode:
    match txt_node.text_type:
        case TextType.PLAIN_TEXT:
            return LeafNode(None, txt_node.text)
        case TextType.BOLD_TEXT:
            return LeafNode("strong", txt_node.text)
        case TextType.ITALIC_TEXT:
            return LeafNode("em", txt_node.text)
        case TextType.UNDERLINE_TEXT:
            return LeafNode("u", txt_node.text)
        case TextType.STRIKETHROUGH_TEXT:
            return LeafNode("del", txt_node.text)
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
            new_nodes.append(i)
            continue

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

        images = extract_markdown_images(i.text)
        if len(images) == 0:
            new_nodes.append(i)
            continue

        old_text = i.text
        for alt, url in images:
            sections = old_text.split(f"![{alt}]({url})", 1)

            if len(sections) != 2:
                raise ValueError("Image section not closed")

            if sections[0] != "":
                new_nodes.append(make_text_node(sections[0], TextType.PLAIN_TEXT))

            new_nodes.append(make_text_node(alt, TextType.IMAGE_TEXT, url))
            old_text = sections[1]

        if old_text != "":
            new_nodes.append(make_text_node(old_text, TextType.PLAIN_TEXT))

    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []

    for i in old_nodes:
        if i.text_type != TextType.PLAIN_TEXT or i.text == "":
            new_nodes.append(i)
            continue

        links = extract_markdown_links(i.text)
        if len(links) == 0:
            new_nodes.append(i)
            continue

        old_text = i.text
        for alt, url in links:
            sections = old_text.split(f"[{alt}]({url})", 1)

            if len(sections) != 2:
                raise ValueError("Link section not closed")

            if sections[0] != "":
                new_nodes.append(make_text_node(sections[0], TextType.PLAIN_TEXT))

            new_nodes.append(make_text_node(alt, TextType.LINK_TEXT, url))
            old_text = sections[1]

        if old_text != "":
            new_nodes.append(make_text_node(old_text, TextType.PLAIN_TEXT))

    return new_nodes


def text_to_textnodes(text: str) -> list[TextNode]:
    nodes: list[TextNode] = [make_text_node(text, TextType.PLAIN_TEXT)]

    for delimiter, delimiter_type in DELIMITERS.items():
        nodes = split_nodes_delimiter(nodes, delimiter, delimiter_type)

    return split_nodes_link(split_nodes_image(nodes))
