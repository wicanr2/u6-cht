#!/usr/bin/env python3
"""
LB Compendium quiz patch:
保留英文題目（原版 copy protection 風味），但在每題後加 (答案：...) 提示。
首次 quiz 觸發前加中文 disclaimer 告知玩家：這是密碼保護不是翻譯漏掉。
"""
import json

PATH = '/home/anr2/u6-cht/dumps/translations/005_Lord British.json'
d = json.load(open(PATH, 'r', encoding='utf-8'))

# 題目 → 答案 keyword hint（4-letter prefix match）
QUIZ = {
    '"What part of the tangle vine doth put one to sleep?"': 'cent / pod / frag',
    '"What doth trolls lack?"':                              'end',
    '"How doth giant squids crush their prey?"':             'beak',
    '"Where hath images of the silver serpent been seen?"':  'tomb / wall / anci / monu',
    '"What art reapers remnants of?"':                       'anci / ench / fore',
    '"What creature art wisps oft mistaken for?"':           'fire / fly',
    '"How wert the headlesses produced?"':                   'wiza / expe',
    '"What valued item canst one find near the spawning grounds of Hydras?"': 'nigh / mush',
    '"How canst one fend off rotworms?"':                    'torc / fire / flam / burn / pass',
    '"How doth sea serpents attack?"':                       'fire / ball / swip / tail',
}

# Disclaimer 加到此句尾（首次 quiz 觸發前提示）
DISCLAIMER_TARGET = '"Only the true Avatar would know what was contained in the Compendium I sent."*'
DISCLAIMER_ADD    = '"唯有真聖者方知朕所贈典籍之內容。\n【以下為原版密碼保護題目（U6 Copy Protection），保留英文以存古風；答案於括號內以拉丁字母提供。】"*'

# 錯答時的 disclaimer
WRONG_TARGET = '"Nay, \'tis not the correct answer. Consult thy Compendium."'
WRONG_NEW    = '「非也，此答有誤。請參閱括號內提示再答。」'

changes = 0
for tr in d['translations']:
    en = tr.get('en', '')
    if en in QUIZ:
        old_zh = tr.get('zh', '')
        # Keep English question, append answer hint
        tr['zh'] = f'{en} (答案: {QUIZ[en]})'
        print(f'Q: {en[:50]}...')
        print(f'    OLD: {old_zh[:50]}')
        print(f'    NEW: {tr["zh"][:80]}')
        changes += 1
    elif en == DISCLAIMER_TARGET:
        tr['zh'] = DISCLAIMER_ADD
        print(f'PRE-QUIZ disclaimer set')
        changes += 1
    elif en == WRONG_TARGET:
        tr['zh'] = WRONG_NEW
        print(f'WRONG-answer message updated')
        changes += 1

# Write back
with open(PATH, 'w', encoding='utf-8') as f:
    json.dump(d, f, ensure_ascii=False, indent=1)
    f.write('\n')

print(f'\n{changes} entries patched in 005 Lord British.')
