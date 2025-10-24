import logging
import sys
from markdown_utils import markdown_to_html_node, extract_markdown_title
from static import clean_dst, setup_static_files

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        # logging.StreamHandler(sys.stderr),
    ],
)


def main():
    md = """

    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

    #     node = markdown_to_html_node(md)

    #     with open("test.html", "w") as file:
    #         _ = file.write(node.to_html())
    # if not clean_dst():
    #     logging.error("Error during cleaning...")
    #     sys.exit(1)

    # if not setup_static_files():
    #     logging.error("Error during static file setup...")
    #     sys.exit(1)
    print(extract_markdown_title(md))


main()
