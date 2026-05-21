#!/usr/bin/env python3
"""
Mass fix for `@EN（ZH）ZH'` duplicate pattern found by editor2 agent.

Engine behavior (confirmed via ConverseGump::parse_token reading):
  `@EN` → @ stripped, EN displayed + collected as clickable keyword
  `@EN（ZH）X` displays as `EN（ZH）X` — if X contains ZH, visual repeat!

Fix: if same Chinese chars appear immediately after the close paren,
strip them off (they were translator's redundant gloss).
"""
import json, re, glob, os, sys

APPLY = '--apply' in sys.argv

# Pattern: @EN（ZH）+ X — if X starts with chars from ZH (or X == ZH), strip X
# Conservative: only strip if X is single CJK char that ZH ends with, or X == ZH suffix
pat = re.compile(r'@([A-Za-z][A-Za-z0-9\']*)（([一-鿿]+)）([一-鿿]+)')

stats = {'files': 0, 'fixed': 0}
samples = []

for path in sorted(glob.glob('/home/anr2/u6-cht/dumps/translations/*.json')):
    fn = os.path.basename(path)
    if '_engine' in fn or fn == 'BOOK_DAT.json':
        continue
    try:
        text = open(path, 'r', encoding='utf-8').read()
    except: continue
    orig = text

    def repl(m):
        en, zh, after = m.group(1), m.group(2), m.group(3)
        # Check if `after` starts with chars duplicating end of `zh`
        # Strategy: if first 1-2 chars of `after` match suffix of `zh` → strip them
        for n in (3, 2, 1):
            if after[:n] == zh[-n:]:
                # strip the duplicate prefix
                stats['fixed'] += 1
                new_after = after[n:]
                if len(samples) < 20:
                    samples.append((fn, m.group(0), f'@{en}（{zh}）{new_after}'))
                return f'@{en}（{zh}）{new_after}'
        return m.group(0)

    new_text = pat.sub(repl, text)
    if new_text != orig:
        stats['files'] += 1
        if APPLY:
            open(path, 'w', encoding='utf-8').write(new_text)

print(f'\nstats: {stats}')
print(f'\nfirst 20 fixes:')
for fn, old, new in samples:
    print(f'  {fn}:')
    print(f'    OLD: {old}')
    print(f'    NEW: {new}')
print(f"\n{'DRY-RUN — re-run with --apply' if not APPLY else 'CHANGES WRITTEN'}")
