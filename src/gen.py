from operator import ge
import os
import logging
from src.fileop import read_from_file, write_to_file
from src.markdown_utils import markdown_to_html_node
from src.textnode_utils import extract_markdown_title


def generate_pages_from_path_md(
    template: str = "template.html", src: str = "", dst: str = "public"
) -> bool:
    """Generates HTML pages from the markdown files present at the src preserving the directory structure while a base template.\n
    In the case that the destination directory path does not exists, it tries to create it\n
    """
    target_from = os.path.abspath(os.path.expanduser(src))
    target_to = os.path.abspath(os.path.expanduser(dst))
    template = os.path.abspath(os.path.expanduser(template))

    # Ensure source exists
    if not os.path.exists(target_from):
        logging.error(f"Source directory does not exist: {target_from}")
        return False

    if not os.path.exists(template) or os.path.isdir(template):
        logging.error(f"Template does not exist or is not a file: {template}")
        return False

    if not os.path.isdir(target_to):
        logging.error(f"Destination path is not a directory: {target_from}")
        return False

    def generate_pages_from_path_md_recursive(
        template: str = "template.html", src: str = "", dst: str = "public"
    ):
        gen_page = read_from_file(template)

        try:
            for file in os.listdir(src):
                file_path = os.path.join(src, file)

                if os.path.isfile(file_path):
                    filename = os.path.basename(file_path).replace("md", "html")
                    filepath_to_create = os.path.join(dst, filename)
                    src_md_content = read_from_file(file_path)

                    logging.info(
                        f"Generating page from ({file_path}) to ({filepath_to_create})..."
                    )

                    generated_html = markdown_to_html_node(src_md_content).to_html()
                    markdown_page_title = extract_markdown_title(src_md_content)

                    gen_page = gen_page.replace("{{ Title }}", markdown_page_title)
                    gen_page = gen_page.replace("{{ Content }}", generated_html)

                    write_to_file(filepath_to_create, gen_page)

                elif os.path.isdir(file_path):
                    subfolder_path: str = os.path.join(dst, os.path.basename(file_path))
                    logging.info(f"Entering subfolder: {file_path} ...")
                    logging.info(f"Creating subfolder: {subfolder_path} ...")

                    os.makedirs(
                        subfolder_path, exist_ok=True
                    )  # create the folder at dst

                    generate_pages_from_path_md_recursive(
                        template, file_path, subfolder_path
                    )

        except Exception as e:
            logging.error(f"Error generating pages from directory {src}: {e}")
            return False

    generate_pages_from_path_md_recursive(template, target_from, target_to)
    return True


def generate_page_from_path_md(
    template: str = "template.html", src: str = "", dst: str = "public"
) -> bool:
    """Generates a single HTML page from a given markdown file using a base template.\n
    In the case that the destination directory path does not exists, it tries to create it\n
    """

    target_from = os.path.abspath(os.path.expanduser(src))
    target_to = os.path.abspath(os.path.expanduser(dst))
    template = os.path.abspath(os.path.expanduser(template))

    # Ensure source exists
    if not os.path.exists(target_from):
        logging.error(f"Source directory does not exist: {target_from}")
        return False

    if not os.path.exists(template) or os.path.isdir(template):
        logging.error(f"Template does not exist or is not a file: {template}")
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
