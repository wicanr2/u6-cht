#!/usr/bin/env python3
"""Merge Lord British 3 batches into a single 005_Lord British.json"""
import json
out = {"_meta": {"npc": "Lord British", "batches": 3}, "translations": []}
for batch in ['005_Lord British_batch1of3.json', '005_Lord British_batch2of3.json', '005_Lord British_batch3of3.json']:
    d = json.load(open(f'/home/anr2/u6-cht/dumps/translations/{batch}', encoding='utf-8'))
    out["translations"].extend(d["translations"])

# Merge keyword_mapping + glossary_additions + riddles_additions from batch 1 if exists
b1 = json.load(open('/home/anr2/u6-cht/dumps/translations/005_Lord British_batch1of3.json', encoding='utf-8'))
out["keyword_mapping"] = b1.get("keyword_mapping", {})
out["glossary_additions"] = b1.get("glossary_additions", {})
out["riddles_additions"] = b1.get("riddles_additions", [])
out["translator_notes"] = "LB 3 batches merged. " + b1.get("translator_notes", "")

open('/home/anr2/u6-cht/dumps/translations/005_Lord British.json', 'w', encoding='utf-8').write(
    json.dumps(out, ensure_ascii=False, indent=2))
print(f'Merged: {len(out["translations"])} translations')
