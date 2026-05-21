#!/usr/bin/env python3
"""
9px Big5 font generator — render AR PL UMing outline at 9 pixels, threshold
to 1-bit, place in same 12-row × 2-byte container so engine layout unchanged.

Output file structure matches build-big5-font-wqysharp.py 的 14758 slots ×
24 bytes/glyph = 354192 bytes total. 內容只佔上方 9 rows，下方 3 rows 留白。
"""
import sys, os
from freetype import Face, FT_LOAD_RENDER

# AR PL UMing has no 9px embedded; render outline at 9px with grayscale,
# threshold to 1-bit. UMing 是 Han 字型，比 WQY outline 更清晰於小尺寸。
FONT = '/usr/share/fonts/truetype/arphic/uming.ttc'
OUT  = sys.argv[1] if len(sys.argv) > 1 else '/home/anr2/u6-cht/dumps/big5_u6_9x12.fnt'
PX   = 9
THRESHOLD = 96  # 0-255 grayscale → 1-bit cutoff

NUM_LEAD = 94
NUM_TRAIL = 157
GLYPH_BYTES = 24      # 12 rows * 2 bytes (kept for engine compat)
TOTAL_SLOTS = NUM_LEAD * NUM_TRAIL
TOTAL_BYTES = TOTAL_SLOTS * GLYPH_BYTES

CONTENT_ROWS = 12  # we'll fit 9px content inside, top-aligned


def trail_offset(t):
    if 0x40 <= t <= 0x7E: return t - 0x40
    if 0xA1 <= t <= 0xFE: return t - 0xA1 + 63
    return None


def linear_index(lead, trail):
    to = trail_offset(trail)
    if to is None: return None
    return (lead - 0xA1) * NUM_TRAIL + to


def render_glyph(face, codepoint):
    try:
        face.load_char(codepoint, FT_LOAD_RENDER)  # grayscale
    except Exception:
        return bytes(GLYPH_BYTES)
    bmp = face.glyph.bitmap
    rows = bmp.rows
    width = bmp.width
    pitch = bmp.pitch
    buf = bmp.buffer
    if rows == 0 or width == 0:
        return bytes(GLYPH_BYTES)

    out = bytearray(GLYPH_BYTES)
    # Top-align in 12-row container — keep at ascent line.
    # UMing 9px ascent ~ 8, descent ~ 1.
    dst_y_start = max(0, 8 - face.glyph.bitmap_top)

    for src_y in range(rows):
        dst_y = dst_y_start + src_y
        if dst_y < 0 or dst_y >= CONTENT_ROWS:
            continue
        for col in range(min(width, 12)):
            g = buf[src_y * pitch + col]
            if g >= THRESHOLD:
                out[dst_y * 2 + (col >> 3)] |= (0x80 >> (col & 7))
    return bytes(out)


def b5_to_unicode_map():
    t = {}
    for lead in range(0xA1, 0xFF):
        for trail in list(range(0x40, 0x7F)) + list(range(0xA1, 0xFF)):
            try:
                t[(lead, trail)] = ord(bytes([lead, trail]).decode('big5'))
            except UnicodeDecodeError:
                pass
    return t


def main():
    face = Face(FONT, 0)
    face.set_pixel_sizes(PX, PX)
    print(f'font: {face.family_name.decode()} @ {PX}px outline → 1-bit threshold {THRESHOLD}')
    b5map = b5_to_unicode_map()
    print(f'Big5 codepoints mapped: {len(b5map):,}')
    out = bytearray(TOTAL_BYTES)
    rendered = blank = 0
    for (lead, trail), cp in b5map.items():
        idx = linear_index(lead, trail)
        if idx is None: continue
        g = render_glyph(face, cp)
        if any(g): rendered += 1
        else: blank += 1
        off = idx * GLYPH_BYTES
        out[off:off+GLYPH_BYTES] = g
    with open(OUT, 'wb') as f: f.write(out)
    print(f'wrote {OUT}: {len(out):,} bytes ({rendered} rendered, {blank} blank-mapped)')


if __name__ == '__main__':
    main()
