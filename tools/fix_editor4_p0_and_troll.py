#!/usr/bin/env python3
"""
Apply editor4 P0 fixes + 聖者之書 canonical name rule:
- Troll 山怪 → 巨人 (sage book p43)
- Minoc 密諾克 → 米諾克 (sage book p23)
- E4-P0-1: 057 Utomo @kill bracket fix
- E4-P0-2: 089 Marney @killed bracket + close-quote fix
"""
import json, glob, os

T = '/home/anr2/u6-cht/dumps/translations'

SPECIFIC = [
    {
        'file': '057_Utomo.json',
        'pattern': '去@kill（殺好）人',
        'replace': '去@kill（殺害）好人',
    },
    {
        'file': '089_Marney.json',
        'pattern': '「尤爾在父親@killed被殺後，將它還給了我。',
        'replace': '「尤爾在父親@killed（被殺）後，將它還給了我。」',
    },
]

# Sage book canonical name rule (user 2026-05-22: 翻譯衝突以聖者之書為主)
GLOBAL_RULES = [
    ('山怪', '巨人'),         # Troll (聖者之書 p52 + 遊戲手冊 p43)
    ('密諾克', '米諾克'),    # Minoc (聖者之書 p23)
    ('崔西克', '特林希克'),  # Trinsic (聖者之書 p21-23) — reverse our earlier unification
]

stats = {'specific_files': 0, 'global_files': 0, 'global_replacements': 0}

# Apply specifics
for r in SPECIFIC:
    path = os.path.join(T, r['file'])
    try:
        text = open(path,'r',encoding='utf-8').read()
        if r['pattern'] in text:
            new_text = text.replace(r['pattern'], r['replace'])
            open(path,'w',encoding='utf-8').write(new_text)
            stats['specific_files'] += 1
            print(f"  ✓ {r['file']}: {r['pattern'][:30]}... → {r['replace'][:30]}...")
    except FileNotFoundError:
        print(f"  ✗ {r['file']} not found")

# Apply global rules
for path in sorted(glob.glob(os.path.join(T, '*.json'))):
    fn = os.path.basename(path)
    if '_engine' in fn: continue
    text = open(path,'r',encoding='utf-8').read()
    orig = text
    changes = []
    for src, dst in GLOBAL_RULES:
        if src in text:
            c = text.count(src)
            text = text.replace(src, dst)
            changes.append(f'{src}→{dst}×{c}')
            stats['global_replacements'] += c
    if text != orig:
        open(path,'w',encoding='utf-8').write(text)
        stats['global_files'] += 1
        if len(changes):
            print(f"  ✓ {fn}: {', '.join(changes)}")

# Also update glossary
g_path = '/home/anr2/u6-cht/dumps/glossary.json'
if os.path.exists(g_path):
    text = open(g_path,'r',encoding='utf-8').read()
    orig = text
    for src, dst in GLOBAL_RULES:
        text = text.replace(src, dst)
    if text != orig:
        open(g_path,'w',encoding='utf-8').write(text)
        print('  ✓ glossary.json updated')

print(f'\nstats: {stats}')
