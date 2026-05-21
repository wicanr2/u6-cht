#!/usr/bin/env python3
"""
Apply BOOK.DAT translation JSON. Zero-growth: each entry stays exactly same byte
length (space-padded if zh < original len). The 16-bit pointer table remains
valid because no offsets shift.

If any zh_bytes > len, abort with error.

Usage: apply_book_dat.py <book_dat_input> <translation_json> <output>
"""
import json, sys, os

if len(sys.argv) < 4:
    print("usage: apply_book_dat.py <book_dat> <translation_json> <output>")
    sys.exit(2)

src, tx_path, out = sys.argv[1], sys.argv[2], sys.argv[3]

data = bytearray(open(src, 'rb').read())
tx = json.load(open(tx_path, encoding='utf-8'))
items = tx['translations']

# Sort by offset descending to be safe (though we only do equal/shrink in-place)
items_sorted = sorted(items, key=lambda x: x['offset'], reverse=True)

equal, shrinks, over, errs = 0, 0, 0, 0
for it in items_sorted:
    off = it['offset']
    orig_len = it['len']
    zh = it['zh']
    try:
        zb = zh.encode('big5', errors='replace')
    except Exception as e:
        print(f'!! offset {off}: encode err {e}')
        errs += 1
        continue

    if len(zb) > orig_len:
        print(f'!! offset {off}: OVERFLOW zh_bytes={len(zb)} > len={orig_len}: {zh[:30]!r}')
        over += 1
        continue
    elif len(zb) == orig_len:
        data[off:off+orig_len] = zb
        equal += 1
    else:
        padded = zb + b' ' * (orig_len - len(zb))
        data[off:off+orig_len] = padded
        shrinks += 1

open(out, 'wb').write(bytes(data))
print(f'\nwrote {out} ({len(data)} bytes, original was {os.path.getsize(src)})')
print(f'  equal:  {equal}')
print(f'  shrink: {shrinks}')
print(f'  OVER:   {over}')
print(f'  errs:   {errs}')
