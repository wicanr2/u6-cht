#!/usr/bin/env python3
"""
名詞漂移修正：依 reviewer 建議統一標準譯名。
依據：
  - Novel editor (2026-05-21)：Codex 主流為「守則之書」
  - Sin'Vraal 主流為「辛弗拉」
"""
import glob, os, json

TRANS_DIR = '/home/anr2/u6-cht/dumps/translations'

# 順序很重要：先換最長
RULES = [
    # Codex 統一為「守則之書」
    ('終極智慧之典', '終極智慧守則之書'),
    ('智典',         '守則之書'),
    ('法典',         '守則之書'),
    # Sin'Vraal 統一為「辛弗拉」
    ('辛夫拉爾', '辛弗拉'),
]

files = sorted(glob.glob(os.path.join(TRANS_DIR, '*.json')))
changes = {}
for path in files:
    try:
        with open(path, 'r', encoding='utf-8') as f:
            text = f.read()
    except: continue
    orig = text
    file_changes = []
    for src, dst in RULES:
        c = text.count(src)
        if c:
            text = text.replace(src, dst)
            file_changes.append(f'{src}→{dst}×{c}')
    if text != orig:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(text)
        changes[os.path.basename(path)] = file_changes

print(f'Updated {len(changes)} files:')
for fn, cs in sorted(changes.items()):
    print(f'  {fn}: {", ".join(cs)}')
