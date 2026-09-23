#!/usr/bin/env python3
import sys
from pathlib import Path

# Automatically inject src directory into PATH
src_dir = Path(__file__).resolve().parent / "src"
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

from serinity.cli import run_cli

if __name__ == "__main__":
    run_cli()
