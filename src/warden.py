import logging
import os
from time import sleep
from src.fileop import write_json_to_file, read_json_file_stats_from_file

FILES_STATS_PATH = "internal/file_stats.json"

##
#  This file contains the implementation of a 'warden' script. It's simple in nature.
#
#  (I know there better ways to do this or even production ready projects that do just this.
#  But then i ask you, where is the fun in running someone else's code?)
#
#  It's Used to detect file changes in the markdown content directory passed in by the user for a livereload
##


class Warden:
    def __init__(
        self, dir_path: str = "content", files_stats_path: str = FILES_STATS_PATH
    ):
        self.dir_path: str = dir_path
        self.files_stats_path: str = files_stats_path
        # self.total_files_in_dir: int = sum(1 for _ in os.walk("dirpath") for __ in _[2])
        self._file_stats_cache: dict[
            str, dict[str, str | float]
        ] = {}  # Cache for quick access
        self._load_file_stats_cache()

    def _load_file_stats_cache(self) -> None:
        """Load file stats into memory for faster access"""
        try:
            files_metadata = read_json_file_stats_from_file(self.files_stats_path)
            for file_data in files_metadata:
                key = file_data["filepath"].replace("\\", "/")
                self._file_stats_cache[key] = {
                    "filename": file_data["filename"],
                    "ctime": float(file_data["ctime"]),
                    "mtime": float(file_data["mtime"]),
                }
        except Exception as e:
            logging.warning(f"Could not load existing file stats: {e}")
            self._file_stats_cache = {}

    def save_dir_state(self) -> bool:
        """
        A simple function that recursively saves ctime and mtime for file tracking from files inside of the directory path (self.files_stats_path).
        """
        files: list[dict[str, str]] = []

        def save_initial_files_state_recursive(path: str) -> None:
            try:
                for entry in os.scandir(path):
                    if entry.is_file():
                        file_stat = entry.stat()

                        file_data = {
                            "filename": entry.name,
                            "filepath": entry.path.replace("\\", "/"),
                            "mtime": f"{file_stat.st_mtime}",
                            "ctime": f"{file_stat.st_ctime}",
                        }

                        files.append(file_data)

                        self._file_stats_cache[file_data["filepath"]] = {
                            "filename": file_data["filename"],
                            "ctime": float(file_data["ctime"]),
                            "mtime": float(file_data["mtime"]),
                        }

                    elif entry.is_dir():
                        _ = save_initial_files_state_recursive(entry.path)

            except Exception as e:
                logging.error(f"Error saving content files information: {e}")

        save_initial_files_state_recursive(self.dir_path)
        write_json_to_file(self.files_stats_path, files)

        return True

    def has_file_changed(self, filepath: str) -> bool:
        try:
            normalized_path = filepath.replace("\\", "/")
            if normalized_path not in self._file_stats_cache:
                self._update_snapshot_for_file(normalized_path)
                return True

            file_stat = os.stat(filepath)
            ctime: float = file_stat.st_ctime
            mtime: float = file_stat.st_mtime

            cached_data = self._file_stats_cache[normalized_path]
            if ctime != cached_data["ctime"] or mtime != cached_data["mtime"]:
                self._update_snapshot_for_file(normalized_path)
                return True

            return False

        except (OSError, FileNotFoundError):
            normalized_path = filepath.replace("\\", "/")
            # File was deleted or inaccessible
            if normalized_path in self._file_stats_cache:
                self._remove_file_from_dir_state(normalized_path)
            return True

        except Exception as e:
            logging.error(f"Error checking file change {filepath}: {e}")
            return False

    def _remove_file_from_dir_state(self, filepath: str) -> None:
        normalized_path = filepath.replace("\\", "/")
        if normalized_path in self._file_stats_cache:
            del self._file_stats_cache[normalized_path]
            _ = self.save_dir_state()

    def _update_snapshot_for_file(self, filepath: str) -> None:
        try:
            file_stat = os.stat(filepath)
            normalized_path = filepath.replace("\\", "/")

            # Update cache
            self._file_stats_cache[normalized_path] = {
                "filename": os.path.basename(filepath),
                "ctime": file_stat.st_ctime,
                "mtime": file_stat.st_mtime,
            }

            _ = self.save_dir_state()

        except Exception as e:
            logging.error(f"Error updating snapshot for {filepath}: {e}")

    def has_dir_files_changed(self, dir_path: str = "content") -> bool:
        changes_detected = False
        current_files: set[str] = set()

        def check_directory_recursive(path: str) -> bool:
            nonlocal changes_detected
            nonlocal current_files

            try:
                for entry in os.scandir(path):
                    if entry.is_file():
                        filepath = entry.path.replace("\\", "/")
                        current_files.add(filepath)

                        if self.has_file_changed(filepath):
                            changes_detected = True
                            return True

                    elif entry.is_dir():
                        if check_directory_recursive(entry.path):
                            return True
                return False
            except Exception as e:
                logging.error(f"Error checking directory {path}: {e}")
                return False

        if check_directory_recursive(dir_path):
            return True

        # Check for deleted files
        cached_files = set(self._file_stats_cache.keys())
        deleted_files = cached_files - current_files
        if deleted_files:
            for filepath in deleted_files:
                del self._file_stats_cache[filepath]

            _ = self.save_dir_state()
            return True

        return changes_detected

    def monitor(self, poll_interval: float = 0.3):
        while True:
            has_changes = self.has_dir_files_changed()
            yield has_changes
            sleep(poll_interval)
