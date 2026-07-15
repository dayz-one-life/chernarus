#!/usr/bin/env python3
"""Increase every zombie zone's dmin/dmax by 1, skipping zones with dmax=0."""
import re
import sys

ZONE_DENSITY = re.compile(r'dmin="(\d+)" dmax="(\d+)"')

def buff(m: re.Match) -> str:
    dmin, dmax = int(m.group(1)), int(m.group(2))
    if dmax == 0:
        return m.group(0)
    return f'dmin="{dmin + 1}" dmax="{dmax + 1}"'

def transform(text: str) -> str:
    return ZONE_DENSITY.sub(buff, text)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(f"usage: {sys.argv[0]} <xml-file>")
    path = sys.argv[1]
    # newline="" disables newline translation on read AND write, so the file's
    # original line endings (this file is CRLF) are preserved byte-for-byte.
    with open(path, encoding="utf-8", newline="") as f:
        original = f.read()

    expected = original.count('<zone ')
    new_text, n = ZONE_DENSITY.subn(buff, original)
    if n != expected:
        sys.exit(
            f"ABORT: matched {n} dmin/dmax pairs but found {expected} '<zone ' "
            f"occurrences in {path}; refusing to write (possible format change)"
        )

    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(new_text)
    print(f"buff applied to {path} ({n} zones)")
