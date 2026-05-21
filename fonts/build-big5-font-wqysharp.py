#!/usr/bin/env python3
"""
Build a 12x12 Big5 bitmap font for U6 CHT, sourced from WenQuanYi Zen Hei
Sharp embedded bitmap (face index 2, size 0 = 12px).

Layout (file: big5_u6_12x12.fnt):
  Each char = 12 rows * 2 bytes/row (12 bits + 4 bit padding, MSB-first)
              = 24 bytes/char
  Linear index:
      num_trail = (0x7E - 0x40 + 1) + (0xFE - 0xA1 + 1) = 63 + 94 = 157
      num_lead  = 0xFE - 0xA1 + 1                       = 94
      idx(lead,trail) = (lead - 0xA1) * 157 +
                        (trail - 0x40        if trail <= 0x7E else
                         trail - 0xA1 + 63)
      total slots = 94 * 157 = 14758
      file size   = 14758 * 24 = 354_192 bytes
"""
import sys, os
from freetype import Face, FT_LOAD_RENDER, FT_LOAD_MONOCHROME, FT_LOAD_TARGET_MONO

WQY = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
OUT = sys.argv[1] if len(sys.argv) > 1 else '/home/anr2/u6-cht/dumps/big5_u6_12x12.fnt'

NUM_LEAD = 94                       # 0xA1..0xFE
NUM_TRAIL = 157                     # 0x40..0x7E (63) + 0xA1..0xFE (94)
GLYPH_BYTES = 24                    # 12 rows * 2 bytes
TOTAL_SLOTS = NUM_LEAD * NUM_TRAIL   # 14758
TOTAL_BYTES = TOTAL_SLOTS * GLYPH_BYTES  # 354_192


def trail_offset(trail):
    if 0x40 <= trail <= 0x7E:
        return trail - 0x40
    if 0xA1 <= trail <= 0xFE:
        return trail - 0xA1 + 63
    return None


def linear_index(lead, trail):
    to = trail_offset(trail)
    if to is None:
        return None
    return (lead - 0xA1) * NUM_TRAIL + to


def render_glyph(face, codepoint):
    """Render a Unicode codepoint to 12x12 monochrome.  Returns 24 bytes."""
    try:
        face.load_char(codepoint, FT_LOAD_RENDER | FT_LOAD_MONOCHROME | FT_LOAD_TARGET_MONO)
    except Exception:
        return bytes(GLYPH_BYTES)
    bmp = face.glyph.bitmap
    rows = bmp.rows
    width = bmp.width
    pitch = bmp.pitch
    buf = bmp.buffer
    if rows == 0 or width == 0:
        return bytes(GLYPH_BYTES)

    # Baseline: WQY Sharp 12px ascent ~10, descent ~2; align top so bitmap_top maps near 10.
    dst_y_start = 10 - face.glyph.bitmap_top
    out = bytearray(GLYPH_BYTES)
    for src_y in range(rows):
        dst_y = dst_y_start + src_y
        if dst_y < 0 or dst_y >= 12:
            continue
        src_row_off = src_y * pitch
        # Render up to 12 columns wide
        for col in range(min(width, 12)):
            byte = buf[src_row_off + (col >> 3)]
            bit = byte & (0x80 >> (col & 7))
            if bit:
                out[dst_y * 2 + (col >> 3)] |= (0x80 >> (col & 7))
    return bytes(out)


def b5_to_unicode_map():
    """Build Big5 -> Unicode lookup via Python's cp950 (≈ Big5)."""
    table = {}
    for lead in range(0xA1, 0xFF):
        for trail in list(range(0x40, 0x7F)) + list(range(0xA1, 0xFF)):
            two = bytes([lead, trail])
            try:
                ch = two.decode('big5')
                table[(lead, trail)] = ord(ch)
            except UnicodeDecodeError:
                pass
    return table


def main():
    face = Face(WQY, 2)   # face 2 = Sharp
    face.select_size(0)   # 12px embedded bitmap
    print(f"face: {face.family_name.decode()}, embedded sizes: {[(s.size, s.width, s.height) for s in face.available_sizes]}")

    b5map = b5_to_unicode_map()
    print(f"Big5 codepoints mapped: {len(b5map):,}")

    out = bytearray(TOTAL_BYTES)
    rendered = 0
    blank = 0
    for (lead, trail), cp in b5map.items():
        idx = linear_index(lead, trail)
        if idx is None:
            continue
        g = render_glyph(face, cp)
        if any(g):
            rendered += 1
        else:
            blank += 1
        off = idx * GLYPH_BYTES
        out[off:off+GLYPH_BYTES] = g

    with open(OUT, 'wb') as f:
        f.write(out)
    print(f"Wrote {OUT}: {len(out):,} bytes ({TOTAL_SLOTS} slots, {rendered} rendered, {blank} blank-mapped)")


if __name__ == '__main__':
    main()
