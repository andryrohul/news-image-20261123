#!/usr/bin/env python3
"""Entry program for news-image-20261123 (Python 3.13, stdlib only).

The image is entry.png beside this file: a one-page newspaper front
page, "THE WORLD IN ONE DAY", summing up Monday 23 November 2026 in
36 date-checked stories across 6 regions. This program only copies it
to the output directory, so both grader runs write identical bytes.

Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for
/output:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import shutil


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(here, "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    print("wrote %s (%d bytes)" % (dst, os.path.getsize(dst)))


if __name__ == "__main__":
    main()
