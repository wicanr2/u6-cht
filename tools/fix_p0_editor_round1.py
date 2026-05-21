#!/usr/bin/env python3
"""
應用第一輪 editor-in-chief 報告的 P0 修正。
依據：dumps/editor_in_chief_report.md
"""
import json, glob, os

TRANS_DIR = '/home/anr2/u6-cht/dumps/translations'

# Specific text replacements per file
P0_FIXES = [
    # P0-1, P0-3: 「不列顛王顛王」重字（@British 後跟 「顛王」）
    {
        'pattern': '@British（不列顛王）顛王',
        'replace': '@British（不列顛王）',
    },
    # P0-2: 「貓人之貓人」重字
    {
        'pattern': '@Werecat（酒窖之貓人）之貓人』',
        'replace': '@Werecat（酒窖之貓人）』',
    },
    # P0-4: Chuckles quest hint — 兩個 keyword 括號互換
    {
        'pattern': '翻翻@chest（寶箱）托房裡那只@Nystul（寶箱）',
        'replace': '去翻@Nystul（尼斯托）房裡的@chest（寶箱）',
    },
    # P0-6: Reaper quiz answer
    {
        'pattern': '死神乃何物之遺存？',
        'replace': '樹妖乃何物之遺存？',
    },
    # P1-1: Dupre「甲甲」重字
    {
        'pattern': '身披一襲閃亮的甲甲',
        'replace': '身披一襲閃亮甲冑',
    },
    # P1-8: 大烏賊統一（編輯第一輪建議）
    {
        'pattern': '巨烏賊以何物壓碎其獵物',
        'replace': '大烏賊以何物壓碎其獵物',
    },
    # P1-10 Mongbat
    {
        'pattern': '魔蝠',
        'replace': '蝙猴',
    },
    # 殘餘 bilingual 重字（額外 sweep）
    {
        'pattern': '@gargoyles（魔像族）族',  # 「@魔像族族」重字
        'replace': '@gargoyles（魔像族）',
    },
    {
        'pattern': '@gargoyle（魔像）族',     # 「@魔像族」 with extra 族
        'replace': '@gargoyle（魔像族）',
    },
    {
        'pattern': '@gargoyle（魔像）族戰事',
        'replace': '@gargoyle（魔像族）戰事',
    },
]

# Valor 英勇 → 勇敢 (P0-5) — only in 194_Valor.json
VALOR_FILES = ['194_Valor.json']

# Files to also process for Valor virtue mapping
all_files = sorted(glob.glob(os.path.join(TRANS_DIR, '*.json')))

stats = {}
for path in all_files:
    fn = os.path.basename(path)
    if '_engine' in fn:
        continue
    try:
        text = open(path, 'r', encoding='utf-8').read()
    except: continue
    orig = text

    # Apply general P0/P1 fixes
    for rule in P0_FIXES:
        if rule['pattern'] in text:
            count = text.count(rule['pattern'])
            text = text.replace(rule['pattern'], rule['replace'])
            stats.setdefault(fn, []).append(f'{rule["pattern"][:30]}…×{count}')

    # Valor specific (P0-5) — only in 194_Valor and Quiz/LB references
    if fn in VALOR_FILES or 'British' in fn:
        # 「英勇」 in virtue context → 「勇敢」
        # Be careful: 英勇 is a regular adjective too, so we need targeted replacement
        valor_targets = [
            ('英勇祭壇', '勇敢祭壇'),
            ('英勇之德', '勇敢之德'),
            ('英勇仍有許多', '勇敢仍有許多'),
            ('英勇之美德', '勇敢之美德'),
            ('美德——英勇', '美德——勇敢'),
            ('「英勇」', '「勇敢」'),
        ]
        for src, dst in valor_targets:
            if src in text:
                c = text.count(src)
                text = text.replace(src, dst)
                stats.setdefault(fn, []).append(f'{src}→{dst}×{c}')

    if text != orig:
        open(path, 'w', encoding='utf-8').write(text)

print(f'Updated {len(stats)} files:')
for fn, changes in sorted(stats.items()):
    print(f'  {fn}: {", ".join(changes)}')
