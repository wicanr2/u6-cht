#!/usr/bin/env python3
"""
Walk every CONVERSE.A/B unpacked .conv file and extract printable ASCII
runs (>= 3 chars) as a translation worksheet.

Output: dumps/converse_strings.json
    [
      {"file": "002_Dupre.conv", "offset": 2, "len": 5, "text": "Dupre"},
      ...
    ]

We treat any byte in 0x20-0x7E as printable. Adjacent printables form a run.
We exclude bytes < 0x20 and >= 0x7F (control/opcode/multibyte zone).
"""
import os, json, glob, re

CONV_DIR = '/home/anr2/u6-cht/dumps/converse'
OUT_JSON = '/home/anr2/u6-cht/dumps/converse_strings.json'

MIN_LEN = 3
records = []
total_files = 0
total_bytes = 0

for path in sorted(glob.glob(os.path.join(CONV_DIR, '*.conv'))):
    total_files += 1
    data = open(path, 'rb').read()
    name = os.path.basename(path)
    i = 0
    while i < len(data):
        b = data[i]
        if 0x20 <= b <= 0x7E:
            j = i
            while j < len(data) and 0x20 <= data[j] <= 0x7E:
                j += 1
            run_len = j - i
            if run_len >= MIN_LEN:
                text = data[i:j].decode('ascii')
                records.append({
                    'file': name,
                    'offset': i,
                    'len': run_len,
                    'text': text,
                })
                total_bytes += run_len
            i = j
        else:
            i += 1

with open(OUT_JSON, 'w') as f:
    json.dump(records, f, ensure_ascii=False, indent=1)

print(f"{total_files} files, {len(records)} string runs, {total_bytes:,} text bytes")
print(f"-> {OUT_JSON}")

# Print histogram of lengths
from collections import Counter
hist = Counter()
for r in records:
    L = r['len']
    bucket = '1-9' if L < 10 else '10-29' if L < 30 else '30-99' if L < 100 else '100+'
    hist[bucket] += 1
print('Length distribution:', dict(hist))
