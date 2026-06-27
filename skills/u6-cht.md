---
name: u6-cht
description: Ultima VI 繁體中文化專案的工作流知識庫。包含 Plan B 架構、Big5 字型、翻譯流程、engine hook 點、所有踩過的坑。新 session 直接讀這份就能無痛接手。
---

# Ultima VI 繁體中文化 Skill

> 一份給未來 Claude session（或人類協作者）的速通文件。讀完即可承接這個專案。

## 30 秒摘要

- **目標**：把 1990 年 Origin Systems *Ultima VI: The False Prophet* 漢化為繁體中文（Big5），跑在 **ScummVM/Nuvie engine** 上。
- **路線**：**Plan B 載入時字串替換**（不動 `CONVERSE.A` bytecode，engine 印字前查 lookup 表替換英文 → 中文）。
- **狀態**：v1.5 已 ship。199 NPC + BOOK.DAT + 27 個 intro cinematic Lua chunks 翻完、7298+ lookup entries + 170 fragments、in-game Big5 渲染驗證。GitHub: https://github.com/wicanr2/u6-cht
- **語言風格**：文白並用古典中文（thee/thou → 汝/卿、'tis → 此乃）。LB 用「朕/卿」國王語。
- **譯名最高權威**：1992 台灣《創世紀聖者之書》（user rule 2026-05-22「翻譯衝突以聖者之書為主」）。詳見 [[譯名權威]] 節。
- **版本標籤**：v1.0 v1.1 v1.2 v1.2.1 v1.3 v1.3.1 v1.4 v1.5（Linux AppImage + Win 7z 各一份）

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
| **`ScriptCutscene::print_text` + `print_text_raw`** | intro cinematic Lua 字幕（v1.2 起）|

**注意：`MsgScroll::display_string` 看似中央 hook 但仍會漏**——`usecode/u6_usecode.cpp` 等檔案直接 hardcode 字串呼叫 scroll，這些字串走中央 hook 時若 fragment 表沒覆蓋就洩漏。**已知漏翻待補**：`cannon balls`（LB 王宮裝飾）、`the noble ruler of...`（08_lb_dialog 底部）。新發現按 [[漏翻字串 SOP]] 處理。

### Intro Cinematic Hook 特別說明（v1.2+）

Intro cinematic 在 `ScriptCutscene::ScriptCutscene` constructor 階段執行，**早於 `Game::init()`**，
而 CHTranslate 原本在 `Game::init()` 才載入。結果：intro 跑的時候 CHT 還沒準備好，整段 cinematic 顯示英文。

**修正**：在 `ScriptCutscene::ScriptCutscene` ctor 最早期（load assets 之前）加入：

```cpp
CHTranslate::get()->load(config);
```

確保 cinematic 啟動時 CHT 已就位。

### Lua chunk fragment split 原理

`print_text` 把 intro 字幕按換行拆成多個 Lua chunk 分次呼叫 engine。
每個 chunk 必須對 fragment 表 **完全匹配**（字元都不差）才能命中。

**Debug 技巧**：在 `ScriptCutscene::print_text` 加：
```cpp
debug(1, "CIN: %s", s);
```
啟動 ScummVM 加 `--debuglevel=1`，即可在 stderr 看到每個 Lua 實際傳入的 chunk 字串，
再把這些字串逐條加入 `_engine_fragments.json`。

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

### 漏翻字串 SOP（user 回報某個對話框出現英文時）

**症狀**：in-game 看到英文 token，例如 `opened!`、`closed!`、`cannon balls`。

**步驟**：
```bash
# 1. grep engine source 找來源（不是只搜 translations/）
grep -rn '"<English snippet>"' scummvm-src/engines/ultima/nuvie/
# 重點掃描位置：
#   usecode/u6_usecode.cpp    ← 容器/門/物件互動 hardcoded scroll->display_string
#   converse/converse.cpp     ← hardcoded converse engine 字串
#   core/events.cpp           ← Look/Search 命令文字
#   gui/widgets/msg_scroll.cpp ← 中央 hook

# 2. 確認是 scroll->display_string / Converse::print / nscript_print 哪一支

# 3. 加 fragment 到 translations/_engine_fragments.json
#    必須 cover 三種 \n 變體（呼叫端可能 trim 或包 \n）：
#      "\nopened!\n" / "opened!\n" / "opened!"

# 4. rebuild（不需 rebuild engine）
python3 tools/build_lookup_table.py

# 5. 重啟 ScummVM 驗證
```

**已知例子**：
- `u6_usecode.cpp:466,471` 容器開關 → `\nopened!\n` / `\nclosed!\n`
- `u6_usecode.cpp:1739` → `\nCan't (Un)lock an opened door\n`
- 這些都是 **detection table 找不到、只能 grep engine source 才知道** 的隱藏 hardcoded string。

---

## Windows mingw build gotcha（v1.4 踩坑）

### 症狀
Wine 或實機跑 `scummvm.exe ultima6`：
```
WARNING: ultima failed to instantiate engine: Game id not supported
(target 'ultima6', path '...')!
```
但 `scummvm.exe --list-all-games | grep ultima6` 卻列出 `ultima:ultima6` — **detection 看得到但 instantiate 拒絕**。

### 根因
`engines/ultima/metaengine.cpp:203` 的 createInstance 用 `#ifdef ENABLE_ULTIMA6` 包住 Nuvie 引擎。configure 在這條鏈失敗：

```
add_engine ultima6 ... "highres 16bit lua"     ← ultima6 依賴 lua
↓
--disable-all-engines --enable-engine=ultima   ← 只開 meta-engine，沒指定 sub-engines
↓
configure：「沒有任何啟用的 engine 需要 lua」→ Feature Lua is disabled as unused by enabled engines
↓
USE_LUA 不定義 → ultima6 依賴未滿足 → ENABLE_ULTIMA6 不定義
↓
createInstance 走 default → kUnsupportedGameidError
```

### 修法（mingw configure flags）
```bash
./configure --host=i686-w64-mingw32 \
  --disable-all-engines \
  --enable-engine=ultima,ultima6 \   # ← 必須顯式列 sub-engine
  --enable-lua \                     # ← 必須顯式 force lua（避免被 auto-disable）
  --enable-release-mode \
  --with-sdl-prefix=...
```

**驗證方法**：
```bash
grep -E "USE_LUA|ENABLE_ULTIMA6" config.h config.mk
# 預期看到：
#   config.h:#define USE_LUA
#   config.mk:ENABLE_ULTIMA6 = 1
#   config.mk:USE_LUA=1
```

### 為什麼 Linux build 沒事
本機 `./configure` 沒加 `--disable-all-engines`，預設 enable-all → 所有 sub-engine 默認開 → lua 被需要 → 自動 enable。Mingw build 為了縮 binary size 才 disable-all + 白名單 enable，結果踩這個 trap。

### Cross-compile 路徑
- Build tree: `/home/anr2/zak-cht-build/scummvm-win-src/`（**共用** zak-cht 那邊的 mingw build env，省 SDL2 mingw 依賴）
- 工具鏈: `i686-w64-mingw32-g++`（32-bit）
- SDL2: `~/zak-cht-build/mingw-deps/SDL2-2.28.5/i686-w64-mingw32/`
- 產出: `scummvm.exe` ~48 MB（含 Nuvie + Lua）；v1.4 漏 Lua 的版本是 ~38 MB

### 啟動 in-game test (Xephyr 無頭)
```bash
Xephyr -screen 800x600 :2 &
DISPLAY=:2 ./scummvm-src/scummvm --extrapath=... ultima6 &
DISPLAY=:2 xdotool key Escape; sleep 1; DISPLAY=:2 xdotool mousemove 400 500 click 1
DISPLAY=:2 ffmpeg -y -f x11grab -video_size 800x600 -i :2 -frames:v 1 /tmp/shot.png
```

### Screenshot pipeline tips（重拍 README 截圖時）

- **MD5 dedup check** 避免同一張圖誤用兩次：
  ```bash
  md5sum docs/screenshots/*.png | sort
  ```
  歷史教訓：v1.5 `09_intro_zh.png` 與 `11_intro_caption1.png` md5 完全相同，是 agent 拍 intro 時取了同一 frame。
- **`.bak` 已 gitignored**（`*.bak` / `*.bak.*`）— 重拍前 `cp x.png x.png.bak` 保留 rollback 路徑，不會污染 git
- **Xephyr `:2`** — 不要踩到本機 `:0`/`:1`。確認 `ps aux | grep Xephyr` 沒衝突
- **xdotool 大小寫敏感** — `Return` vs `return` 不同；`l` vs `L` 觸發不同 binding（U6 用小寫 `l` = Look）
- **Intro cinematic timing** — ScummVM 啟動後等 5–10s 才開始播 intro；ffmpeg 抓 frame 要算好時點
- **不能自動拍的場景** → 列在 audit 報告標 `MANUAL`，請 user 手動跑（戰鬥、LB Quiz、特定 NPC 對話）

### 從遊戲資料抽圖：世界地圖 + NPC 頭像（v1.5.2 README 重繪）

純 Python 解碼，**不連 engine、不需外部素材**。工具：`tools/extract_u6_images.py`（解碼器）、`tools/build_readme_art.py`（標註地圖 + 頭像牆生成）。

三個格式要點（都 port 自 nuvie，逐位驗證過）：

- **U6 LZW**（`U6Lzw::decompress_buffer`）：4-byte LE uncompressed-size header → 9~12 bit 變長 codeword，`0x100`=reset dict、`0x101`=EOF，dict 從 `0x102` 起。`source += 4` 跳過 header 再解。
- **U6Lib_n 容器**（`PORTRAIT.A/B`）：U6 type 無 4-byte 檔頭，offset table 為 4-byte entries，**top byte = flag**、低 3 bytes = offset。`num_items` 靠「掃到第一個 data block」推算。
- **關鍵坑**：portrait item 即使 lib flag=0（未壓），**item bytes 本身仍是獨立 LZW 流**（nuvie `PortraitU6::get_portrait_data` 永遠再跑一次 `lzw.decompress_buffer`）。所以要 lib 解出 item → 再 LZW 解一次 → 才得 56×64 indexed。
- **U6PAL**：前 768 bytes = 256 色 RGB，6-bit；還原成 8-bit 要 `value << 2`（見 `GamePalette::loadPalette`）。768 之後是輔助資料，別讀進來。
- **世界地圖**：`WORLDMAP.BMP` 是單一 LZW 流，解出 128×128 戰略 overview（1 px = 8×8 tiles）。直接套 U6PAL 即得真實 Britannia 全景。

**城市 pin 座標取真值**：讀 `SAVEGAME/OBJLIST` offset `0x100 + actor#*3`，3 bytes 解 `x=b1+((b2&3)<<8)`、`y=((b2&0xfc)>>2)+((b3&0xf)<<6)`（10-bit，0–1023）。overview 座標 = tile/8。actor# = 譯檔檔名數字（portrait index = actor#−1）。各城代表 NPC 用 OBJLIST 真實位置 → pin 不靠手繪。驗證歸屬可 grep 該 NPC 譯檔的 zh/en 找城市自稱（如 Zellivan 譯檔出現 "Jhelom"+"valor"）。

### 重打包 Windows release zip

```bash
# 用最新 mingw scummvm.exe + 原有 engine-data + u6cht-data
cd /tmp && rm -rf u6cht-VER-windows && mkdir u6cht-VER-windows
cp /home/anr2/zak-cht-build/scummvm-win-src/scummvm.exe u6cht-VER-windows/
cp /home/anr2/zak-cht-build/scummvm-win-src/SDL2.dll u6cht-VER-windows/  # 若 mingw build 沒含
cp -r <previous release>/engine-data u6cht-VER-windows/
mkdir u6cht-VER-windows/u6cht-data
cp /home/anr2/u6-cht/working/game/cht_strings.tab u6cht-VER-windows/u6cht-data/
cp /home/anr2/u6-cht/working/game/big5_u6_12x12.fnt u6cht-VER-windows/u6cht-data/
# run.bat 永遠取 dist/windows/ 的 source of truth（CRLF 已驗），不要從前版 zip 沿用
cp /home/anr2/u6-cht/dist/windows/run-free.bat u6cht-VER-windows/run.bat   # free / FULL 各一份
# README.txt 沿用前版（更新 VER 字串）
7z a -t7z -mx=9 u6cht-VER-windows-x86.7z u6cht-VER-windows/
mv u6cht-VER-windows-x86.7z /home/anr2/u6-cht/releases/
```

或對「現有 release 7z」做 hotfix 重打（issue #2 v1.5.1 → v1.5.1a 即此法）：

```bash
./dist/windows/repack.sh releases/u6cht-1.5.1-windows-x86.7z      free  releases/u6cht-1.5.1a-windows-x86.7z
./dist/windows/repack.sh releases/u6cht-1.5.1-FULL-windows-x86.7z full  releases/u6cht-1.5.1a-FULL-windows-x86.7z
```

**驗證**：
1. `file <root>/run.bat` 必須含 `CRLF line terminators`；缺了就是回到舊雷。
2. `wine cmd /c run.bat fakedir </dev/null` 應該乾淨走 ERROR 分支、`exit /b 1`、無 syntax error。
3. 解壓另一目錄，wine 跑 `scummvm.exe ultima6` 期望看不到 `Game id not supported`。

**踩過的雷（issue #2, 2026-06）**：Linux 工作環境寫的 `.bat` 預設 LF，**Windows CMD 跑 LF .bat 會 syntax error**，wine cmd 卻寬容地照跑 → 「我這邊 wine 可以」騙過了三個 release（v1.3→v1.5.1）。修法：(1) `.bat` source 集中在 `dist/windows/` 並用 `file` 確認 CRLF；(2) 別再 `>/dev/null`（Windows 是 `>nul`）；(3) 用 `repack.sh`，它會檢查 source 是 CRLF + repack 後再驗一次。對應 rule 82「Wine 跑得起來 ≠ Win10/11 cmd 跑得起來」。

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
13. **usecode hardcoded scroll->display_string** — `engines/ultima/nuvie/usecode/u6_usecode.cpp` 直接寫死 `"\nopened!\n"` 等字串。中央 hook 雖能截到，但 fragment 表沒收就漏。grep `display_string` 整個 usecode/ 才找全。詳見 [[漏翻字串 SOP]]
14. **mingw build 漏 ENABLE_ULTIMA6** — Windows cross-compile 因 lua auto-disable 連鎖反應導致 ultima6 沒編進去。詳見 [[Windows mingw build gotcha]]

---

<a name="譯名權威"></a>
## 譯名權威：1992 聖者之書優先

**User rule 2026-05-22**：翻譯衝突時以 1992 台灣《創世紀聖者之書》為準（不是 v1.3 那種「以多數使用統一」邏輯）。理由：**老玩家才能理解**，1992 的中文化是台灣 Ultima 圈的共同記憶。

兩份權威 PDF（repo 根目錄 untracked，含版權不入 git）：

| 檔 | 來源 | 內容 |
|---|---|---|
| `DDSC-J-00007-創世紀聖者之書特別版.pdf` | 台灣電腦玩家雜誌 1992 (83p) | **主**：八德 / 城名 / Avatar 對話 / lore |
| `DDSC-J-00124-遊戲手冊：創世紀６.pdf` | 軟體世界 1992 (13p) | **副**：職業 / 26 魔法音節 / 物品 / 操作 |

衝突處理 SOP：
1. 看聖者之書（主） — 通常翻得最完整
2. 看遊戲手冊（副） — 涵蓋系統用語
3. 都沒有才自行音/意譯
4. **凡 user 規則覆蓋既有譯法 → 寫進 [[重要譯名變動記錄]]，並用 `tools/fix_term_drift.py` 全域 sweep**

歷史教訓：v1.3 把 Trinsic 統一成「崔西克」（多數出現次數），v1.5 user 指出聖者之書是「特林希克」，整個反轉並重拍 13 個 NPC + 截圖。今後判斷 conflict **先看聖者之書，再決定**。

---

## 名詞對照（節錄）

完整見 `dumps/glossary.json`。

| EN | 中譯 | 備注 |
|---|---|---|
| Lord British | 不列顛王 | |
| Avatar | 聖者 | |
| gargoyle | 魔像族 | |
| Britannia | 不列顛尼亞 | |
| Britain | 不列顛城 | |
| Codex (of Ultimate Wisdom) | **知識寶典**（終極智慧知識寶典）| v1.1 起改：聖者之書 1992 正典用語 |
| Singularity | 獨一 | |
| Control / Passion / Diligence | 控制 / 熱情 / 勤勉（魔像族三原則）| |
| Honesty / Compassion / Valor | 誠實 / 慈悲 / **勇敢**（八德前三） | Valor = 勇敢（v1.2 起），非「勇氣」|
| Honor | 榮譽 | v1.2 統一（多數用法 25:12）|
| Trinsic | **特林希克** | v1.5 反轉 v1.3（聖者之書 p21-23）|
| Jhelom | 傑隆 | v1.3 統一（從哲倫改）|
| Minoc | **米諾克** | v1.5 改（聖者之書 p23，從密諾克）|
| Troll | **巨人** | v1.5 改（聖者之書 p52 + 遊戲手冊 p43，從山怪）|

### 重要譯名變動記錄

| 版本 | 舊譯 | 新譯 | 原因 |
|---|---|---|---|
| v1.1 | Codex 守則之書 | 知識寶典 | 聖者之書 1992 正典用語 |
| v1.2 | Valor 勇氣 | 勇敢 | 統一 4 個 NPC / 5 處（044/049/127/160）|
| v1.2 | Honor 榮耀 | 榮譽 | 多數用法（NPC 197）|
| v1.3 | Trinsic 川辛/特林希克 | 崔西克 | 全域統一 |
| v1.3 | Jhelom 哲倫 | 傑隆 | 全域統一 |
| **v1.5** | Trinsic 崔西克 | **特林希克** | **反轉 v1.3**（user rule 2026-05-22：聖者之書優先；老玩家才能理解）|
| v1.5 | Minoc 密諾克 | 米諾克 | 聖者之書 p23 — 10 files |
| v1.5 | Troll 山怪 | 巨人 | 聖者之書 p52 + 遊戲手冊 p43 |

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
| Honor (榮譽) | T+C | summ | Trinsic 特林希克 |
| Spirituality (靈性) | T+L+C | om | Skara Brae |
| Humility (謙卑) | （皆無）| lum | New Magincia |

魔像族 = 鏡像三原則 **Control / Passion / Diligence**（控制 / 熱情 / 勤勉）。

---

## 聯絡與貢獻

- Repo: https://github.com/wicanr2/u6-cht
- Owner: wicanr2 (Chun-Yu Wang) <wicanr2@gmail.com>
- License: GPL (engine) / CC BY-SA (translations) / Apache 2.0 (font) / MIT (tools)
