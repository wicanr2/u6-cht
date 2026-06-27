#!/usr/bin/env python3
"""
Build a 16x16 Big5 bitmap font for U6 CHT v2.0, sourced from WenQuanYi Zen Hei
Sharp embedded bitmap (face index 2, size 16).

Layout (file: big5_u6_16x16.fnt):
  Each char = 16 rows * 2 bytes/row (16 bits MSB-first, no padding)
              = 32 bytes/char
  Linear index:
      num_trail = (0x7E - 0x40 + 1) + (0xFE - 0xA1 + 1) = 63 + 94 = 157
      num_lead  = 0xFE - 0xA1 + 1                       = 94
      idx(lead,trail) = (lead - 0xA1) * 157 +
                        (trail - 0x40        if trail <= 0x7E else
                         trail - 0xA1 + 63)
      total slots = 94 * 157 = 14758
      file size   = 14758 * 32 = 472_256 bytes
"""
import sys, os
from freetype import Face, FT_LOAD_RENDER, FT_LOAD_MONOCHROME, FT_LOAD_TARGET_MONO

WQY = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
OUT = sys.argv[1] if len(sys.argv) > 1 else '/home/anr2/u6-cht/dumps/big5_u6_16x16.fnt'

NUM_LEAD = 94                       # 0xA1..0xFE
NUM_TRAIL = 157                     # 0x40..0x7E (63) + 0xA1..0xFE (94)
GLYPH_BYTES = 32                    # 16 rows * 2 bytes
TOTAL_SLOTS = NUM_LEAD * NUM_TRAIL   # 14758
TOTAL_BYTES = TOTAL_SLOTS * GLYPH_BYTES  # 472_256

GLYPH_W = 16
GLYPH_H = 16


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
    """Render a Unicode codepoint to 16x16 monochrome.  Returns 32 bytes (MSB-first, 16 bits per row)."""
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

    # WQY Zen Hei Sharp 16px embedded: ascent ~13, descent ~3.
    # bitmap_top is the distance from baseline to top of bitmap.
    # We want the glyph anchored so the top of the rendered area aligns near row 0
    # with a small breathing room. For 16px the typical bitmap_top is 13.
    top = face.glyph.bitmap_top
    # row_offset: where in the 16-row output buffer the top of this bitmap goes
    row_offset = max(0, 13 - top)  # 13 = ideal ascent for 16px
    left_offset = max(0, face.glyph.bitmap_left)

    out = bytearray(GLYPH_BYTES)
    for r in range(min(rows, GLYPH_H - row_offset)):
        dst_row = row_offset + r
        if dst_row >= GLYPH_H:
            break
        bits = 0
        for c in range(min(width, GLYPH_W - left_offset)):
            byte = buf[r * pitch + (c // 8)]
            bit = (byte >> (7 - (c % 8))) & 1
            if bit:
                dst_c = left_offset + c
                if dst_c < GLYPH_W:
                    bits |= 1 << (15 - dst_c)
        out[dst_row * 2]     = (bits >> 8) & 0xFF
        out[dst_row * 2 + 1] = bits & 0xFF
    return bytes(out)


def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    face = Face(WQY, 2)  # face index 2 = WenQuanYi Zen Hei Sharp

    # Select embedded 16px bitmap
    found = False
    for i, s in enumerate(face.available_sizes):
        if s.size // 64 == 16:
            face.select_size(i)
            found = True
            break
    if not found:
        print('ERROR: WQY zenhei Sharp 16px embedded bitmap not found', file=sys.stderr)
        sys.exit(1)

    out = bytearray(TOTAL_BYTES)
    slot_count = 0
    nonempty = 0
    for lead in range(0xA1, 0xFF):
        for trail in list(range(0x40, 0x7F)) + list(range(0xA1, 0xFF)):
            slot = linear_index(lead, trail)
            if slot is None:
                continue
            slot_count += 1
            # Decode Big5 lead+trail -> Unicode codepoint
            try:
                ch = bytes([lead, trail]).decode('big5')
            except UnicodeDecodeError:
                continue
            if len(ch) != 1:
                continue
            glyph = render_glyph(face, ch)
            if any(glyph):
                nonempty += 1
            out[slot * GLYPH_BYTES:(slot + 1) * GLYPH_BYTES] = glyph

    with open(OUT, 'wb') as f:
        f.write(out)

    print(f'wrote {OUT}: {len(out)} bytes, {nonempty}/{slot_count} non-empty glyphs')


if __name__ == '__main__':
    main()
