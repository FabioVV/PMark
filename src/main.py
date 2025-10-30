import logging
import subprocess
import sys
import os
from src.static import clean_dst, setup_static_files
from src.gen import generate_pages_from_path_md
from src.server import run_server
from src.warden import Warden

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
    args_cmd = sys.argv[1:]
    basepath = sys.argv[1:2]  # Do this more elegantly later. Add command line options

    if len(sys.argv) <= 1:
        basepath = []

    dir_to_generate_from = os.path.join("content")
    commands = [sys.executable, "-m", "src.main"] + args_cmd

    warden = Warden(dir_to_generate_from)
    if warden.save_dir_state():
        changes = warden.monitor()

        for has_changes in changes:
            if has_changes:
                result = subprocess.run(commands)  # rebuild project

                if result.returncode != 0:
                    print("Error: subprocess returned non-zero exit code")
                    print(result)
                    sys.exit(result.returncode)

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
    run_server("docs", 8001)


main()
