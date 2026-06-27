#!/usr/bin/env python3
"""
Dump ASCII art glyphs from u6cht binary .fnt files for visual diff.

Usage:
  dump_font_glyph.py <chars> [--12 PATH] [--16 PATH]

Default paths:
  --12  working/game/big5_u6_12x12.fnt
  --16  dumps/big5_u6_16x16.fnt
"""
import sys, os, argparse

NUM_TRAIL = 157

def trail_offset(trail):
    if 0x40 <= trail <= 0x7E: return trail - 0x40
    if 0xA1 <= trail <= 0xFE: return trail - 0xA1 + 63
    return None

def linear_index(lead, trail):
    to = trail_offset(trail)
    if to is None: return None
    return (lead - 0xA1) * NUM_TRAIL + to


def render_glyph(data, slot, rows, glyph_bytes):
    bytes_per_row = glyph_bytes // rows
    bits_per_row = bytes_per_row * 8
    g = data[slot * glyph_bytes : (slot + 1) * glyph_bytes]
    out = []
    for r in range(rows):
        bits = 0
        for b in range(bytes_per_row):
            bits = (bits << 8) | g[r * bytes_per_row + b]
        line = ''.join('█' if (bits >> (bits_per_row - 1 - c)) & 1 else '·'
                       for c in range(bits_per_row))
        out.append(line)
    return out


def render_for_size(path, ch, size_label, rows, glyph_bytes):
    with open(path, 'rb') as f:
        data = f.read()
    b = ch.encode('big5')
    lead, trail = b[0], b[1]
    slot = linear_index(lead, trail)
    lines = render_glyph(data, slot, rows, glyph_bytes)
    bytes_per_row = glyph_bytes // rows
    bits_per_row = bytes_per_row * 8
    header = f'{ch} ({size_label}, Big5 {b.hex()}, slot {slot})'
    return header, lines


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('chars')
    ap.add_argument('--12', dest='fnt12', default='working/game/big5_u6_12x12.fnt')
    ap.add_argument('--16', dest='fnt16', default='dumps/big5_u6_16x16.fnt')
    args = ap.parse_args()

    for ch in args.chars:
        print(f'\n========== {ch} ==========')
        try:
            h12, l12 = render_for_size(args.fnt12, ch, '12×12', 12, 24)
        except Exception as e:
            print(f'12×12 FAIL: {e}'); l12 = None
        try:
            h16, l16 = render_for_size(args.fnt16, ch, '16×16', 16, 32)
        except Exception as e:
            print(f'16×16 FAIL: {e}'); l16 = None

        # side-by-side: pad 12-line block to 16 lines
        if l12 and l16:
            print(f'  {h12:<40} | {h16}')
            l12_padded = l12 + ['············'] * (16 - len(l12))
            for a, b in zip(l12_padded, l16):
                print(f'  {a}                             | {b}')
        elif l12:
            print(f'  {h12}')
            for line in l12: print(f'  {line}')
        elif l16:
            print(f'  {h16}')
            for line in l16: print(f'  {line}')


if __name__ == '__main__':
    main()
