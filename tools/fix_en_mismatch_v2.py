#!/usr/bin/env python3
"""
v2 修法：translator agent 對某些 NPC 寫了不存在 source 的 en（hallucinated 文字）。
策略：
1. 對每個 NPC 的譯文，檢查 en 是否在 source 中
2. 若不在：丟棄該條（因為 lookup 永遠對不上）
3. 從 source 拉出未翻譯的條目，標記為「待補譯」於另一檔
"""
import json, glob, os, sys

TRANS_DIR = '/home/anr2/u6-cht/dumps/translations'
SRC_DIR   = '/home/anr2/u6-cht/dumps/npc_extracted'

def process(npc_id):
    src_p = os.path.join(SRC_DIR, npc_id + '.json')
    tr_p  = os.path.join(TRANS_DIR, npc_id + '.json')
    if not (os.path.exists(src_p) and os.path.exists(tr_p)):
        return None
    src = json.load(open(src_p))
    tr  = json.load(open(tr_p))
    src_set = {s['text'] for s in src['strings']}

    keep, drop = [], []
    for t in tr['translations']:
        en = t.get('en', '')
        if en in src_set:
            keep.append(t)
        else:
            drop.append(t)

    if drop:
        # write back the cleaned translation file
        tr['translations'] = keep
        with open(tr_p, 'w', encoding='utf-8') as f:
            json.dump(tr, f, ensure_ascii=False, indent=1)
            f.write('\n')

    return {
        'npc': npc_id,
        'original': len(tr.get('translations', keep)) + len(drop),
        'kept': len(keep),
        'dropped': len(drop),
        'src_total': len(src['strings']),
    }

# Run on all NPC translation files (skip _engine_, BOOK_DAT, batch)
results = []
for tpath in sorted(glob.glob(os.path.join(TRANS_DIR, '*.json'))):
    fn = os.path.basename(tpath).replace('.json', '')
    if fn.startswith('_') or fn == 'BOOK_DAT' or '_batch' in fn:
        continue
    r = process(fn)
    if r and r['dropped'] > 0:
        results.append(r)

print(f'NPCs with dropped entries: {len(results)}')
for r in results:
    print(f'  {r["npc"]:20s}: dropped {r["dropped"]:2d}, kept {r["kept"]:2d}/{r["original"]} (src has {r["src_total"]})')

if not results:
    print('No mismatches.')
