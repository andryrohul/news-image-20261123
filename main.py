"""Deliver the finished front page for the 23 November 2026 news image entry.

The grader runs this file and expects exactly one artefact: entry.png,
placed inside the folder named by MAKEFUN_OUTPUT_DIR.  Nothing is drawn
here and nothing is fetched; the picture already exists beside this file
and is simply handed over, byte for byte.
"""

import os
import sys

PICTURE_NAME = "entry.png"
CHUNK = 1024 * 64


def _fail(message):
    print("main.py: " + message, file=sys.stderr)
    return 2


def _hand_over(source, target_folder):
    target_folder.mkdir(parents=True, exist_ok=True)
    destination = target_folder / PICTURE_NAME
    moved = 0
    with source.open("rb") as reader, destination.open("wb") as writer:
        while True:
            piece = reader.read(CHUNK)
            if not piece:
                break
            writer.write(piece)
            moved += len(piece)
    return destination, moved


def run():
    wanted = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not wanted:
        return _fail("MAKEFUN_OUTPUT_DIR is not set, so there is nowhere to put entry.png.")

    here = os.path.dirname(os.path.abspath(__file__))
    from pathlib import Path

    source = Path(here) / PICTURE_NAME
    if not source.is_file():
        return _fail("entry.png is missing next to main.py.")

    destination, moved = _hand_over(source, Path(wanted))
    print("delivered {} ({} bytes)".format(destination, moved))
    return 0


if __name__ == "__main__":
    sys.exit(run())
