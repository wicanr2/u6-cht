#!/usr/bin/env python3
"""
把譯文 `@中文` keyword 改成 `@english（中文）` 形式：
- player 看到 @english 是 clickable 英文，丟給 VM 仍 prefix-match 工作
- 括號內中文做提示，玩家知道這個 token 在中文裡的意思

v2：
- 先查 glossary.json[keywords_common] 拿 canonical zh
- 沒有就 fallback to 從 zh 文本掃 @ 後 1-4 個中文字（遇 particle/標點停）
- 多出來的 @ 從 zh 移除

dry-run by default. Pass --apply to write back.
"""
import json, re, glob, os, sys

en_re = re.compile(r'@([A-Za-z][A-Za-z0-9]*)')
zh_marker_re = re.compile(r'@([一-鿿]+)')

# Chinese particles / breakers — token ends at these
PARTICLES = set('的之是了在也都將已與而和或卻但雖若即且又故亦矣哉乎呢嗎吧啊啦呀唉哩呢喔耶就便方則乃為以由從至向往從而並且因而所以然而所且其此那這彼當然只僅有無中上下外內間時向被然卻後前便')

# Single Chinese char or punctuation that breaks tokens
BREAKERS = set('，。、！？「」『』（）：；…—－—《》〈〉【】〔〕') | PARTICLES

FALLBACK_CHAR_CAP = 2  # Most keyword nouns are 2-char; longer proper-nouns live in glossary

APPLY = '--apply' in sys.argv

# Load glossary canonical mapping
glossary = json.load(open('/home/anr2/u6-cht/dumps/glossary.json', encoding='utf-8'))
kw_map = {}  # 'gargoyle' (lowercase, no @) → '魔像'
for tag, zh in glossary.get('keywords_common', {}).items():
    if tag.startswith('@'):
        en_key = tag[1:].lower()
        zh_clean = zh.lstrip('@')
        kw_map[en_key] = zh_clean


def extract_zh_token(zh, at_pos):
    """from @-position, scan up to FALLBACK_CHAR_CAP chinese chars or until breaker."""
    end = at_pos + 1
    chars = 0
    while end < len(zh) and chars < FALLBACK_CHAR_CAP:
        c = zh[end]
        if not ('一' <= c <= '鿿'):
            break
        if c in BREAKERS:
            break
        end += 1
        chars += 1
    return zh[at_pos+1:end], end


stats = {'files_changed': 0, 'entries_changed': 0, 'glossary_hits': 0, 'fallback_scan': 0, 'already_bilingual': 0}
samples = []

for path in sorted(glob.glob('/home/anr2/u6-cht/dumps/translations/*.json')):
    fn = os.path.basename(path)
    if '_engine' in fn or '_batch' in fn:
        continue
    try:
        d = json.load(open(path, 'r', encoding='utf-8'))
    except: continue
    file_changed = False
    for tr in d.get('translations', []):
        en = tr.get('en', '')
        zh = tr.get('zh', '')
        if not en or not zh: continue
        en_kws = en_re.findall(en)
        if not en_kws: continue
        if re.search(r'@[A-Za-z]', zh):
            stats['already_bilingual'] += 1
            continue

        # Find @ positions in zh
        at_positions = [i for i, c in enumerate(zh) if c == '@']
        if not at_positions: continue

        new_zh_parts = []
        last = 0
        n = min(len(en_kws), len(at_positions))
        for i in range(n):
            at_pos = at_positions[i]
            en_kw = en_kws[i]
            # Try glossary canonical first
            canonical = kw_map.get(en_kw.lower())
            if canonical:
                # Find approx zh token length to skip past (use fallback scan)
                zh_token, end = extract_zh_token(zh, at_pos)
                new_zh_parts.append(zh[last:at_pos])
                new_zh_parts.append(f'@{en_kw}（{canonical}）')
                last = end
                stats['glossary_hits'] += 1
            else:
                zh_token, end = extract_zh_token(zh, at_pos)
                new_zh_parts.append(zh[last:at_pos])
                if zh_token:
                    new_zh_parts.append(f'@{en_kw}（{zh_token}）')
                else:
                    new_zh_parts.append(f'@{en_kw}')
                last = end
                stats['fallback_scan'] += 1

        # Remaining @ markers (more zh @ than en kw) → strip @ only
        for at_pos in at_positions[n:]:
            # safety: at_pos should be >= last
            if at_pos < last: continue
            new_zh_parts.append(zh[last:at_pos])
            last = at_pos + 1  # skip the @ char

        new_zh_parts.append(zh[last:])
        new_zh = ''.join(new_zh_parts)
        if new_zh != zh:
            if len(samples) < 10:
                samples.append((fn, en[:60], zh, new_zh))
            tr['zh'] = new_zh
            stats['entries_changed'] += 1
            file_changed = True

    if file_changed:
        stats['files_changed'] += 1
        if APPLY:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(d, f, ensure_ascii=False, indent=1)
                f.write('\n')

print(f'\nstats: {stats}')
print(f'\nfirst 10 samples:')
for fn, en, zh_old, zh_new in samples:
    print(f'  {fn}: {en}')
    print(f'    OLD: {zh_old}')
    print(f'    NEW: {zh_new}')
print(f"\n{'DRY-RUN — no files written. Re-run with --apply.' if not APPLY else 'CHANGES WRITTEN.'}")
