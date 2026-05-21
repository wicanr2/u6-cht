#!/usr/bin/env python3
"""
Extract one NPC's printable ASCII strings with offsets + context,
output as JSON suitable for handing to the Translator agent.

Usage: extract_npc_strings.py <conv_file>
"""
import sys, os, re, json

if len(sys.argv) < 2:
    print("usage: extract_npc_strings.py <conv_file>")
    sys.exit(2)

path = sys.argv[1]
data = open(path, 'rb').read()
name = os.path.basename(path)

strings = []
i = 0
while i < len(data):
    if 0x20 <= data[i] <= 0x7E:
        j = i
        while j < len(data) and 0x20 <= data[j] <= 0x7E:
            j += 1
        run = data[i:j].decode('ascii')
        # Skip very short fragments (usually 1-char opcodes' immediate values)
        if len(run) >= 2:
            strings.append({
                'offset': i,
                'len': j - i,
                'text': run,
            })
        i = j
    else:
        i += 1

print(json.dumps({'file': name, 'size': len(data), 'strings': strings},
                 ensure_ascii=False, indent=2))
