from operator import ge
import os
import logging
from src.fileop import read_from_file, write_to_file
from src.markdown_utils import markdown_to_html_node
from src.textnode_utils import extract_markdown_title


def generate_page_from_path_md(
    template: str = "template.html", src: str = "", dst: str = "public"
) -> bool:
    """Generates a single HTML page from a given markdown file using a base template.\n
    In the case that the destination directory path does not exists, it tries to create it\n
    Returns the path of the generated page, or an empty string in the case of a silent failure
    """

    target_from = os.path.abspath(os.path.expanduser(src))
    target_to = os.path.abspath(os.path.expanduser(dst))
    template = os.path.abspath(os.path.expanduser(template))

    # Ensure source exists
    if not os.path.exists(target_from):
        logging.error(f"Source directory does not exist: {target_from}")
        return False

    if not os.path.isdir(target_to):
        logging.error(f"Destination path is not a directory: {target_from}")
        return False

    # Ensure destination exists
    os.makedirs(target_to, exist_ok=True)

    logging.info(f"Generating page from ({target_from}) to ({target_to})...")

    filename = os.path.basename(target_from).replace("md", "html")
    filepath_to_create = os.path.join(target_to, filename)

    gen_page = read_from_file(template)
    src_md_content = read_from_file(target_from)

    generated_html = markdown_to_html_node(src_md_content).to_html()
    markdown_page_title = extract_markdown_title(src_md_content)

    gen_page = gen_page.replace("{{ Title }}", markdown_page_title)
    gen_page = gen_page.replace("{{ Content }}", generated_html)

    write_to_file(filepath_to_create, gen_page)

    return True
