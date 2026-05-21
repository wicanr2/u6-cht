#!/usr/bin/env python3
"""
Extract per-NPC keyword list (4-letter prefix tokens that VM matches against
player input). Conv VM stores them as comma-separated lowercase strings in
KEYWORDS opcode (0xEF) bytecode — translators recorded them as `en` entries
matching the pattern `^[a-z]{3,5}(,[a-z]{3,5})*$`.

Output:
- translations/_keywords.json — mapping NPC name → set of keywords
- docs/npc_keywords.md — human-readable cheatsheet
"""
import json, glob, os, re

TRANS_DIR = '/home/anr2/u6-cht/dumps/translations'
OUT_JSON  = '/home/anr2/u6-cht/translations/_keywords.json'
OUT_MD    = '/home/anr2/u6-cht/docs/npc_keywords.md'

# A KEYWORDS opcode payload looks like: "name", "job,bye", "fath,moth,sist,brot",
# "rest,inn,room", etc. — 3-5 letter prefixes joined by comma. Some tokens may
# be 2-letter (like "yn" for yes/no askc) or up to 6 letters in edge cases.
KW_RE = re.compile(r'^[a-z][a-z\']{1,5}(,[a-z][a-z\']{1,5})*$')

# Always-available keywords (VM auto-handles regardless of NPC list)
COMMON_AUTO = ['name', 'job', 'bye']

# Load glossary for keyword → Chinese annotation
glossary_path = '/home/anr2/u6-cht/dumps/glossary.json'
kw_zh = {}
if os.path.exists(glossary_path):
    g = json.load(open(glossary_path, 'r', encoding='utf-8'))
    for tag, zh in g.get('keywords_common', {}).items():
        if tag.startswith('@'):
            kw_zh[tag[1:].lower()] = zh.lstrip('@').rstrip('，。、！？ ')

def annotate(kw):
    # 4-letter prefix from glossary canonical mapping (best effort)
    for full_en, zh in kw_zh.items():
        if full_en.startswith(kw):
            return f'{kw}/{zh}'
    return kw

result = {}

for path in sorted(glob.glob(os.path.join(TRANS_DIR, '*.json'))):
    fn = os.path.basename(path).replace('.json', '')
    if fn.startswith('_') or fn == 'BOOK_DAT' or '_batch' in fn:
        continue
    try:
        d = json.load(open(path, 'r', encoding='utf-8'))
    except: continue

    keywords = set()
    for tr in d.get('translations', []):
        en = tr.get('en', '')
        if KW_RE.match(en):
            for kw in en.split(','):
                keywords.add(kw.strip().lower())

    # extract NPC display name from filename (NN_Name)
    parts = fn.split('_', 1)
    if len(parts) == 2:
        npc_num, npc_name = parts
        try:
            npc_num = int(npc_num)
        except:
            continue
        result[npc_num] = {
            'name':     npc_name,
            'keywords': sorted(keywords),
        }

# Write JSON
os.makedirs(os.path.dirname(OUT_JSON), exist_ok=True)
with open(OUT_JSON, 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=1)
    f.write('\n')

# Write Markdown cheatsheet
os.makedirs(os.path.dirname(OUT_MD), exist_ok=True)
with open(OUT_MD, 'w', encoding='utf-8') as f:
    f.write('# NPC Keyword Cheatsheet\n\n')
    f.write('每 NPC 對 player 輸入做 4-letter prefix match。'
            '玩家可輸入以下任一 keyword 觸發對話分支。\n\n')
    f.write('「name / job / bye」三個是 VM 內建，所有 NPC 都接受。')
    f.write('表中只列出此 NPC 額外定義的 keyword（不含 name/job/bye）。\n\n')
    f.write(f'共 {len(result)} 個 NPC。\n\n')
    f.write('| # | NPC | Keywords (extra) |\n')
    f.write('|---|---|---|\n')
    for num in sorted(result.keys()):
        d = result[num]
        extra = [k for k in d['keywords'] if k not in COMMON_AUTO]
        annotated = [annotate(k) for k in extra]
        f.write(f'| {num:03d} | {d["name"]} | `{", ".join(annotated) if annotated else "—"}` |\n')

print(f'NPCs processed: {len(result)}')
print(f'Total unique keywords across all NPCs: {len({k for d in result.values() for k in d["keywords"]})}')
print(f'Wrote {OUT_JSON} and {OUT_MD}')
