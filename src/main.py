import logging
import sys
import os
from static import clean_dst, setup_static_files
from gen import generate_page_from_path_md

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        # logging.StreamHandler(sys.stderr),
    ],
)


def main():
    if not clean_dst():
        sys.exit(1)

    if not setup_static_files():
        sys.exit(1)

    generate_page_from_path_md(src=os.path.join("content", "index.md"))


main()
