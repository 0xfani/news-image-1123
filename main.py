"""Entry for make.fun's news-image-20261123: "Sum up 23 November's world news in one image".

The picture is drawn ahead of time and committed as entry.png; this program only hands it over.
It copies entry.png to $MAKEFUN_OUTPUT_DIR (or /output in the make.fun sandbox) after checking
that it is a PNG and fits the 1 MiB cap, so both graded runs write the same bytes. Standard library only.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")
LIMIT = 1024 * 1024
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def main() -> int:
    with open(SOURCE, "rb") as fh:
        head = fh.read(8)
    if head != PNG_SIGNATURE:
        print("entry.png is not a PNG", file=sys.stderr)
        return 1
    if os.path.getsize(SOURCE) > LIMIT:
        print("entry.png is over 1 MiB", file=sys.stderr)
        return 1
    with open(SOURCE, "rb") as fh:
        fh.seek(16)
        width = int.from_bytes(fh.read(4), "big")
        height = int.from_bytes(fh.read(4), "big")
    if width > 1024 or height > 1024:
        print(f"entry.png is {width}x{height}, over 1024 px", file=sys.stderr)
        return 1
    target_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(target_dir, exist_ok=True)
    shutil.copyfile(SOURCE, os.path.join(target_dir, "entry.png"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
