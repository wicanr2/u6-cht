#!/usr/bin/env python3
"""Build README art from real U6 game data:
  1. docs/screenshots/britannia_map.png   — authentic overview map + 8 city pins
  2. docs/screenshots/npc/<name>.png       — NPC portrait icons (party + city reps)

Depends on tools/extract_u6_images.py (U6 LZW / container / palette decoders).
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(__file__))
from extract_u6_images import GAME, load_palette, lzw_decompress, indexed_to_image, extract_portrait

ROOT = os.path.join(os.path.dirname(__file__), "..")
SHOT = os.path.join(ROOT, "docs", "screenshots")
NPCDIR = os.path.join(SHOT, "npc")

SERIF = "/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc"
SANS = "/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc"


def font(path, size, idx=0):
    return ImageFont.truetype(path, size, index=idx)


# ----- city table: (key, EN, 中文城, 美德中, 美德EN, 真言, actor#, overview x,y)
CITIES = [
    ("moonglow",   "Moonglow",     "月光城",     "誠實", "Honesty",      "ahm",  33, 110, 55),
    ("britain",    "Britain",      "不列顛城",   "慈悲", "Compassion",   "mu",    5,  38, 43),
    ("jhelom",     "Jhelom",       "哲倫",       "勇敢", "Valor",        "ra",   43,  17, 112),
    ("yew",        "Yew",          "紫衫城",     "正義", "Justice",      "beh",  90,  26, 58),
    ("minoc",      "Minoc",        "米諾克",     "犧牲", "Sacrifice",    "cah",  67,  79, 10),
    ("trinsic",    "Trinsic",      "特林希克",   "榮譽", "Honor",        "summ",186,  66, 119),
    ("skarabrae",  "Skara Brae",   "史卡拉布雷", "靈性", "Spirituality", "om",   88,   6, 58),
    ("newmagincia","New Magincia", "新馬精西亞", "謙卑", "Humility",     "lum",  97,  95, 88),
]

# per-city label placement: side = where the label card sits.
#   "L" = left margin, "R" = right margin, "M" = floating on the map.
#   ly = card top y (absolute canvas px); for "M", (lx,ly) both absolute.
LABEL = {
    "yew":         dict(side="L", ly=292),
    "skarabrae":   dict(side="L", ly=452),
    "jhelom":      dict(side="L", ly=726),
    "minoc":       dict(side="R", ly=150),
    "moonglow":    dict(side="R", ly=404),
    "newmagincia": dict(side="R", ly=600),
    "britain":     dict(side="M", lx=474, ly=300),
    "trinsic":     dict(side="M", lx=452, ly=742),
}


def build_map():
    pal = load_palette(os.path.join(GAME, "U6PAL"))
    raw = open(os.path.join(GAME, "WORLDMAP.BMP"), "rb").read()
    decomp = lzw_decompress(raw)
    base = indexed_to_image(decomp, 128, 128, pal)

    SCALE = 6
    mw = mh = 128 * SCALE          # 768
    mp = base.resize((mw, mh), Image.NEAREST)

    # canvas with aged-parchment margins (wide sides for marginal labels)
    M_L, M_T, M_R, M_B = 232, 96, 232, 64
    cw, ch = mw + M_L + M_R, mh + M_T + M_B
    canvas = Image.new("RGB", (cw, ch), (22, 20, 16))
    d = ImageDraw.Draw(canvas)
    d.rectangle([6, 6, cw - 7, ch - 7], outline=(120, 96, 56), width=3)
    canvas.paste(mp, (M_L, M_T))
    d.rectangle([M_L - 1, M_T - 1, M_L + mw, M_T + mh], outline=(70, 55, 32), width=2)

    f_title = font(SERIF, 36)
    f_city = font(SERIF, 21)
    f_en = font(SERIF, 13)
    f_leg = font(SERIF, 14)

    title = "不列顛尼亞 — 八德八城"
    sub = "Britannia: Eight Virtues, Eight Cities"
    tw = d.textlength(title, font=f_title)
    d.text(((cw - tw) / 2, 18), title, font=f_title, fill=(226, 200, 140))
    sw = d.textlength(sub, font=f_en)
    d.text(((cw - sw) / 2, 64), sub, font=f_en, fill=(150, 132, 96))

    CARD_W, CARD_H = 196, 50

    def draw_card(lx, ly, line1, line2):
        card = Image.new("RGBA", (CARD_W, CARD_H), (18, 14, 10, 230))
        cd = ImageDraw.Draw(card)
        cd.rectangle([0, 0, CARD_W - 1, CARD_H - 1], outline=(184, 150, 90, 255), width=2)
        cd.text((10, 4), line1, font=f_city, fill=(238, 214, 150))
        cd.text((10, 30), line2, font=f_en, fill=(178, 160, 122))
        canvas.paste(card, (int(lx), int(ly)), card)

    for key, en, cn, vir, viren, mantra, actor, ovx, ovy in CITIES:
        px, py = M_L + ovx * SCALE, M_T + ovy * SCALE
        cfg = LABEL[key]
        side = cfg["side"]
        if side == "L":
            lx = 16
            conn = (lx + CARD_W, cfg["ly"] + CARD_H // 2)
        elif side == "R":
            lx = cw - CARD_W - 16
            conn = (lx, cfg["ly"] + CARD_H // 2)
        else:
            lx = cfg["lx"]
            conn = (lx + (px > lx + CARD_W / 2 and CARD_W or 0), cfg["ly"] + CARD_H // 2)
        ly = cfg["ly"]
        # leader line first (under pin/card)
        d.line([px, py, conn[0], conn[1]], fill=(206, 176, 108), width=2)
        # pin (gold ring + red core)
        r = 9
        d.ellipse([px - r, py - r, px + r, py + r], fill=(250, 226, 120), outline=(120, 70, 20), width=2)
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(150, 40, 30))
        draw_card(lx, ly, f"{cn} · {vir}", f"{en} · {mantra}")

    legend = "◉ 美德聖城 · pin 座標取自遊戲 SAVEGAME · 底圖 WORLDMAP.BMP（128² overview）經 U6Lzw 解壓 + U6PAL 還原"
    lw = d.textlength(legend, font=f_leg)
    d.text(((cw - lw) / 2, ch - 38), legend, font=f_leg, fill=(150, 132, 96))

    out = os.path.join(SHOT, "britannia_map.png")
    canvas.save(out)
    print("wrote", out, canvas.size)


# ----- portraits -------------------------------------------------------------
PORTRAITS = [
    # (filename, actor#)   party + LB court + city reps + special
    ("iolo", 4), ("dupre", 2), ("shamino", 3),
    ("lord_british", 5), ("geoffrey", 7), ("nystul", 6),
    ("mariah", 33), ("zellivan", 43), ("michael", 90), ("julia", 67),
    ("sentri", 186), ("horance", 88), ("katrina", 97),
    ("chuckles", 10), ("sherry", 9), ("smith", 132),
]


def build_portraits():
    os.makedirs(NPCDIR, exist_ok=True)
    pal = load_palette(os.path.join(GAME, "U6PAL"))
    SCALE = 2
    for name, actor in PORTRAITS:
        img = extract_portrait(actor - 1, pal)
        if img is None:
            print("!! no portrait", name, actor)
            continue
        img = img.resize((56 * SCALE, 64 * SCALE), Image.NEAREST)
        # gold frame
        fr = Image.new("RGB", (img.width + 6, img.height + 6), (150, 116, 56))
        fr.paste(img, (3, 3))
        d = ImageDraw.Draw(fr)
        d.rectangle([0, 0, fr.width - 1, fr.height - 1], outline=(90, 66, 28), width=1)
        out = os.path.join(NPCDIR, f"{name}.png")
        fr.save(out)
    print("wrote", len(PORTRAITS), "portraits to", NPCDIR)


if __name__ == "__main__":
    build_portraits()
    build_map()
