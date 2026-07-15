#!/usr/bin/env python3
"""Halve nominal/min (round up) on every <type> in db/types.xml except
types flagged deloot="1" or carrying a <usage name="ContaminatedArea"/>."""
import re
import sys

def ceil_half(n: int) -> int:
    return -(-n // 2)  # integer ceil: 1->1, 2->1, 3->2, 0->0

def nerf_block(m: re.Match) -> str:
    block = m.group(0)
    if 'deloot="1"' in block or 'name="ContaminatedArea"' in block:
        return block
    block = re.sub(r'(<nominal>)(\d+)(</nominal>)',
                   lambda x: f'{x.group(1)}{ceil_half(int(x.group(2)))}{x.group(3)}', block)
    block = re.sub(r'(<min>)(\d+)(</min>)',
                   lambda x: f'{x.group(1)}{ceil_half(int(x.group(2)))}{x.group(3)}', block)
    return block

def transform(text: str) -> str:
    return re.sub(r'<type name=.*?</type>', nerf_block, text, flags=re.DOTALL)

if __name__ == "__main__":
    path = sys.argv[1]
    with open(path, encoding="utf-8") as f:
        original = f.read()
    with open(path, "w", encoding="utf-8") as f:
        f.write(transform(original))
    print(f"nerf applied to {path}")
