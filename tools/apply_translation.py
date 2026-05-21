#!/usr/bin/env python3
"""
Apply translator-agent output JSON to a .conv file.

For each translation entry:
  - Encode zh as Big5
  - If zh_bytes == original len: in-place byte replace (safe, no offset shift)
  - If zh_bytes < original len: replace + pad with spaces to original len
  - If zh_bytes > original len: WARN — needs growable repack via pack_converse tool

Output: <conv>.zh — patched .conv file. Re-run unpack_conv -r to bundle into converse.a.

Usage: apply_translation.py <conv_file> <translation_json>
"""
import sys, os, json

if len(sys.argv) < 3:
    print("usage: apply_translation.py <conv_file> <translation_json>")
    sys.exit(2)

conv_path, json_path = sys.argv[1], sys.argv[2]
data = bytearray(open(conv_path, 'rb').read())
tx = json.load(open(json_path, encoding='utf-8'))

# tx may be {translations: [...]} or top-level array
items = tx['translations'] if isinstance(tx, dict) and 'translations' in tx else tx

warnings, shrinks, equal, growth = 0, 0, 0, 0
total_delta = 0

# Apply in REVERSE offset order so earlier offsets don't shift
items_sorted = sorted(items, key=lambda x: x['offset'], reverse=True)

for it in items_sorted:
    off = it['offset']
    orig_len = it['len']
    en = it.get('en', '')
    zh = it['zh']

    # Sanity check: original bytes match
    orig_bytes = bytes(data[off:off+orig_len])
    try:
        orig_str = orig_bytes.decode('ascii')
    except UnicodeDecodeError:
        print(f"!! offset {off}: not pure ASCII, skipping")
        warnings += 1
        continue
    if en and orig_str != en:
        print(f"!! offset {off}: EN mismatch — file has {orig_str!r}, json expects {en!r}")
        warnings += 1
        continue

    # Encode zh as Big5
    try:
        zh_bytes = zh.encode('big5', errors='replace')
    except Exception as e:
        print(f"!! offset {off}: encode err {e}")
        warnings += 1
        continue

    if len(zh_bytes) == orig_len:
        data[off:off+orig_len] = zh_bytes
        equal += 1
    elif len(zh_bytes) < orig_len:
        # Pad with spaces to original len (keeps offsets stable)
        padded = zh_bytes + b' ' * (orig_len - len(zh_bytes))
        data[off:off+orig_len] = padded
        shrinks += 1
    else:
        # Growth — let pack_conv handle (different file, no offsets stored separately)
        delta = len(zh_bytes) - orig_len
        total_delta += delta
        # In-place grow: insert extra bytes, push the rest right
        data[off:off+orig_len] = zh_bytes
        growth += 1
        print(f"   grow @{off}: {orig_len} -> {len(zh_bytes)} bytes (+{delta})")

# Write output
out_path = conv_path + '.zh'
open(out_path, 'wb').write(bytes(data))

print(f"\nwrote {out_path} ({len(data)} bytes, original was {os.path.getsize(conv_path)})")
print(f"  equal:  {equal}")
print(f"  shrink: {shrinks}  (space-padded)")
print(f"  grow:   {growth}   (+{total_delta} bytes total)")
print(f"  warn:   {warnings}")
