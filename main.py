"""Ship the finished front page to the grader's output folder.

The picture itself is drawn by build_image.py at build time; this file only
hands the finished entry.png over to the directory the grader names in
MAKEFUN_OUTPUT_DIR. Standard library only: no drawing, no network.
"""

import os
import shutil
import sys
from pathlib import Path

SOURCE_NAME = "entry.png"


def _die(message):
    sys.stderr.write("main.py: " + message + "\n")
    return 1


def _locate_source():
    here = Path(__file__).resolve().parent
    candidate = here / SOURCE_NAME
    if not candidate.exists():
        return None
    return candidate


def _output_folder():
    raw = os.environ.get("MAKEFUN_OUTPUT_DIR", "").strip()
    if not raw:
        return None
    return Path(raw)


def run():
    source = _locate_source()
    if source is None:
        return _die("entry.png is missing next to main.py; nothing to "
                    "deliver.")
    folder = _output_folder()
    if folder is None:
        return _die("MAKEFUN_OUTPUT_DIR is not set, so there is nowhere to "
                    "put entry.png.")
    folder.mkdir(parents=True, exist_ok=True)
    target = folder / SOURCE_NAME
    shutil.copyfile(source, target)
    size = target.stat().st_size
    print("delivered " + str(target) + " (" + str(size) + " bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
