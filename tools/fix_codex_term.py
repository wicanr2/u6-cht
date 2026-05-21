#!/usr/bin/env python3
"""
Codex 譯名統一：把所有「守則之書」、「法典」改為「智典」。
跳過 _engine_strings.json 與 BOOK_DAT.json（除非也含此詞）。
"""
import json, glob, os

TRANS_DIR = '/home/anr2/u6-cht/dumps/translations'

# 取代表（順序很重要：先換最長）
RULES = [
    ('終極智慧守則之書', '終極智慧之典'),
    ('終極智慧之守則之書', '終極智慧之典'),
    ('守則之書', '智典'),
    ('終極智慧守則之冊', '終極智慧之典'),
    # 法典只 1 處（141 Sin'Vraal）
    ('法典', '智典'),
]

files = sorted(glob.glob(os.path.join(TRANS_DIR, '*.json')))
changes = {}
for path in files:
    try:
        with open(path, 'r', encoding='utf-8') as f:
            text = f.read()
    except: continue
    orig = text
    cnt = 0
    for src, dst in RULES:
        c = text.count(src)
        if c:
            text = text.replace(src, dst)
            cnt += c
    if text != orig:
        # write only if changed
        with open(path, 'w', encoding='utf-8') as f:
            f.write(text)
        changes[os.path.basename(path)] = cnt

print(f'Updated {len(changes)} files, {sum(changes.values())} replacements:')
for fn, cnt in sorted(changes.items()):
    print(f'  {fn}: {cnt}')
