#!/usr/bin/env python3
"""
Build engine-side lookup table from translation JSONs.

Output: working/game/cht_strings.tab
Format (UTF-8 text, one entry per line, '\t' delimiter, '\\n' escape for newline):
    <en>\t<zh>\n

Engine loads this file at init, builds an unordered_map<string,string>.
At Converse `set_output(text)` and Book render path, replace `text` if matched.
"""
import json, os, glob, sys

TRANS_DIR = '/home/anr2/u6-cht/translations'   # source of truth (git tracked)
OUT_PATH  = '/home/anr2/u6-cht/working/game/cht_strings.tab'
# 舊路徑 'dumps/translations' 已淘汰（v1.5.2 issue #1 兇手：commit 9e54e93 加 fragment
# 加在 translations/、build 卻讀 dumps/translations/，opened!/closed! 始終沒進 tab）。

def to_big5(s: str) -> bytes:
    """Encode zh value to Big5 (cp950) bytes. Replace unencodable chars with '?'.

    The engine's U6Font Big5 path expects byte stream where Big5 leads (0xA1-0xFE)
    are followed by valid trails (0x40-0x7E | 0xA1-0xFE). UTF-8 would render as
    garbage. ASCII chars in zh stay 1-byte ASCII (still hits is_print path).
    """
    out = bytearray()
    for ch in s:
        try:
            out += ch.encode('cp950')
        except UnicodeEncodeError:
            out += b'?'
    return bytes(out)

entries: dict[str, str] = {}
conflicts: dict[str, list[str]] = {}

# Prefer non-batch files over batch files for the same NPC; iterate batches first,
# then merged files so merged overwrites batch entries.
files = sorted(glob.glob(os.path.join(TRANS_DIR, '*.json')))
# Sort: batch files first, then non-batch
files.sort(key=lambda p: (0 if '_batch' in os.path.basename(p) else 1, p))

for path in files:
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    for tr in data.get('translations', []):
        en = tr.get('en')
        zh = tr.get('zh')
        if not en or not zh:
            continue
        if en in entries and entries[en] != zh:
            conflicts.setdefault(en, [entries[en]]).append(zh)
        entries[en] = zh   # last-write-wins; non-batch (after batches) wins

# Emit binary format v3 — exact records keyed by FNV-1a 64-bit hash of en
# (instead of raw en bytes), so cht_strings.tab can be distributed publicly
# without exposing the original game's English source text. Fragments keep
# plain en (~40 short engine-UI labels) since substring match needs the text.
#
#   8 bytes  magic "U6CHT\x00\x03\x00"
#   uint32 LE  exact_count
#   each exact record:
#     8 bytes  fnv1a64(en) LE        (replaces uint16 en_len + en bytes)
#     uint16 LE zh_len + zh_big5
#   uint32 LE  fragment_count
#   each fragment record:
#     uint16 LE en_len + en          (plain — needed for substring match)
#     uint16 LE zh_len + zh_big5
import struct

MAGIC_V3 = b'U6CHT\x00\x03\x00'

# FNV-1a 64-bit. Same algorithm in C++ side (cht_translate.cpp).
FNV_OFFSET = 0xcbf29ce484222325
FNV_PRIME  = 0x100000001b3
MASK64     = (1 << 64) - 1

def fnv1a64(b: bytes) -> int:
    h = FNV_OFFSET
    for byte in b:
        h ^= byte
        h = (h * FNV_PRIME) & MASK64
    return h

os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
unencodable_total = 0
hashed_records = []
hash_collisions = 0
seen_hash = {}
for en, zh in entries.items():
    en_bytes = en.encode('utf-8')
    zh_big5  = to_big5(zh)
    if len(zh_big5) > 65535:
        print(f'WARN: too long zh, skipped: {en[:40]!r}')
        continue
    unencodable_total += zh_big5.count(b'?')
    h = fnv1a64(en_bytes)
    if h in seen_hash and seen_hash[h] != en:
        hash_collisions += 1
    seen_hash[h] = en
    hashed_records.append((h, zh_big5))

# Fragments keep plain en (short UI labels, sub-string match at runtime).
fragments = []
frag_path = os.path.join(TRANS_DIR, '_engine_fragments.json')
if os.path.exists(frag_path):
    with open(frag_path, 'r', encoding='utf-8') as f:
        fdata = json.load(f)
    for tr in fdata.get('fragments', []):
        en = tr.get('en')
        zh = tr.get('zh')
        if not en or not zh: continue
        en_bytes = en.encode('utf-8')
        zh_big5  = to_big5(zh)
        if len(en_bytes) > 65535 or len(zh_big5) > 65535: continue
        unencodable_total += zh_big5.count(b'?')
        fragments.append((en_bytes, zh_big5))

with open(OUT_PATH, 'wb') as f:
    f.write(MAGIC_V3)
    f.write(struct.pack('<I', len(hashed_records)))
    for h, zh_b in hashed_records:
        f.write(struct.pack('<Q', h))     # uint64 LE fnv hash
        f.write(struct.pack('<H', len(zh_b)))
        f.write(zh_b)
    f.write(struct.pack('<I', len(fragments)))
    for en_b, zh_b in fragments:
        f.write(struct.pack('<H', len(en_b)))
        f.write(en_b)
        f.write(struct.pack('<H', len(zh_b)))
        f.write(zh_b)
    print(f'... {len(fragments)} fragments appended (plain en)')
    if hash_collisions:
        print(f'WARN: {hash_collisions} hash collisions — strings differ but hash to same uint64')

print(f'wrote {OUT_PATH}: {len(entries)} entries, zh stored as Big5/cp950')
if unencodable_total:
    print(f'WARNING: {unencodable_total} chars could not encode to Big5 (replaced with "?")')
if conflicts:
    print(f'NOTE: {len(conflicts)} keys had translation conflicts (kept the last one)')
    for en, vals in list(conflicts.items())[:5]:
        print(f'  conflict: {en!r:80.80} -> {vals}')
