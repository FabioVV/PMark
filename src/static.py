import os
import logging
import shutil
# import sys


def clean_dst(dst: str = "docs") -> bool:
    """
    Deletes all content inside of the destination folder to ensure that the site generation is clean.\n
    WARNING: You can pass in any filesystem path, and if it can, this function will delete everything inside.\n
    Use with caution.
    """
    target = os.path.abspath(os.path.expanduser(dst))

    def recursive_delete(path: str):
        try:
            for file in os.listdir(path):
                file_path = os.path.join(path, file)

                if os.path.isfile(file_path):
                    logging.info(f"Deleting file {file_path}...")

                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    logging.info(f"Entering subfolder: {file_path} ...")

                    _ = recursive_delete(file_path)

            os.rmdir(path)

        except Exception as e:
            logging.error(f"Error cleaning {path} directory: {e}")
            return False

    try:
        if os.path.exists(target) and os.path.isdir(target):
            # r = input(
            #     f"(If not confirmed, files will be generated anyway).\nConfirm cleaning of the {target} directory? (y/n)"
            # )
            r = "y"
            if r.lower() == "y":
                _ = recursive_delete(target)
                logging.info(f"{dst} directory cleaned...")
            else:
                logging.info("aborting...")
                # sys.exit(0)
                return True

            # Recreate the directory, if necessary
            os.makedirs(target, exist_ok=True)
            return True

        else:
            logging.error(
                f"Error cleaning {dst}. (Is it a directory? Does it exists?) "
            )
            return False

    except Exception as e:
        logging.error(f"Error cleaning {dst} directory: {e}")
        return False


def setup_static_files(src: str = "static", dst: str = "docs") -> bool:
    """
    If no args are given, Copies the static files provided in the /static folder at the root of the project to the /public folder.\n
    If more flexibility is needed, source and destiny paths can be passed to control from where the static files will be copied to where.
    """

    target_from = os.path.abspath(os.path.expanduser(src))
    target_to = os.path.abspath(os.path.expanduser(dst))

    # Ensure source exists
    if not os.path.exists(target_from):
        logging.error(f"Source directory does not exist: {target_from}")
        return False

    if not os.path.isdir(target_from):
        logging.error(f"Source path is not a directory: {target_from}")
        return False

    if not os.path.isdir(target_to):
        logging.error(f"Destination path is not a directory: {target_from}")
        return False

    # Ensure destination exists
    os.makedirs(target_to, exist_ok=True)

    def setup_static_files_recursive(src: str, dst: str):
        try:
            for file in os.listdir(src):
                file_path = os.path.join(src, file)

                if os.path.isfile(file_path):
                    logging.info(f"Copying: {file_path} ...")
                    _ = shutil.copy2(file_path, dst)

                elif os.path.isdir(file_path):
                    subfolder_path: str = os.path.join(dst, os.path.basename(file_path))
                    logging.info(f"Entering subfolder: {file_path} ...")
                    logging.info(f"Creating subfolder: {subfolder_path} ...")

                    os.makedirs(
                        subfolder_path, exist_ok=True
                    )  # create the folder at dst

                    _ = setup_static_files_recursive(file_path, subfolder_path)

        except Exception as e:
            logging.error(f"Error copying static files from {src} to {dst}: {e}")
            return False

    _ = setup_static_files_recursive(target_from, target_to)

    return True
