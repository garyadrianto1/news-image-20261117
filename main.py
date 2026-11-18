#!/usr/bin/env python3
"""news-image-20261117 entry (Python 3.13, standard library only).

The entry image is the entry.png beside this file, and the program copies
it to /output/entry.png. The gate takes a whole PNG or JPEG of at most
1 MiB and 1024 by 1024 pixels, and the judge sees exactly the bytes copied.

Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))

OUT.mkdir(parents=True, exist_ok=True)
shutil.copyfile(HERE / "entry.png", OUT / "entry.png")
