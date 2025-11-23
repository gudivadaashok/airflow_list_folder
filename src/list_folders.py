import os
import logging
from datetime import datetime
from pathlib import Path
import argparse

# -----------------------------
# Logging setup
# -----------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

# -----------------------------
# CLI Argument Parsing
# -----------------------------
parser = argparse.ArgumentParser(description="List folders in a directory.")
parser.add_argument(
    "directory",
    type=str,
    help="Path to the directory you want to inspect"
)
args = parser.parse_args()

directory = Path(args.directory)

# -----------------------------
# Main logic
# -----------------------------
logging.info(f"Current time: {datetime.now()}")

if not directory.exists():
    logging.error(f"Directory does not exist: {directory}")
    exit(1)

logging.info(f"Scanning directory: {directory}")

folders = [p.name for p in directory.iterdir() if p.is_dir()]
folders.sort()

logging.info("Folders found:")
for name in folders:
    logging.info(f"  - {name}")
