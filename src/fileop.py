import logging
import os
import json


def read_json_file_stats_from_file(files_stats_path: str) -> list[dict[str, str]]:
    try:
        with open(files_stats_path, "r") as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        logging.error(f"Error: File '{files_stats_path}' not found.")
        return [{}]
    except PermissionError:
        logging.error(f"Error: Permission denied for '{files_stats_path}'.")
        return [{}]
    except UnicodeDecodeError:
        logging.error(
            f"Error: Could not decode '{files_stats_path}'. Try using a different encoding for the file, like UTF-8."
        )
        return [{}]
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return [{}]


def write_json_to_file(dst: str, data: list[dict[str, str]]) -> None:
    filename = os.path.basename(dst)
    try:
        with open(dst, "w") as file:
            json.dump(data, file, indent=4)

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
