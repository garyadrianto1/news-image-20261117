#!/usr/bin/env python3
"""news-image-20261117 entry (Python 3.13, standard library only).

The entry image is the entry.png beside this file, and the program copies
it to /output/entry.png. The gate takes a whole PNG or JPEG of at most
1 MiB and 1024 by 1024 pixels, and the judge sees exactly the bytes copied.

Validation (added in the fix round, after the round-1 rejection): before
copying, the program checks the file is a real PNG (magic bytes), is at
most 1 MiB, and its IHDR dimensions are at most 1024x1024. Any failure
aborts with a clear error instead of handing the gate a bad file. After
the copy it reads the output back and compares it byte for byte with the
source, so a truncated or failed copy is caught loudly.

The size check uses stat() and the header check reads only the first 33
bytes, so an oversized file is rejected without ever being loaded into
memory. Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for
/output:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import shutil
import struct
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))

MAX_BYTES = 1_048_576
MAX_DIM = 1024
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def fail(msg):
    print(f"main.py: ERROR: {msg}", file=sys.stderr)
    raise SystemExit(1)


def validate_png(path):
    try:
        size = path.stat().st_size
    except OSError as e:
        fail(f"cannot stat {path.name}: {e}")
    if size > MAX_BYTES:
        fail(f"{path.name} is {size} bytes, over the 1 MiB limit")
    if size < 33:
        fail(f"{path.name} is only {size} bytes, too short to be a PNG")
    with open(path, "rb") as f:
        head = f.read(33)
    if head[:8] != PNG_MAGIC:
        fail(f"{path.name} is not a PNG (bad magic bytes)")
    if head[12:16] != b"IHDR":
        fail(f"{path.name} has no PNG IHDR chunk")
    width, height = struct.unpack(">II", head[16:24])
    if width == 0 or height == 0:
        fail(f"{path.name} has a zero dimension")
    if width > MAX_DIM or height > MAX_DIM:
        fail(f"{path.name} is {width}x{height}, over the 1024x1024 limit")
    return width, height, size


def main():
    src = HERE / "entry.png"
    if not src.is_file():
        fail(f"{src} not found next to main.py")
    width, height, nbytes = validate_png(src)
    OUT.mkdir(parents=True, exist_ok=True)
    dst = OUT / "entry.png"
    shutil.copyfile(src, dst)
    # read back and compare: the gate must see exactly the source bytes.
    if dst.read_bytes() != src.read_bytes():
        fail(f"{dst} differs from {src.name} after copying")
    print(f"main.py: copied {src.name} ({width}x{height}, {nbytes} bytes) -> {dst}")


if __name__ == "__main__":
    main()
