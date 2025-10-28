import logging
import sys
import os
from src.static import clean_dst, setup_static_files
from src.gen import generate_page_from_path_md, generate_pages_from_path_md
from src.server import run_server

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        # logging.StreamHandler(sys.stderr),
    ],
)


def main():
    dir_to_generate_from = os.path.join("content")

    if not clean_dst():
        sys.exit(1)

    if not setup_static_files():
        sys.exit(1)

    if not generate_pages_from_path_md(src=dir_to_generate_from):
        logging.error(f"Failed to generate files from directory {dir_to_generate_from}")
        sys.exit(1)

    logging.info("\n\nInitializing server...")
    run_server()


main()
