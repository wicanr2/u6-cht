# u6-cht — Project Context & Glossary

Ultima VI: The False Prophet（1990, Origin Systems）→ ScummVM Nuvie + Plan B load-time 中文化。

> **任何 sub-agent 第一輪先讀本檔 + 對應 task 指向的下層文件。** 別重新摸索既有 know-how —
> 5 輪 tester pass 與 12 個踩過的坑都已整理。

---

## 1. 文件索引（按使用場景）

### 「我要玩遊戲 / 派 game-tester / 驗中文化」
→ **`docs/PLAYTEST.md`** — 5 輪 tester pass 萃取的 onboarding：環境、鍵序、autosave、LB 對話、第一場戰役、CHT debug log 訊號表、已知雷 9 條。

### 「我要改翻譯 / 新增 NPC / 動 engine hook」
→ **`skills/u6-cht.md`** — engine hook 點清單（usecode/converse/events/msg_scroll）、二進位 lookup 格式 v3、漏翻 SOP、Windows mingw build 雷。

### 「我要重打包 Windows release / 處理 issue #2」
→ `dist/windows/run-free.bat` / `run-full.bat` (CRLF source of truth) + `repack.sh` + `skills/u6-cht.md` § 重打包章節。

### 「譯名要參照權威」
→ `dumps/glossary.json`（420+ 條）+ `DDSC-J-00007-創世紀聖者之書特別版.pdf`（1992 主權威）+ `DDSC-J-00124-遊戲手冊：創世紀６.pdf`（副）。**衝突時聖者之書優先**（user rule 2026-05-22）。

### 「ship 規劃 / release note」
→ `CHANGELOG.md` + `RELEASE_NOTES_v1.1.md` + `README.md`。

### 「歷次實機驗證」
→ `dumps/tester_pass{2,3,4,5,6}_report.md`（時序）、`dumps/screenshot_audit_report_v15.md`（最後 v1.5 audit）。

---

## 2. 路徑 cheatsheet

| 位置 | 用途 |
|---|---|
| `/home/anr2/u6-cht/` | 專案根 |
| `scummvm-src/scummvm` | patched ScummVM binary（137 MB，已 build）|
| `scummvm-src/engines/ultima/nuvie/` | engine source（修 hook 點看這裡）|
| `working/game/` | Ultima VI 原版 data + `cht_strings.tab` + `big5_u6_12x12.fnt` + SAVEGAME/ |
| `translations/` | en+zh 譯文 **(git tracked、source of truth)** — `build_lookup_table.py` 讀這份 |
| `translations_public/` | hash+zh 譯文（公開版本，不含 en 原文）|
| `dumps/translations/` | **已淘汰**（v1.5.2 起，build 改讀 `translations/`，見 dumps/translations/README.md）|
| `dist/windows/` | Windows release .bat source of truth (CRLF)、repack.sh |
| `tools/` | Python 工具（`build_lookup_table.py`、`fix_term_drift.py`、`teleport.py`、`extract_u6_images.py`…）|
| `patches/scummvm-u6cht.patch` | engine patch（GPL）|
| `releases/` | 出貨 zip / AppImage（**gitignored** — FULL 版含遊戲檔不公開）|
| `docs/` | 文件與 README screenshot |

---

## 3. Ubiquitous Language（譯名 / 術語）

### 3.1 角色 / 機構

| EN | 中文（權威） | 出處 | 避免 |
|---|---|---|---|
| Lord British | 不列顛王 | 聖者之書 | LB / 大不列顛 |
| Avatar | 聖者 | 聖者之書 | 化身 / 阿瓦塔 |
| Iolo | 尤洛 | 聖者之書 | 約洛 |
| Dupre | 杜普雷 | 聖者之書 | 杜普利 / 杜布雷 |
| Shamino | 夏米諾 | 聖者之書 | 沙米諾 |
| Mariah | 瑪萊雅 | 聖者之書 | 瑪麗亞 |
| Sentri | 山特利 | 聖者之書 | 仙特立 |
| Nystul | 尼斯托 | 聖者之書 | 尼斯特 |
| Geoffrey | 傑佛瑞 | 聖者之書 | 喬佛瑞 |
| Sin'Vraal | 辛弗拉 | 聖者之書 | 辛夫拉爾（drift 已修） |
| Chuckles | 笑笑 | 聖者之書 | 查克 / 笑哥 |
| Sherry | 雪莉 | 聖者之書 | 雪麗 |
| Gargoyle (s) | 魔像 / 魔像族 | 聖者之書 | 石像 / 加爾果 |

### 3.2 城市 / 地理（八德八城）

| EN | 中文 | 美德 |
|---|---|---|
| Britain | 不列顛城 | 慈悲 (Compassion) |
| Moonglow | 月光城 | 誠實 (Honesty) |
| Trinsic | 特林希克 | 榮譽 (Honor) |
| Yew | 紫衫城 | 正義 (Justice) |
| Minoc | 米諾克 | 犧牲 (Sacrifice) |
| Jhelom | 哲倫 | 勇敢 (Valor) |
| Skara Brae | 史卡拉布雷 | 靈性 (Spirituality) |
| New Magincia | 新馬精西亞 | 謙卑 (Humility) |

### 3.3 概念物品

| EN | 中文 |
|---|---|
| Codex of Ultimate Wisdom | 終極智慧守則之書（簡稱「守則之書」）|
| Compendium | 典籍 / 聖者之書（指 manual lookup quiz）|
| Orb of the Moons | 月之球 |
| Moongate | 月之門 |
| eight virtues | 八德 |
| Stranger | 異世界來客 |

### 3.4 系統用語

| EN | 中文 |
|---|---|
| Use | 使用 |
| Look | 察看 |
| Talk | 對話 |
| Attack | 攻擊 |
| Get | 取得 / 拾起 |
| `>進入戰鬥！` `>脫離戰鬥！` | combat mode toggle |
| `opened!` / `closed!` | 已開啟！/ 已關閉！ |
| `Thou dost see ` | 汝見 |
| `Nothing happens.` | 毫無動靜。 |
| `Out of range.` | 搆不著。 |

### 3.5 第二人稱與語氣

統一規則（pass5/6 編輯校對）：
- 一般敘述：「**汝**」（古文感）
- NPC 個性化：杜普雷「兄弟 / 老朋友」、夏米諾「老友 / 摯友」、尼斯托「老朽 / 聖者」
- 不混用「你 / 妳」與「汝」於同一段

---

## 4. 標誌性數字（用來 sanity check）

| 項 | 數字 |
|---|---|
| NPC 翻譯檔總數 | ~206（含 `_engine_*.json` + `_keywords.json`）|
| `cht_strings.tab` baseline (v1.5.2) | **7298 entries + 189 fragments** (v3, hashed) |
| Big5 字型 | `big5_u6_12x12.fnt`（12×12，3 font path 共用）|
| 翻譯主版本 | v1.5.1 ship、v1.5.2 開發中 |
| OBJLIST actor table | offset `0x100 + actor#*3`，3 bytes 解 x/y/z (10-bit each) |
| Avatar = actor #1，LB = actor #5 | 見 `tools/teleport.py` |

---

## 5. Flagged ambiguities（待釐清）

- **Lord British 後綴**：tester report B-02 指出 Dupre 用「不列顛王」、Geoffrey 用「不列顛王陛下」混用。第二次出現用「陛下」做代詞是規則嗎？尚未統一。
- **`tile` token leak**（issue #1.2）：v1.5.2 加 11 條候選 fragment，需實機 `CHT-LOOK ground:` 驗證真實字串長相再微調。
- **LB `the noble ruler of...`**（issue #1.3）：表內 5 變體都已收但仍 leak — 需實機 `CHT-LOOK actor-look:` 抓真實 aname 看是第 6 變體還是其他。
- **「杜」glyph 視覺辨識**（2026-06-27 朋友 finding）：12px WQY Sharp embedded bitmap 的「杜」字 row 3 像素接近「壯」/「狀」/「牡」，玩家會誤認。字型 atlas 內字本身正確（Big5=A7F9）。修法選項 A-D 見 docs/PLAYTEST.md § 8 第 10 條與 task #19。

---

## 6. Conventions

- commit message：中文，trailer 帶 `Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>`。
- push 用 `GIT_SSH_COMMAND="ssh -i ~/.ssh/id_github_wicanr2 -o IdentitiesOnly=yes" git push`。
- 不上傳含遊戲檔的 FULL release 到 GitHub（IP）— FULL 版只留 local `releases/`。
- 不 commit cht_strings.tab / 任何 .bak* / dumps/ 內 working 產物。
