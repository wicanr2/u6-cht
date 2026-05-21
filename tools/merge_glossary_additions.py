#!/usr/bin/env python3
"""
Merge `glossary_additions` from translator output JSONs into the master
`glossary.json`. Also append `riddles_additions` entries to riddles.entries.
"""
import json, os, glob

MASTER = '/home/anr2/u6-cht/dumps/glossary.json'
TRANS_DIR = '/home/anr2/u6-cht/dumps/translations'

master = json.load(open(MASTER, encoding='utf-8'))

added_terms, added_riddles = 0, 0
for tx_path in sorted(glob.glob(os.path.join(TRANS_DIR, '*.json'))):
    tx = json.load(open(tx_path, encoding='utf-8'))
    npc = os.path.basename(tx_path).replace('.json', '')

    additions = tx.get('glossary_additions', {})
    for section, items in additions.items():
        if not isinstance(items, dict):
            continue
        if section not in master:
            master[section] = items
            added_terms += len(items)
            continue
        for k, v in items.items():
            if k.startswith('_'):
                continue
            if k not in master[section]:
                master[section][k] = v
                added_terms += 1

    for r in tx.get('riddles_additions', []):
        master.setdefault('riddles', {}).setdefault('entries', []).append(r)
        added_riddles += 1

open(MASTER, 'w', encoding='utf-8').write(
    json.dumps(master, ensure_ascii=False, indent=2))
print(f"Merged {added_terms} new terms, {added_riddles} new riddles into {MASTER}")
