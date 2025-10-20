#!/usr/bin/env python3
import sys
import subprocess

try:
    args = []  # FIXME: maybe let the user pass in some args

    result = subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", "src"] + args
    )
    if result.returncode != 0:
        print("Error: subprocess returned non-zero exit code")
        print(result)
        sys.exit(result.returncode)

except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
