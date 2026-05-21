#!/usr/bin/env python3
"""
產生 3 個 Big5 字型 size 預覽圖，user 比較哪個喜歡。
"""
from freetype import Face, FT_LOAD_RENDER, FT_LOAD_MONOCHROME, FT_LOAD_TARGET_MONO
from PIL import Image, ImageDraw, ImageFont

SAMPLE = "汝見地板。對話-不列顛王。Iolo 擦傷。"

CANDIDATES = [
    ("WQY Sharp 12px (current)",
     '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc', 2, 12),
    ("AR PL UMing 11px (1px smaller)",
     '/usr/share/fonts/truetype/arphic/uming.ttc', 0, 11),
    ("WQY Sharp 12px scaled-down→10px",
     '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc', 2, 10),  # outline at 10
]

def render(face_path, face_idx, px, text):
    face = Face(face_path, face_idx)
    # Try embedded bitmap first; fallback to outline at requested px
    embedded = None
    for s in face.available_sizes:
        if s.size//64 == px:
            embedded = s
            break
    if embedded:
        for i, s in enumerate(face.available_sizes):
            if s.size//64 == px:
                face.select_size(i)
                break
    else:
        face.set_pixel_sizes(px, px)
    cells = []
    for ch in text:
        try:
            face.load_char(ch, FT_LOAD_RENDER | FT_LOAD_MONOCHROME | FT_LOAD_TARGET_MONO)
        except:
            continue
        bmp = face.glyph.bitmap
        cells.append((ch, bmp.rows, bmp.width, bmp.pitch, bytes(bmp.buffer),
                      face.glyph.bitmap_top, face.glyph.bitmap_left))
    return cells

def to_image(cells, px, label):
    line_h = px + 2
    total_w = sum(c[2] + 2 for c in cells) + 20
    img = Image.new('RGB', (total_w * 4, line_h * 6 + 30), 'white')
    draw = ImageDraw.Draw(img)
    # Scale 4x for visibility
    SCALE = 4
    x = 4 * SCALE
    y_base = 18 * SCALE
    draw.text((4, 2), f"{label} (each pixel scaled x{SCALE})", fill='black')
    for ch, h, w, pitch, buf, top, left in cells:
        for sy in range(h):
            for sx in range(w):
                byte = buf[sy * pitch + (sx >> 3)]
                bit = byte & (0x80 >> (sx & 7))
                if bit:
                    px_x = (x + sx) * SCALE
                    px_y = (y_base + sy - top + px) * SCALE
                    draw.rectangle([px_x, px_y, px_x+SCALE-1, px_y+SCALE-1], fill='black')
        x += w + 2
    return img

for label, path, idx, px in CANDIDATES:
    fn = label.split()[0].lower().replace(' ', '_').replace('(', '').replace(')', '')
    out = f'/tmp/font_preview_{px}_{fn}.png'
    cells = render(path, idx, px, SAMPLE)
    img = to_image(cells, px, label)
    img.save(out)
    print(f'{label} → {out}')
