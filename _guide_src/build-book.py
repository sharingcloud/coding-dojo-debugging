import os
import shutil

SRC_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SRC_DIR)

MDBOOK_EXE = os.path.join(SRC_DIR, "mdbook.exe")
BUILD_DIR = os.path.join(SRC_DIR, "book")
OUTPUT_DIR = os.path.join(PROJECT_DIR, "guide")

# Build book
os.system(f"cd {SRC_DIR} && {MDBOOK_EXE} build")

# Copy output
shutil.rmtree(OUTPUT_DIR, ignore_errors=True)
shutil.copytree(BUILD_DIR, OUTPUT_DIR)