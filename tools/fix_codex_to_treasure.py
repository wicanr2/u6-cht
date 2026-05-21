#!/usr/bin/env python3
"""
採納聖者之書 1992 版的 Codex 譯名「知識寶典」取代我們 v1.0 的「守則之書」。

依據：dumps/sage_book_cross_ref.md
"""
import json, glob, os

TRANS_DIR = '/home/anr2/u6-cht/dumps/translations'

RULES = [
    ('終極智慧守則之書', '終極智慧之寶典'),
    ('守則之書',         '知識寶典'),
]

changes = {}
for path in sorted(glob.glob(os.path.join(TRANS_DIR, '*.json'))):
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

# Also fix glossary
glossary_path = '/home/anr2/u6-cht/dumps/glossary.json'
if os.path.exists(glossary_path):
    with open(glossary_path, 'r', encoding='utf-8') as f:
        gtext = f.read()
    for src, dst in RULES:
        gtext = gtext.replace(src, dst)
    with open(glossary_path, 'w', encoding='utf-8') as f:
        f.write(gtext)

print(f'Updated {len(changes)} files:')
for fn, cs in sorted(changes.items())[:20]:
    print(f'  {fn}: {", ".join(cs)}')
if len(changes) > 20:
    print(f'  ... and {len(changes)-20} more')
