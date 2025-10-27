import logging
import os


def write_to_file(dst: str, content: str) -> None:
    filename = os.path.basename(dst)
    try:
        with open(dst, "w") as file:
            _ = file.write(content)

    except FileNotFoundError:
        logging.error(f"Error: File '{filename}' not found.")
    except PermissionError:
        logging.error(f"Error: Permission denied for '{filename}'.")
    except UnicodeDecodeError:
        logging.error(
            f"Error: Could not decode '{filename}'. Try using a different encoding for the file, like UTF-8."
        )
    except Exception as e:
        logging.error(f"Unexpected error: {e}")


def read_from_file(filepath: str) -> str:
    filename = os.path.basename(filepath)
    try:
        with open(filepath, "r") as file:
            content = file.read()
            return content
    except FileNotFoundError:
        logging.error(f"Error: File '{filename}' not found.")
        return ""
    except PermissionError:
        logging.error(f"Error: Permission denied for '{filename}'.")
        return ""

    except UnicodeDecodeError:
        logging.error(
            f"Error: Could not decode '{filename}'. Try using a different encoding for the file, like UTF-8."
        )
        return ""

    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return ""
