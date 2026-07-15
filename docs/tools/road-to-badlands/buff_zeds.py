#!/usr/bin/env python3
"""Increase every zombie zone's dmin/dmax by 1, skipping zones with dmax=0."""
import re
import sys

def buff(m: re.Match) -> str:
    dmin, dmax = int(m.group(1)), int(m.group(2))
    if dmax == 0:
        return m.group(0)
    return f'dmin="{dmin + 1}" dmax="{dmax + 1}"'

def transform(text: str) -> str:
    return re.sub(r'dmin="(\d+)" dmax="(\d+)"', buff, text)

if __name__ == "__main__":
    path = sys.argv[1]
    # newline="" disables newline translation on read AND write, so the file's
    # original line endings (this file is CRLF) are preserved byte-for-byte.
    with open(path, encoding="utf-8", newline="") as f:
        original = f.read()
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(transform(original))
    print(f"buff applied to {path}")
