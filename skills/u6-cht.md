---
name: u6-cht
description: Ultima VI 繁體中文化專案的工作流知識庫。包含 Plan B 架構、Big5 字型、翻譯流程、engine hook 點、所有踩過的坑。新 session 直接讀這份就能無痛接手。
---

# Ultima VI 繁體中文化 Skill

> 一份給未來 Claude session（或人類協作者）的速通文件。讀完即可承接這個專案。

## 30 秒摘要

- **目標**：把 1990 年 Origin Systems *Ultima VI: The False Prophet* 漢化為繁體中文（Big5），跑在 **ScummVM/Nuvie engine** 上。
- **路線**：**Plan B 載入時字串替換**（不動 `CONVERSE.A` bytecode，engine 印字前查 lookup 表替換英文 → 中文）。
- **狀態**：v1.0 已 ship。199 NPC + BOOK.DAT 翻完、7298 lookup entries + 40 fragments、in-game Big5 渲染驗證。GitHub: https://github.com/wicanr2/u6-cht
- **語言風格**：文白並用古典中文（thee/thou → 汝/卿、'tis → 此乃）。LB 用「朕/卿」國王語。

---

## 路徑 cheatsheet

| 位置 | 用途 |
|---|---|
| `~/u6-cht/` | 專案根 |
| `~/u6-cht/scummvm-src/` | ScummVM clone + 我們的 patches |
| `~/u6-cht/working/game/` | Ultima VI 原版 data + `cht_strings.tab` + `big5_u6_12x12.fnt`|
| `~/u6-cht/translations/` | en+zh 譯文（git tracked，含原版 source key）|
| `~/u6-cht/translations_public/` | hash+zh 譯文（公開版本）|
| `~/u6-cht/tools/` | Python 工具 |
| `~/u6-cht/patches/scummvm-u6cht.patch` | engine patch（GPL）|
| `~/u6-cht/dumps/glossary.json` | 名詞對照表（420+ 條）|
| `~/u6-cht/dumps/style_guide.md` | 風格指南 |
| `~/u6-cht/dumps/npc_extracted/` | 原版 `CONVERSE.A` 抽出 ASCII（**gitignored**）|

---

## 核心架構（Plan B）

```
原版 CONVERSE.A (English bytecode)
        ↓
    [Conv VM 解析 — 不動！]
        ↓
    add_text() 收集英文字串
        ↓
[Engine hook: CHTranslate::translate(en)]
        ↓
    cht_strings.tab v3 binary lookup
    (FNV-1a 64-bit hash → Big5 zh)
        ↓
    Big5 字串
        ↓
    [U6Font/ConvFont/WOUFont 渲染]
        ↓
    螢幕顯示中文
```

**為何 Plan B 而非 Plan A**：U6 conv VM 的 opcode 區間 0xA1-0xFE 與 Big5 lead byte 完全衝突（試過 6 版 heuristic 都掛）。Plan B 零 byte-alignment 風險。

---

## 三條 Big5 字型路徑

| 模組 | 用途 | 檔 |
|---|---|---|
| `U6Font` | MsgScroll 8×8（主對話面板）| `engines/ultima/nuvie/fonts/u6_font.{cpp,h}` |
| `ConvFont` | NewUI ConverseGump 變寬字 | `engines/ultima/nuvie/fonts/conv_font.{cpp,h}` |
| `WOUFont` | cutscene / intro 字體 | `engines/ultima/nuvie/fonts/wou_font.{cpp,h}` |

字型檔：`big5_u6_12x12.fnt`（WenQuanYi Zen Hei Sharp 12px embedded bitmap，由 `tools/build-big5-font-wqysharp.py` 生成）。

---

## Engine hook 點清單

漏掉任何一處英文就洩漏。已 hook 完：

| Hook | 用途 |
|---|---|
| `ConverseInterpret::do_text()` | NPC script dialogue（最主要）|
| `Converse::print(const char *s)` | hardcoded engine 字串如 "How can I join..." |
| `Converse::collect_input` SIDENT/SLOOK | NPC 名 / 描述 |
| `Book::get_book_data()` | BOOK.DAT 書籍/卷軸 |
| `Events::look(Actor*)` / `lookAtCursor` / `search` | Look 命令的 actor/ground/search 文字 |
| `nscript_print()` (Lua print) | prefix-aware「Thou dost see X.」拼接 |
| **`MsgScroll::display_string`（中央 hook）** | 所有 scroll 輸出最後一道防線 |
| `Player::get_gender_title()` | `$G` 變數 milord/milady → 公子/姑娘 |

---

## 二進位 lookup 格式 (`cht_strings.tab` v3)

```
8 bytes  magic "U6CHT\x00\x03\x00"
uint32   exact_count
exact records (× exact_count):
  uint64 LE  FNV-1a 64-bit hash of en
  uint16 LE  zh_len
  bytes     zh_big5
uint32   fragment_count
fragment records (× fragment_count):
  uint16 LE  en_len
  bytes     en (plain)
  uint16 LE  zh_len
  bytes     zh_big5
```

**為何 hash key**：可分發 binary 而不洩漏原版 English source。Fragment 走 plain 因需要 substring match。

---

## 常見工作流

### 改翻譯 → in-game 看效果
```bash
# 1. 編輯 translations/<NPC>.json 或 dumps/translations/<NPC>.json
vim translations/005_Lord\ British.json

# 2. 重建 lookup binary（< 1 秒）
python3 tools/build_lookup_table.py

# 3. 啟動 ScummVM（不需重編 engine）
DISPLAY=:2 ./scummvm-src/scummvm \
  --extrapath=./scummvm-src/dists/engine-data \
  --debuglevel=1 ultima6
```

### 改 engine code → rebuild
```bash
cd scummvm-src && make -j8
```

### 新增 / 重譯 NPC
```bash
# 1. 抽 source 字串
python3 tools/extract_npc_strings.py working/game/CONVERSE.A NN \
    > dumps/npc_extracted/NN_Name.json

# 2. 手動或 agent 翻成 translations/<NPC>.json
# 3. build_lookup_table.py
```

### 重做名詞統一
```bash
python3 tools/fix_term_drift.py   # 編輯 RULES dict 內的 src→dst pairs
python3 tools/build_lookup_table.py
```

### 啟動 in-game test (Xephyr 無頭)
```bash
Xephyr -screen 800x600 :2 &
DISPLAY=:2 ./scummvm-src/scummvm --extrapath=... ultima6 &
DISPLAY=:2 xdotool key Escape; sleep 1; DISPLAY=:2 xdotool mousemove 400 500 click 1
DISPLAY=:2 ffmpeg -y -f x11grab -video_size 800x600 -i :2 -frames:v 1 /tmp/shot.png
```

---

## 12 個踩過的坑（簡版，詳細看 README.md）

1. **Plan A 失敗** — U6 opcode 區 0xA1-0xFE 與 Big5 lead byte 撞，heuristic 無解
2. **UTF-8/Big5 編碼** — lookup 必須存 Big5 bytes，不能 UTF-8
3. **0x5C escape 撞 Big5 trail** — 88 個 Big5 字 trail = 0x5C（許/功/閱），改 binary format 解決
4. **CJK 無空格 wrap** — MsgScroll tokenizer 加 Big5 pair 獨立 token
5. **Line height 8 vs 12** — bump stride 8→10、drop baseline lift
6. **多輸出 codepath** — 8 個 hook 點必須全 cover
7. **Copy protection** — LB Compendium quiz 保留英文 + (答案: keyword) 括號註記
8. **Parallel agent normalize** — Sonnet agents 各譯各的，要後期 `fix_term_drift.py`
9. **byte-exact key** — translation `en` 欄位 1 byte 不對就 lookup miss
10. **Lua print** — `nscript_print` 加 prefix-aware substitution
11. **Lua dynamic 字串** — fragment substitution（inline find-replace）
12. **多段 add_text** — paragraph split (`\n\n` boundary) 拆開查表

---

## 名詞對照（節錄）

完整見 `dumps/glossary.json`。

| EN | 中譯 |
|---|---|
| Lord British | 不列顛王 |
| Avatar | 聖者 |
| gargoyle | 魔像族 |
| Britannia | 不列顛尼亞 |
| Britain | 不列顛城 |
| Codex (of Ultimate Wisdom) | 守則之書（終極智慧守則之書）|
| Singularity | 獨一 |
| Control / Passion / Diligence | 控制 / 熱情 / 勤勉（魔像族三原則）|
| Honesty / Compassion / Valor | 誠實 / 慈悲 / 勇氣（八德前三） |

## LB Compendium quiz 答案速查表

| 題目 | 答案 keyword |
|---|---|
| tangle vine doth put one to sleep | cent / pod / frag |
| trolls lack | end |
| giant squids crush prey | beak |
| silver serpent been seen | tomb / wall / anci / monu |
| reapers remnants of | anci / ench / fore |
| wisps oft mistaken for | fire / fly |
| headlesses produced | wiza / expe |
| spawning grounds of Hydras | nigh / mush |
| fend off rotworms | torc / fire / flam / burn / pass |
| sea serpents attack | fire / ball / swip / tail |

---

## 八德與三原則（劇情骨架）

人類八德 = 三原則 (Truth / Love / Courage) 之 2³ 排列：

| 德 | 構成 | 真言 | 對應城 |
|---|---|---|---|
| Honesty (誠實) | Truth | ahm | Moonglow 月光城 |
| Compassion (慈悲) | Love | mu | Britain 不列顛城 |
| Valor (勇氣) | Courage | ra | Jhelom 哲倫 |
| Justice (正義) | T+L | beh | Yew 尤伊 |
| Sacrifice (犧牲) | L+C | cah | Minoc 米諾克 |
| Honor (榮譽) | T+C | summ | Trinsic 川辛 |
| Spirituality (靈性) | T+L+C | om | Skara Brae |
| Humility (謙卑) | （皆無）| lum | New Magincia |

魔像族 = 鏡像三原則 **Control / Passion / Diligence**（控制 / 熱情 / 勤勉）。

---

## 聯絡與貢獻

- Repo: https://github.com/wicanr2/u6-cht
- Owner: wicanr2 (Chun-Yu Wang) <wicanr2@gmail.com>
- License: GPL (engine) / CC BY-SA (translations) / Apache 2.0 (font) / MIT (tools)
