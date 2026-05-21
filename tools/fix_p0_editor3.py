#!/usr/bin/env python3
"""Apply editor3 P0/P1 fixes to translation JSONs."""
import json, glob, os

T = '/home/anr2/u6-cht/dumps/translations'

# Specific full-string replacements
REPLACEMENTS = [
    # E3-P0-1: 066 Gwenno offset 260 keyword brackets shifted
    {
        'file': '066_Gwenno.json',
        'pattern': '@songs（公會）',
        'replace': '@songs（歌謠）',
    },
    {
        'file': '066_Gwenno.json',
        'pattern': '@notation（歌謠）',
        'replace': '@notation（記譜法）',
    },
    {
        'file': '066_Gwenno.json',
        'pattern': '@guild（公會）法',
        'replace': '@guild（公會）',
    },
    # E3-P0-2
    {
        'file': '066_Gwenno.json',
        'pattern': '@number（音符）',
        'replace': '@number（數字）',
    },
    # E3-P1-3: Captain John 操控 → 克制
    {
        'file': '183_Captain John.json',
        'pattern': '操控',
        'replace': '克制',
    },
    # E3-P1-4: 180 Mandrake 美德列表 英勇/榮耀 → 勇敢/榮譽
    {
        'file': '180_Mandrake.json',
        'pattern': '誠實、慈悲、英勇、正義、犧牲、榮耀',
        'replace': '誠實、慈悲、勇敢、正義、犧牲、榮譽',
    },
    # E3-P1-6: 100 Thindle 名字分割
    {
        'file': '100_Thindle.json',
        'pattern': '@Thindle（辛德）爾紡線匠',
        'replace': '@Thindle（辛德爾）紡線匠',
    },
    # E3-P1-7: 110 Dr Cat 不列顛城
    {
        'file': '110_Dr_ Cat.json',
        'pattern': '@Britain（不列）顛城',
        'replace': '@Britain（不列顛城）',
    },
    # E3-P1-8: 153 Shubin 小麵包
    {
        'file': '153_Shubin.json',
        'pattern': '@roll（小麵）包',
        'replace': '@roll（小麵包）',
    },
]

# Global Valor 勇氣 → 勇敢 (only when it's the virtue name)
VALOR_FILES_GLOBAL = ['044_Nomaan.json', '049_Culham.json', '127_Ahrmaand.json', '160_Simon.json']
VALOR_REPLACES = [
    ('勇氣符文', '勇敢符文'),
    ('勇氣真言', '勇敢真言'),
    ('勇氣神壇', '勇敢神壇'),
    ('勇氣聖壇', '勇敢聖壇'),
    ('勇氣祭壇', '勇敢祭壇'),
    ('勇氣之德', '勇敢之德'),
    ('美德勇氣', '美德勇敢'),
]

# Global Honor 榮耀 → 榮譽 (197 + related)
HONOR_FILES = ['197_Honor.json']
HONOR_REPLACES = [
    ('榮耀祭壇', '榮譽祭壇'),
    ('榮耀神壇', '榮譽神壇'),
    ('榮耀聖壇', '榮譽聖壇'),
    ('榮耀之德', '榮譽之德'),
    ('美德榮耀', '美德榮譽'),
    ('榮耀真言', '榮譽真言'),
    ('榮耀符文', '榮譽符文'),
]

changed = {}
for path in sorted(glob.glob(os.path.join(T, '*.json'))):
    fn = os.path.basename(path)
    text = open(path,'r',encoding='utf-8').read()
    orig = text
    file_changes = []
    for r in REPLACEMENTS:
        if fn == r['file'] and r['pattern'] in text:
            c = text.count(r['pattern'])
            text = text.replace(r['pattern'], r['replace'])
            file_changes.append(f"{r['pattern'][:25]}→{r['replace'][:25]}×{c}")
    if fn in VALOR_FILES_GLOBAL:
        for src, dst in VALOR_REPLACES:
            if src in text:
                c = text.count(src)
                text = text.replace(src, dst)
                file_changes.append(f'{src}→{dst}×{c}')
    if fn in HONOR_FILES:
        for src, dst in HONOR_REPLACES:
            if src in text:
                c = text.count(src)
                text = text.replace(src, dst)
                file_changes.append(f'{src}→{dst}×{c}')
    if text != orig:
        open(path,'w',encoding='utf-8').write(text)
        changed[fn] = file_changes

print(f'Updated {len(changed)} files:')
for fn, cs in sorted(changed.items()):
    print(f'  {fn}: {", ".join(cs)}')
