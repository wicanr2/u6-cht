#!/usr/bin/env python3
"""
修正已 bilingual 化譯文中的括號內容：若 canonical map 中有更準確的譯名，
就以 canonical 取代 fallback scan 抓的中文片段。

例：`@Captain（黎奧）` → `@Captain（船長）`
"""
import json, re, glob, os, sys

APPLY = '--apply' in sys.argv

# Load glossary canonical
g = json.load(open('/home/anr2/u6-cht/dumps/glossary.json', encoding='utf-8'))
kw_map = {}
for tag, zh in g.get('keywords_common', {}).items():
    if tag.startswith('@'):
        kw_map[tag[1:].lower()] = zh.lstrip('@')

# Extra common terms (same as bilingual_keywords.py EXTRA_KW)
EXTRA = {
    'captain':'船長', 'lord':'王', 'sir':'爵士', 'king':'國王', 'queen':'女王', 'lady':'夫人',
    'hubert':'胡伯', 'lion':'獅', 'pirate':'海盜', 'pirates':'海盜', 'ship':'船', 'sail':'航行',
    'sailing':'航行', 'sea':'海', 'forest':'森林', 'woods':'森林', 'tree':'樹', 'home':'家',
    'friend':'朋友', 'friends':'朋友', 'mother':'母親', 'father':'父親', 'family':'家人',
    'wife':'妻', 'husband':'夫', 'son':'兒子', 'daughter':'女兒', 'brother':'兄弟', 'sister':'姊妹',
    'gold':'金幣', 'money':'金幣', 'food':'食物', 'drink':'飲品', 'fish':'魚', 'meat':'肉',
    'work':'工作', 'help':'幫助', 'quest':'試煉', 'song':'歌', 'story':'故事', 'stories':'故事',
    'book':'書', 'spell':'咒語', 'magic':'魔法', 'mage':'法師', 'wizard':'巫師',
    'spider':'蜘蛛', 'silk':'絲', 'silver':'銀', 'serpent':'蛇', 'guard':'衛兵', 'guards':'衛兵',
    'town':'城', 'city':'城', 'castle':'城堡', 'inn':'客棧', 'room':'房間', 'door':'門', 'key':'鑰匙',
    'weapon':'兵器', 'sword':'劍', 'bow':'弓', 'shield':'盾', 'armor':'盔甲',
    'leave':'離隊', 'join':'入伙', 'avatar':'聖者', 'compendium':'典籍', 'codex':'知識寶典',
    'wisp':'幽影', 'wisps':'幽影', 'orb':'月之球', 'moon':'月光石', 'moonstone':'月光石',
    'shrine':'聖壇', 'virtue':'美德', 'mantra':'真言', 'rune':'符文',
    'banquet':'宴會', 'banquets':'宴會', 'damsel':'佳人', 'damsels':'佳人',
    'grail':'聖杯', 'grails':'聖杯', 'gratitude':'謝意', 'beliefs':'信念', 'belief':'信念',
    'stones':'石頭', 'british':'不列顛王', 'lycaeum':'學苑', 'xiao':'蕭', 'power':'威力',
    'powder':'火藥', 'kegs':'桶', 'torches':'火把', 'oil':'油', 'lockpicks':'撬鎖工具',
    'gems':'寶石', 'backpacks':'背包', 'bags':'袋子', 'shovels':'鏟子',
    'favor':'恩情', 'fourth':'第四', 'pastry':'點心', 'dragon':'巨龍', 'egg':'蛋',
    'sauce':'醬汁', 'whitsaber':'白刃', 'leonna':'里歐娜', 'john':'約翰',
    'ham':'火腿', 'biscuits':'餅乾', 'repairs':'修繕', 'dreams':'夢境',
    'golden':'金鹿', 'hind':'號', 'gargoyles':'魔像族', 'gargoyle':'魔像',
    'instruction':'習藝', 'fencing':'擊劍', 'instructor':'教師', 'tip':'劍尖',
    'foil':'銳劍', 'lesson':'一課',
}
for k, v in EXTRA.items():
    if k not in kw_map:
        kw_map[k] = v

# Pattern: @ENGLISH（CURRENT_ZH） — Chinese paren
# Note: 「（」 = U+FF08 fullwidth left paren, 「）」 = U+FF09
pat = re.compile(r'@([A-Za-z][A-Za-z0-9\']*)（([^）]+)）')

stats = {'files': 0, 'fixed': 0, 'unchanged': 0}
samples = []
for path in sorted(glob.glob('/home/anr2/u6-cht/dumps/translations/*.json')):
    fn = os.path.basename(path)
    if '_engine' in fn or '_batch' in fn or fn == 'BOOK_DAT.json':
        continue
    try:
        with open(path, 'r', encoding='utf-8') as f:
            text = f.read()
    except: continue
    orig = text
    def repl(m):
        en, zh_old = m.group(1), m.group(2)
        canonical = kw_map.get(en.lower())
        if canonical and canonical != zh_old:
            stats['fixed'] += 1
            if len(samples) < 8:
                samples.append((fn, en, zh_old, canonical))
            return f'@{en}（{canonical}）'
        stats['unchanged'] += 1
        return m.group(0)
    new_text = pat.sub(repl, text)
    if new_text != orig:
        stats['files'] += 1
        if APPLY:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(new_text)

print(f'\nstats: {stats}')
print(f'\nfirst 8 fixes:')
for fn, en, old, new in samples:
    print(f'  {fn}: @{en}（{old}） → @{en}（{new}）')
print(f"\n{'DRY-RUN — re-run with --apply' if not APPLY else 'CHANGES WRITTEN'}")
