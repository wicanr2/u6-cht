#!/usr/bin/env python3
"""
Extract text entries from BOOK.DAT.

Structure: 16-bit LE pointer table at start (~128 entries), data follows.
Each pointer is offset into BOOK.DAT where that entry's text starts.
Entry ends at next entry's offset (or end-of-file).

Output: JSON with {offset, len, text} per entry — translator-ready format.
"""
import json, sys

PATH = '/home/anr2/u6-cht/ultima6/BOOK.DAT'
data = open(PATH, 'rb').read()

# Parse pointer table — pointers stored 16-bit LE
# First pointer is data start; pointer table ends when pointer >= data start
ptrs = []
data_start = None
i = 0
while i < 256:
    p = data[i] + (data[i+1] << 8)
    if data_start is None:
        data_start = p
    if i >= data_start - 2:
        break
    ptrs.append(p)
    i += 2

print(f'Pointer table: {len(ptrs)} entries, data starts at offset {data_start}', file=sys.stderr)

entries = []
for idx, ptr in enumerate(ptrs):
    next_ptr = ptrs[idx+1] if idx+1 < len(ptrs) else len(data)
    if next_ptr <= ptr:
        # End/sentinel
        continue
    blob = data[ptr:next_ptr]
    # Decode as ASCII; null-terminate if present
    end = blob.find(b'\x00')
    if end >= 0:
        blob = blob[:end]
    try:
        text = blob.decode('ascii', errors='replace')
    except:
        text = repr(blob)
    entries.append({
        'idx': idx,
        'offset': ptr,
        'len': len(blob),
        'text': text,
    })

# Filter out tiny entries (< 4 chars, likely sentinels or one-byte glyphs)
entries = [e for e in entries if e['len'] >= 4]

out = {'source': 'BOOK.DAT', 'entries': entries}
print(json.dumps(out, ensure_ascii=False, indent=1))
print(f'Extracted {len(entries)} entries (filter >=4 bytes)', file=sys.stderr)
