#!/usr/bin/env python3
"""
修 P0 mismatch：翻譯 JSON 的 en 與 npc_extracted 的 text 不完全相符 →
lookup 永遠對不上。逐筆比對，若 zh 已就位且 en 只差在空格/標點，
就用 source text 取代 en（zh 不動）。

報告漏網（無法用 offset/len 安全匹配的）給人工。
"""
import json, glob, os, sys

TRANS_DIR = '/home/anr2/u6-cht/dumps/translations'
SRC_DIR   = '/home/anr2/u6-cht/dumps/npc_extracted'

def load_src(npc_id_filename):
    # input like '095_Charlotte' or '049_Culham'
    p = os.path.join(SRC_DIR, npc_id_filename + '.json')
    if not os.path.exists(p): return None
    return json.load(open(p, 'r', encoding='utf-8'))

repaired_total = 0
report = []
for tpath in sorted(glob.glob(os.path.join(TRANS_DIR, '*.json'))):
    fn = os.path.basename(tpath).replace('.json', '')
    if fn.startswith('_') or fn == 'BOOK_DAT':
        continue
    # Skip batch files; merged file is canonical
    if '_batch' in fn: continue

    src = load_src(fn)
    if src is None: continue
    src_by_offset = {s['offset']: s for s in src['strings']}
    src_texts = {s['text'] for s in src['strings']}

    tdata = json.load(open(tpath, 'r', encoding='utf-8'))
    trans = tdata.get('translations', [])
    changed = False
    for tr in trans:
        en = tr.get('en')
        if not en or en in src_texts:
            continue
        # Try matching by offset
        ofs = tr.get('offset')
        if ofs is not None and ofs in src_by_offset:
            src_text = src_by_offset[ofs]['text']
            # only auto-repair if differ by whitespace/quote-ish only
            stripped_en = en.strip()
            stripped_src = src_text.strip()
            if (stripped_en == stripped_src or
                en.replace(' ', '') == src_text.replace(' ', '')):
                tr['en'] = src_text
                changed = True
                repaired_total += 1
                continue
        report.append((fn, ofs, en[:60], 'no auto-repair'))

    if changed:
        with open(tpath, 'w', encoding='utf-8') as f:
            json.dump(tdata, f, ensure_ascii=False, indent=1)
            f.write('\n')

print(f'Auto-repaired {repaired_total} entries.')
if report:
    print(f'\nUnresolved ({len(report)}):')
    for r in report[:30]:
        print(f'  {r}')
