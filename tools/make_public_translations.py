#!/usr/bin/env python3
"""
產生 public-safe 譯文檔：把 dumps/translations/ 的 en+zh JSON
轉成 translations_public/ 的 hash+zh JSON（無 en 原文）。

Hash key = FNV-1a 64-bit of en bytes (UTF-8/ASCII)，與 engine 一致。

repo 公開只 ship `translations_public/`；私下開發者保留 `dumps/translations/`
（gitignored）作為 source-of-truth 編輯。要 rebuild lookup binary：
1. 自備合法 U6 → `tools/extract_npc_strings.py CONVERSE.A` → npc_extracted/
2. 自寫 dumps/translations/<NPC>.json 或從 translations_public/ 配自己的 npc_extracted 反查
3. `build_lookup_table.py`
"""
import json, os, glob

SRC_DIR = '/home/anr2/u6-cht/dumps/translations'
OUT_DIR = '/home/anr2/u6-cht/translations_public'

FNV_OFFSET = 0xcbf29ce484222325
FNV_PRIME  = 0x100000001b3
MASK64     = (1 << 64) - 1

def fnv1a64(b: bytes) -> int:
    h = FNV_OFFSET
    for byte in b:
        h ^= byte
        h = (h * FNV_PRIME) & MASK64
    return h

os.makedirs(OUT_DIR, exist_ok=True)

stats = {'files': 0, 'entries': 0, 'fragments': 0}

for path in sorted(glob.glob(os.path.join(SRC_DIR, '*.json'))):
    fn = os.path.basename(path)

    # fragments stay plain (engine UI labels) — passthrough copy
    if fn == '_engine_fragments.json':
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        stats['fragments'] = len(data.get('fragments', []))
        with open(os.path.join(OUT_DIR, fn), 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=1)
            f.write('\n')
        continue

    # batch files: skip (merged file is canonical)
    if '_batch' in fn:
        continue

    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    public = {
        '_meta': data.get('_meta', {}),
        'translations': [],
        'glossary_additions': data.get('glossary_additions', {}),
        'translator_notes': data.get('translator_notes', ''),
    }
    for tr in data.get('translations', []):
        en = tr.get('en', '')
        zh = tr.get('zh', '')
        if not en or not zh:
            continue
        h = fnv1a64(en.encode('utf-8'))
        out = {
            'hash': f'{h:016x}',
            'zh':   zh,
        }
        # Keep `note` if it gives context (length, 5C avoidance, etc), but drop
        # `offset`/`len` since those are tied to original conv bytecode layout.
        if tr.get('note'):
            out['note'] = tr['note']
        public['translations'].append(out)
        stats['entries'] += 1

    with open(os.path.join(OUT_DIR, fn), 'w', encoding='utf-8') as f:
        json.dump(public, f, ensure_ascii=False, indent=1)
        f.write('\n')
    stats['files'] += 1

print(f'Stripped {stats["files"]} files: {stats["entries"]} hashed entries + {stats["fragments"]} plain fragments')
print(f'Output: {OUT_DIR}/')
