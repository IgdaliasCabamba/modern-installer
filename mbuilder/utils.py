import sys
import os
from rich.console import *
from rich.panel import *
from rich.markdown import *
from rich.prompt import *
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn, TimeElapsedColumn
from rich.padding import *
import shutil
import time
import tarfile
import pathlib

if getattr(sys, "frozen", False):
    root_path = os.path.dirname(os.path.realpath(sys.executable))
else:
    root_path = os.path.dirname(os.path.realpath(__file__))

VERSION = "0.0.1 (Alpha)"

MENU = """[bold]
1 New Project
2 Help
3 Exit
"""

HELP_AND_CREDITS = """
"""

MAIN_FILE = os.path.join(root_path, "res", "main.py")
BACKEND_FILE = os.path.join(root_path, "res", "backend.py")
SPEC_FILE = os.path.join(root_path, "res", "main.spec")
INIT_TEMPLATE = os.path.join(root_path, "res", "templates", "init", "static")

def make_tarfile(output_filename, source_dir):
    with tarfile.open(output_filename, "w:xz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))