---
name: u6-translation-workflow
description: Ultima VI 繁中化翻譯流程 skill。三輪 editor agent + tester 驗證、bilingual keyword 策略、distilled PDF 加速 review、Lua chunk fragment capture 全流程。新 session 讀完即可承接翻譯 / QA 工作。
---

# Ultima VI 翻譯工作流程 Skill

> 本文件記錄 u6-cht 專案從原文抽取到 in-game 驗證的完整翻譯流程，包含踩過的坑與有效的 agent 協作策略。

---

## 一、整體流程概覽

```
原版 CONVERSE.A
    ↓ tools/extract_npc_strings.py
dumps/npc_extracted/<NN>_Name.json   (English source)
    ↓ 翻譯 agent（Sonnet × 4 平行 or Opus 單跑）
translations/<NN>_Name.json          (en + zh 雙語 JSON)
    ↓ tools/build_lookup_table.py
data/cht_strings.tab                 (v3 binary lookup)
    ↓ ScummVM 載入 → in-game
    ↓ tester agent (xdotool + ffmpeg)
截圖驗證
```

---

## 二、翻譯 JSON 格式

```json
{
  "npc_id": "005",
  "npc_name": "Lord British",
  "translations": [
    {
      "en": "Thou art the Avatar?",
      "zh": "汝便是聖者？"
    },
    {
      "en": "@join",
      "zh": "@join（加入）"
    }
  ]
}
```

**重要約束**：
- `en` 欄位必須是 **byte-exact** 從 source 抽出的字串，禁止手打。
  1 個空格差異 → hash miss → in-game 顯示英文。
- `zh` 欄位為 UTF-8 儲存；`build_lookup_table.py` 自動轉 Big5 bytes。
- keyword 行用 `@keyword（中文）` 格式（bilingual 雙語，見下節）。

---

## 三、Bilingual Keyword 策略

### 問題背景

NPC 對話中有 `@keyword` 觸發詞，玩家要輸入英文關鍵字才能觸發對話分支。
若把 keyword 純翻成中文，玩家不知道要打什麼。
若完全保留英文，對話框裡英文 keyword 顯得突兀。

### 採用方案：`@english（中文）`

```
原文: @honor
譯文: @honor（榮譽）
```

玩家看到「榮譽」知道這個概念，用 `honor` 輸入依然觸發。視覺上兩語並存，體驗最佳。

### 工具

```bash
# 把翻譯 JSON 裡所有 @keyword 行規範化為雙語格式
python3 tools/bilingual_keywords.py

# 批次修正格式錯誤（@EN（ZH）ZH 重字等）
python3 tools/fix_at_duplicates.py
```

### Bilingual 格式規則

| 格式 | 處理方式 |
|---|---|
| `@honor（榮譽）` | ✅ 正確 |
| `@honor` | ⚠️ 缺中文，補上 |
| `@honor（榮譽）榮譽` | ❌ 重字，工具自動修正 |
| `@join` 類後接多個選項 | 每個選項獨立一行雙語 |

---

## 四、三輪 Editor Agent 方法

### 為何需要多輪

168 個 NPC 用 4 個 Sonnet agent 平行翻譯後，名詞漂移（term drift）難以避免：
- Codex 出現 4 種譯名（守則之書 / 智典 / 法典 / 終極智慧之典）
- Valor 同時出現「勇氣」與「勇敢」
- 個別 NPC 語氣漂移（Phoenix 全用「我/你」現代語）

三輪 review 分工明確，解決不同層次問題。

---

### 第一輪：Editor-in-Chief（P0 重要修正）

**任務**：抓語意錯誤、嚴重風格問題、名詞大幅誤譯

**Agent prompt 模板**：
```
你是一位資深繁體中文文學編輯，專精古典文言與遊戲在地化。
請審閱以下 Ultima VI NPC 對話翻譯，找出：
1. 語意嚴重錯誤（如 Singularity 譯成「獨身者」）
2. 名詞不符術語表（見 dumps/glossary.json）
3. 語氣嚴重不一致（如某 NPC 全用現代「我/你」）

術語表節錄：[貼上 glossary 前 30 條]
待審 JSON：[貼上目標 NPC JSON]
```

**產出**：editor_in_chief_report.md（P0 列表 + 修正建議）

---

### 第二輪：Novel Editor（文學潤色）

**任務**：評分 + 文學性提升，聚焦語感、節奏、文白平衡

**Agent prompt 模板**：
```
你是一位繁體中文文學小說編輯，請對以下 RPG 對話翻譯進行文學審閱。
評分標準（滿分 50）：
- 文白平衡（15分）：有古典味但不艱澀
- 角色聲音（15分）：LB 要有王者氣度，平民要接地氣
- 流暢度（10分）：中文讀起來是否自然
- 原味保留（10分）：Ultima 的莊嚴感是否延續

請給出：總分 / 每項得分 / 前 5 個高優先修正建議
```

**產出**：editor2_report.md（分數 + 修正清單）

---

### 第三輪：Editor3（精修 P0/P1 + 邊界情況）

**任務**：整合前兩輪意見，實際修正 JSON，同時處理：
- keyword bracket 對齊（`@keyword` 位置 vs. 後續對話）
- @number 的語意（`@number（音符）` vs. `@number（數字）`）
- 細節一致性（Captain John 操控 vs. 克制）

**工具**：
```bash
python3 tools/fix_p0_editor3.py        # 批次套用 editor3 修正
python3 tools/fix_bilingual_brackets.py # canonical map post-fix
```

---

## 五、名詞漂移修正工具

```bash
# 查名詞漂移
python3 tools/fix_term_drift.py --dry-run

# 套用修正（編輯 RULES dict 後執行）
python3 tools/fix_term_drift.py

# 例：RULES dict
RULES = {
    "終極智慧之典": "知識寶典",
    "智典": "知識寶典",
    "辛夫拉爾": "辛弗拉",
    "勇氣": "勇敢",   # 在 Valor 上下文
}
```

**注意**：`fix_term_drift.py` 做的是全文字串 replace，上下文盲目。
有些名詞（如「勇氣」在非 Valor 語境）可能需手動排除。執行後務必 diff 檢查。

---

## 六、Distilled PDF Reference 加速 Review

### 問題

聖者之書（聖者之書.pdf）+ 遊戲手冊（遊戲手冊.pdf）共約 100 頁，
每次 review 都去找正典譯名太費時。

### 解法：製作精華 distilled 版

```
dumps/distilled_sage_book.md    — 聖者之書 P1-50 精華（200 行）
dumps/distilled_manual.md       — 遊戲手冊 13 頁精華（120 行）
dumps/sage_book_cross_ref.md    — cross-ref 決策紀錄（譯名採用依據）
```

### 建立 distilled 方法

讓 agent 讀 PDF 並產出：
1. 所有出現的地名/角色名/術語 → 正典中文對應
2. 重要劇情段落的措辭參考
3. 有歧義的名詞（如 Codex）的採用決策

之後 review 時直接 grounding distilled 文件，不用重讀原 PDF。

### 已知正典依據

| 術語 | 正典來源 | 採用譯名 |
|---|---|---|
| Codex of Ultimate Wisdom | 聖者之書 1992 p.18 「知識寶典」| 知識寶典 |
| Reaper | 聖者之書 p.76 「樹妖」| 樹妖（非死神）|
| 大烏賊 | 遊戲手冊 + 聖者之書 一致 | 大烏賊（非巨型烏賊）|
| Valor | 遊戲手冊 德行篇 「勇敢」| 勇敢（非勇氣）|

---

## 七、Lua Chunk Fragment Capture 流程

### 問題背景

Intro cinematic 的字幕透過 Lua `image_print` 呼叫，每次只傳一個 chunk 給 engine。
Chunk 的切分方式不直觀（按 Lua script 的換行），必須知道 **實際傳入的 chunk 字串** 才能寫對應 fragment。

### Debug 方法

**Step 1：在 engine 加 debug log**

在 `ScriptCutscene::print_text` 加：
```cpp
debug(1, "CIN: [%s]", s);
```

**Step 2：帶 debuglevel 啟動**

```bash
DISPLAY=:2 ./scummvm-src/scummvm \
  --extrapath=./scummvm-src/dists/engine-data \
  --debuglevel=1 ultima6 2>&1 | grep "^CIN:" | tee /tmp/cin_chunks.txt
```

**Step 3：把抓到的 chunk 加入 fragment 表**

```json
// dumps/translations/_engine_fragments.json
{
  "fragments": [
    {
      "en": "You bolt from your house, stumbling, running blind in the",
      "zh": "你倉皇奪門而出，跌跌撞撞，在"
    },
    {
      "en": "storm. Into the forest, down the path, through the rain... to the stones.",
      "zh": "風雨中盲目奔跑……穿越森林，沿路而下，直奔那石陣而去。"
    }
  ]
}
```

**Step 4：rebuild + 驗證**

```bash
python3 tools/build_lookup_table.py
# 重啟 ScummVM 看 intro
```

### Chunk Fragment 匹配規則

- Fragment 表是 **有序列表**，先列出的先匹配。
- Fragment 匹配用 **substring find**（不是 exact），所以超長 chunk 可以用部分匹配。
- 但前綴衝突要小心：若 fragment A 是 B 的前綴，A 必須排在 B 之前。
- Cinematic chunk 通常以換行字元結尾或不帶結尾，測試時兩種都試。

---

## 八、Tester Agent 驗證流程

### 無頭驗證環境

```bash
# 啟動虛擬顯示器（只需一次）
Xephyr -screen 800x600 :2 &

# 啟動 ScummVM
DISPLAY=:2 ./scummvm-src/scummvm \
  --extrapath=./scummvm-src/dists/engine-data \
  --debuglevel=1 ultima6 &

# 等待載入，截圖
sleep 5
DISPLAY=:2 ffmpeg -y -f x11grab -video_size 800x600 -i :2 -frames:v 1 /tmp/shot.png
```

### Tester Checklist（每次 release 前）

| 測試項目 | 指令 | 預期結果 |
|---|---|---|
| 開場 intro cinematic | 啟動遊戲、等待 intro | 中文字幕 |
| Look 地板 | xdotool `l` + 滑鼠點地板 | 「汝見地板」|
| Look 牆 | xdotool `l` + 滑鼠點牆 | 「汝見一面牆」|
| Talk LB | hackmove 至 LB 旁 → `t` | 中文對話 |
| LB Quiz | 進 quiz 流程 | 英文題目 + (答案: xxx) |
| Combat 訊息 | 觸發戰鬥 | 「XXX 擦傷」等中文 |
| ? keyword | Talk → 輸入 `?` | 顯示 keyword 清單 |

### Tester Pass 報告格式

```
# Tester Pass N Report
日期：YYYY-MM-DD
版本：vX.Y.Z

## 結果摘要
PASS: N/M 項通過

## 各項結果
- Look 地板：✅ PASS「汝見地板」
- Talk LB：✅ PASS 中文對話
- LB Quiz：❌ FAIL 仍顯示英文題目（預期：保留英文 + 答案提示）
  → 注意：Quiz 保留英文是設計，FAIL 若是指純英文無提示

## 已知問題 / 待修
- ...
```

---

## 九、Fragment vs. Exact Lookup 選擇指南

| 字串類型 | 使用方式 | 原因 |
|---|---|---|
| NPC 固定對話行 | Exact（hash lookup）| 長度固定，hash 最快 |
| 書籍 / 卷軸文字 | Exact | BOOK.DAT 固定內容 |
| 戰鬥動態字串 `Iolo grazed.` | Fragment（substring replace）| actor 名是 runtime 變數 |
| Intro cinematic 字幕 | Fragment | Lua chunk split 不固定 |
| 方向 `north / south` | Fragment | 動態拼接 |
| 物件 look `Thou dost see X.` | Fragment（prefix rewrite）| `X` 是 runtime |

Fragment 表 vs. exact 表分開儲存在 v3 binary format：

```
magic "U6CHT\x00\x03\x00"
uint32 exact_count   → hash lookup 段
uint32 fragment_count → fragment 段（順序有意義）
```

---

## 十、常見錯誤與排查

### 症狀：某 NPC 對話全顯示英文

1. 確認 `translations/<NN>.json` 的 `en` 欄位是否 byte-exact。
2. 執行 QA 工具：
   ```bash
   python3 tools/check_en_match.py NN
   ```
3. 若有 mismatch，從 `dumps/npc_extracted/<NN>.json` 重取 source key。

### 症狀：Intro cinematic 某段仍英文

1. 加 `debug(1, "CIN: [%s]", s)` 到 `print_text`。
2. 比對 `/tmp/cin_chunks.txt` 與 `_engine_fragments.json`。
3. 通常是 chunk 末尾有多餘空格或 `\n`，fragment key 要完全一致。

### 症狀：中文字顯示亂碼（「瘙間」等）

- lookup 的 zh 欄位存到了 UTF-8 bytes 而非 Big5。
- 確認 `build_lookup_table.py` 的 `to_big5()` 使用 `s.encode('cp950', errors='replace')`。
- 若有 Big5 不支援的字（如部分罕用字），errors='replace' 會丟掉，需手動換同義字。

### 症狀：中文行與行重疊

- Big5 字高 12px > 原版 ASCII 8px。
- 目前 line stride = 10px（妥協值），2px 輕微重疊屬已知 limitation。
- 完整修正需改 `MsgScroll::scroll_height` + `cursor_y` stride logic。

### 症狀：keyword 觸發失效

- 確認 `@keyword（中文）` 的 `@keyword` 部分未被修改。
- engine 觸發機制比對的是 `@` 後的英文 keyword（case-insensitive）。
- `bilingual_keywords.py` 轉換後請再跑一次 `fix_at_duplicates.py` 確保無重字。

---

## 十一、並行翻譯 Agent 策略

### 分工原則

- **Tier 1（核心角色）**：Lord British、主要夥伴（8 人） → Opus 單跑，品質優先
- **Tier 2（城堡群 NPC）**：約 20 人 → Opus 或 Sonnet 高 temp，有 cross-talk
- **Tier 3（全 Britannia 168 人）**：4 個 Sonnet agent 平行，每個 42 人

### Agent Prompt 必帶內容

```
1. 術語表（dumps/glossary.json 節錄，至少前 50 條）
2. 風格指南（dumps/style_guide.md 全文，約 80 行）
3. 已完成的 Tier 1 範例（LB + Mariah 各 3 段，做為語氣對齊基準）
4. bilingual keyword 規則（@keyword → @keyword（中文）格式）
```

### 後期整合必做

```bash
# 1. 名詞漂移修正
python3 tools/fix_term_drift.py

# 2. bilingual keyword 規範化
python3 tools/bilingual_keywords.py

# 3. 重字清除
python3 tools/fix_at_duplicates.py

# 4. en-match 驗證（有 mismatch 就修）
python3 tools/check_en_match.py --all

# 5. rebuild binary
python3 tools/build_lookup_table.py
```

---

## 十二、統計與 KPI

截至 v1.3.1：

| 項目 | 數量 |
|---|---|
| Exact lookup entries | 7298+ |
| Plain fragments | 77 |
| NPCs 翻譯完成 | 199 / 199 |
| BOOK.DAT 條目 | 127 |
| Intro cinematic chunks | 27 / 27 |
| Engine hook 點 | 9 |
| 釋出版本 | 6（v1.0 ~ v1.3.1）|
| Binary lookup 大小 | ~330 KB |

---

## 十三、翻譯品質審核標準（50 分制）

| 評分維度 | 滿分 | 要點 |
|---|---|---|
| 文白平衡 | 15 | 有古典味但不艱澀，現代玩家能讀懂 |
| 角色聲音 | 15 | LB 王者氣度 / 平民接地氣 / 魔像族莊嚴 |
| 流暢度 | 10 | 中文讀起來自然，無翻譯腔 |
| 原味保留 | 10 | Ultima 的 EarlyModern English 莊嚴感延續 |

**目標分數**：editor3 round 達到 44/50 以上即可 ship。

---

## 附：關鍵工具一覽

```
tools/
├── extract_npc_strings.py     抽 CONVERSE.A 英文字串 → JSON
├── build_lookup_table.py      JSON → binary cht_strings.tab
├── fix_term_drift.py          名詞漂移批次修正
├── fix_at_duplicates.py       @EN（ZH）ZH 重字清除
├── bilingual_keywords.py      @keyword → @keyword（中文）
├── fix_bilingual_brackets.py  canonical map post-fix
├── fix_p0_editor_round1.py    editor1 P0 批次套用
├── fix_p0_editor3.py          editor3 P0 批次套用
├── extract_npc_keywords.py    198 NPC × keyword cheatsheet
├── check_en_match.py          en byte-exact 驗證（QA）
└── build-big5-font.py         Big5 點陣字型生成
```

---

## 附：參考文件

```
dumps/
├── glossary.json              420+ 條名詞對照表
├── style_guide.md             風格指南
├── distilled_sage_book.md     聖者之書 P1-50 精華
├── distilled_manual.md        遊戲手冊精華
├── sage_book_cross_ref.md     正典譯名決策紀錄
├── editor_in_chief_report.md  Round 1 P0 清單
├── editor2_report.md          Round 2 文學評分
├── editor3_report.md          Round 3（44/50）
├── tester_pass3_report.md     Pass 3（7/9 PASS）
└── tester_pass4_report.md     Pass 4（PASS with conditions）
```
