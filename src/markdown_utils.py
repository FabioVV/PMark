from re import findall
from htmlnode import HtmlNode

MARKDOWN_IMAGES_REGEX = r"!\[(.*?)\]\((.*?)\)"
MARKDOWN_LINKS_REGEX = r"\[(.*?)\]\((.*?)\)"


def extract_markdown_images(md_text: str) -> list[tuple[str, str]]:
    return findall(MARKDOWN_IMAGES_REGEX, md_text)


def extract_markdown_links(md_text: str) -> list[tuple[str, str]]:
    return findall(MARKDOWN_LINKS_REGEX, md_text)


def markdown_to_blocks(md_text: str) -> list[str]:
    md_blocks = md_text.split("\n\n")
    return [block.strip() for block in md_blocks]


def markdown_to_html_node(md_text: str) -> HtmlNode: ...
