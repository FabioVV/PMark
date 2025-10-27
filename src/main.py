import logging
import sys
import os
from src.static import clean_dst, setup_static_files
from src.gen import generate_page_from_path_md

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        # logging.StreamHandler(sys.stderr),
    ],
)


def main():
    file_to_generate = os.path.join("content", "index.md")

    if not clean_dst():
        sys.exit(1)

    if not setup_static_files():
        sys.exit(1)

    if not generate_page_from_path_md(src=file_to_generate):
        logging.error(f"Failed to generate file {file_to_generate}")
        sys.exit(1)


main()
