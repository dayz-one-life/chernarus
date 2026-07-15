#!/usr/bin/env python3
"""Halve nominal/min (round up) on every <type> in db/types.xml except
types flagged deloot="1" or carrying a <usage name="ContaminatedArea"/>."""
import re
import sys

TYPE_BLOCK = re.compile(r'<type name=.*?</type>', re.DOTALL)

def ceil_half(n: int) -> int:
    return -(-n // 2)  # integer ceil: 1->1, 2->1, 3->2, 0->0

def nerf_block(m: re.Match) -> str:
    block = m.group(0)
    if 'deloot="1"' in block or '<usage name="ContaminatedArea"' in block:
        return block
    block = re.sub(r'(<nominal>)(\d+)(</nominal>)',
                   lambda x: f'{x.group(1)}{ceil_half(int(x.group(2)))}{x.group(3)}', block)
    block = re.sub(r'(<min>)(\d+)(</min>)',
                   lambda x: f'{x.group(1)}{ceil_half(int(x.group(2)))}{x.group(3)}', block)
    return block

def transform(text: str) -> str:
    return TYPE_BLOCK.sub(nerf_block, text)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(f"usage: {sys.argv[0]} <xml-file>")
    path = sys.argv[1]
    with open(path, encoding="utf-8", newline="") as f:
        original = f.read()

    expected = original.count('<type name=')
    new_text, n = TYPE_BLOCK.subn(nerf_block, original)
    if n != expected:
        sys.exit(
            f"ABORT: matched {n} <type> blocks but found {expected} '<type name=' "
            f"occurrences in {path}; refusing to write (possible format change)"
        )

    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(new_text)
    print(f"nerf applied to {path} ({n} type blocks)")
