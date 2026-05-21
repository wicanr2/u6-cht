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

# Add more canonical mappings derived from glossary people/places/concepts
EXTRA_KW = {
    'captain':   '船長',
    'lord':      '王',
    'sir':       '爵士',
    'king':      '國王',
    'queen':     '女王',
    'lady':      '夫人',
    'hubert':    '胡伯',
    'lion':      '獅',
    'pirate':    '海盜',
    'pirates':   '海盜',
    'ship':      '船',
    'sail':      '航行',
    'sailing':   '航行',
    'sea':       '海',
    'forest':    '森林',
    'woods':     '森林',
    'tree':      '樹',
    'home':      '家',
    'friend':    '朋友',
    'friends':   '朋友',
    'mother':    '母親',
    'father':    '父親',
    'family':    '家人',
    'wife':      '妻',
    'husband':   '夫',
    'son':       '兒子',
    'daughter':  '女兒',
    'brother':   '兄弟',
    'sister':    '姊妹',
    'gold':      '金幣',
    'money':     '金幣',
    'food':      '食物',
    'drink':     '飲品',
    'fish':      '魚',
    'meat':      '肉',
    'work':      '工作',
    'job':       '職業',
    'name':      '名字',
    'bye':       '再見',
    'help':      '幫助',
    'quest':     '試煉',
    'song':      '歌',
    'story':     '故事',
    'stories':   '故事',
    'book':      '書',
    'spell':     '咒語',
    'magic':     '魔法',
    'mage':      '法師',
    'wizard':    '巫師',
    'spider':    '蜘蛛',
    'silk':      '絲',
    'silver':    '銀',
    'silvered':  '銀製',
    'serpent':   '蛇',
    'guard':     '衛兵',
    'guards':    '衛兵',
    'town':      '城',
    'city':      '城',
    'castle':    '城堡',
    'inn':       '客棧',
    'room':      '房間',
    'door':      '門',
    'key':       '鑰匙',
    'weapon':    '兵器',
    'sword':     '劍',
    'bow':       '弓',
    'shield':    '盾',
    'armor':     '盔甲',
    'leave':     '離隊',
    'join':      '入伙',
    'avatar':    '聖者',
    'compendium':'典籍',
    'codex':     '知識寶典',
    'wisp':      '幽影',
    'wisps':     '幽影',
    'orb':       '月之球',
    'moon':      '月光石',
    'moonstone': '月光石',
    'shrine':    '聖壇',
    'virtue':    '美德',
    'mantra':    '真言',
    'rune':      '符文',
    'forest':    '森林',
    'banquet':   '宴會',
    'banquets':  '宴會',
    'damsel':    '佳人',
    'damsels':   '佳人',
    'grail':     '聖杯',
    'grails':    '聖杯',
    'gratitude': '謝意',
    'beliefs':   '信念',
    'belief':    '信念',
    'stones':    '石頭',
    'british':   '不列顛王',
    'lycaeum':   '學苑',
    'xiao':      '蕭',
    'power':     '威力',
    'powder':    '火藥',
    'kegs':      '桶',
    'torches':   '火把',
    'oil':       '油',
    'lockpicks': '撬鎖工具',
    'gems':      '寶石',
    'backpacks': '背包',
    'bags':      '袋子',
    'shovels':   '鏟子',
    'favor':     '恩情',
    'fourth':    '第四',
    'pastry':    '點心',
    'dragon':    '巨龍',
    'egg':       '蛋',
    'eggs':      '蛋',
    'sauce':     '醬汁',
    'whitsaber': '白刃',
    'leonna':    '里歐娜',
    'john':      '約翰',
    'ham':       '火腿',
    'biscuits':  '餅乾',
    'repairs':   '修繕',
    'dreams':    '夢境',
    'golden':    '金',
    'hind':      '鹿',
    'gargoyles': '魔像族',
    'instruction': '習藝',
    'fencing':   '擊劍',
    'instructor':'教師',
    'tip':       '劍尖',
    'foil':      '銳劍',
    'lesson':    '一課',
}
for k, v in EXTRA_KW.items():
    if k not in kw_map:
        kw_map[k] = v


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
