from re import findall

MARKDOWN_IMAGES_REGEX = r"!\[(.*?)\]\((.*?)\)"
MARKDOWN_LINKS_REGEX = r"\[(.*?)\]\((.*?)\)"


def extract_markdown_images(md_text: str) -> list[tuple[str, str]]:
    return findall(MARKDOWN_IMAGES_REGEX, md_text)


def extract_markdown_links(md_text: str) -> list[tuple[str, str]]:
    return findall(MARKDOWN_LINKS_REGEX, md_text)
