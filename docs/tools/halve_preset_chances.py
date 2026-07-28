#!/usr/bin/env python3
"""Halve the preset-level chance on every <cargo> and <attachments> preset
in cfgrandompresets.xml. Item-level <item ... chance="..."> values are left
untouched."""
import re
import sys
import xml.etree.ElementTree as ET

# \s* after '=' matters: vanilla has '<attachments chance= "0.03" name="headtorches">'
PRESET_CHANCE = re.compile(r'(<(?:cargo|attachments) chance=\s*")([0-9.]+)(")')

def halve(value: str) -> str:
    if float(value) == 0:
        return value  # already-disabled preset; keep formatting untouched
    return "%g" % (float(value) / 2)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(f"usage: {sys.argv[0]} <xml-file>")
    path = sys.argv[1]
    with open(path, encoding="utf-8", newline="") as f:
        original = f.read()

    # independent count via a real XML parse, so a regex miss can't hide itself
    expected = sum(1 for el in ET.fromstring(original).iter()
                   if el.tag in ("cargo", "attachments") and "chance" in el.attrib)
    new_text, n = PRESET_CHANCE.subn(
        lambda m: f"{m.group(1)}{halve(m.group(2))}{m.group(3)}", original)
    if n != expected:
        sys.exit(
            f"ABORT: matched {n} preset chance attributes but found {expected} "
            f"occurrences in {path}; refusing to write (possible format change)"
        )

    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(new_text)
    print(f"preset chances halved in {path} ({n} presets)")
