#!/usr/bin/env python3
"""
Big5 點陣字生成器（u6-cht v1.0 預設配置）

預設用 **AR PL UMing 11px embedded bitmap**（單色 1-bit、字劃清晰、比 WQY 12px 縮小一格）。
其它選項：
    --font wqy-sharp   --size {12,13,14,15,16}
    --font uming       --size {11,12,13,14,15,16}

輸出檔名固定 `big5_u6_12x12.fnt`（即使內容是 11px；engine 預期此檔名），格式：
    94 leads × 157 trails × 24 bytes/glyph = 354192 bytes
    每 glyph 12 rows × 2 bytes (MSB-first)，內容靠頂端對齊，下方空 row 留白
"""
import sys, os, argparse
from freetype import Face, FT_LOAD_RENDER, FT_LOAD_MONOCHROME, FT_LOAD_TARGET_MONO

# 預設：AR PL UMing 11px embedded（u6-cht v1.0 取代 WQY 12px 的決定，見 README）
DEFAULT_FONT = '/usr/share/fonts/truetype/arphic/uming.ttc'
DEFAULT_FACE_IDX = 0
DEFAULT_SIZE = 11

NUM_LEAD = 94
NUM_TRAIL = 157
GLYPH_BYTES = 24
TOTAL_SLOTS = NUM_LEAD * NUM_TRAIL
TOTAL_BYTES = TOTAL_SLOTS * GLYPH_BYTES

FONT_PRESETS = {
    'uming':     ('/usr/share/fonts/truetype/arphic/uming.ttc',     0),
    'wqy-sharp': ('/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc',   2),
}


def trail_offset(t):
    if 0x40 <= t <= 0x7E: return t - 0x40
    if 0xA1 <= t <= 0xFE: return t - 0xA1 + 63
    return None


def linear_index(lead, trail):
    to = trail_offset(trail)
    if to is None: return None
    return (lead - 0xA1) * NUM_TRAIL + to


def render_glyph(face, codepoint, top_align_y):
    try:
        face.load_char(codepoint, FT_LOAD_RENDER | FT_LOAD_MONOCHROME | FT_LOAD_TARGET_MONO)
    except Exception:
        return bytes(GLYPH_BYTES)
    bmp = face.glyph.bitmap
    rows, width, pitch = bmp.rows, bmp.width, bmp.pitch
    buf = bmp.buffer
    if rows == 0 or width == 0:
        return bytes(GLYPH_BYTES)
    dst_y_start = top_align_y - face.glyph.bitmap_top
    out = bytearray(GLYPH_BYTES)
    for src_y in range(rows):
        dst_y = dst_y_start + src_y
        if dst_y < 0 or dst_y >= 12:
            continue
        for col in range(min(width, 12)):
            byte = buf[src_y * pitch + (col >> 3)]
            if byte & (0x80 >> (col & 7)):
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
    ap = argparse.ArgumentParser()
    ap.add_argument('--font', choices=list(FONT_PRESETS.keys()), default='uming',
                    help='font preset (default: uming)')
    ap.add_argument('--size', type=int, default=DEFAULT_SIZE,
                    help='pixel size (default: 11). Must be in embedded sizes.')
    ap.add_argument('-o', '--output', default='/home/anr2/u6-cht/working/game/big5_u6_12x12.fnt')
    args = ap.parse_args()

    font_path, face_idx = FONT_PRESETS[args.font]
    face = Face(font_path, face_idx)
    embedded_sizes = sorted({s.size // 64 for s in face.available_sizes})
    if args.size not in embedded_sizes:
        print(f'ERROR: {args.font} embedded sizes are {embedded_sizes}, requested {args.size}')
        sys.exit(1)
    for i, s in enumerate(face.available_sizes):
        if s.size // 64 == args.size:
            face.select_size(i); break

    # Top-align in 12-row container: ascent depends on font/size
    top_align = max(args.size - 2, 8)  # heuristic: leave 1 row above for ascenders

    print(f'font: {face.family_name.decode()} @ {args.size}px embedded bitmap (1-bit)')
    print(f'output: {args.output}')

    b5map = b5_to_unicode_map()
    out = bytearray(TOTAL_BYTES)
    n = 0
    for (lead, trail), cp in b5map.items():
        idx = linear_index(lead, trail)
        if idx is None: continue
        g = render_glyph(face, cp, top_align)
        if any(g): n += 1
        off = idx * GLYPH_BYTES
        out[off:off+GLYPH_BYTES] = g

    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    open(args.output, 'wb').write(out)
    print(f'wrote {len(out):,} bytes ({n} glyphs rendered)')


if __name__ == '__main__':
    main()
