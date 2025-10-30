#!/usr/bin/env python3
import os
import sys
import subprocess

target = os.path.join(os.getcwd())

try:
    args_cmd = sys.argv[1:]

    if len(sys.argv) <= 1:
        args_cmd = []

    command = [sys.executable, "-m", "src.main"] + args_cmd
    result = subprocess.run(command)
    if result.returncode != 0:
        print("Error: subprocess returned non-zero exit code")
        print(result)
        sys.exit(result.returncode)

except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
