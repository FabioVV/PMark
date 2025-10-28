import logging
import sys
import os
from src.static import clean_dst, setup_static_files
from src.gen import generate_pages_from_path_md
from src.server import run_server

# "/reponame/" format for gitpages

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        # logging.StreamHandler(sys.stderr),
    ],
)


def main():
    basepath = sys.argv[1:2]  # Do this more elegantly later. Add command line options

    if len(sys.argv) <= 1:
        basepath = []

    dir_to_generate_from = os.path.join("content")

    if not clean_dst():
        sys.exit(1)

    if not setup_static_files():
        sys.exit(1)

    if not generate_pages_from_path_md(
        src=dir_to_generate_from, basepath=basepath[0] if len(basepath) > 0 else "/"
    ):
        logging.error(f"Failed to generate files from directory {dir_to_generate_from}")
        sys.exit(1)

    logging.info("\n\nInitializing server...")
    run_server()


main()
