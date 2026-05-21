# Ultima VI 繁體中文化 v1.1

**Release date**: 2026-05-21
**Tag**: v1.1
**Git commit**: 2147f85

## 重點

v1.1 在 v1.0 基礎上做大量品質修正與引擎打磨：

### Engine 改進
- **Cursor Y stride bug fix** — designer agent 找出 v1.0 起 cursor_y `* 8` 但 drawLine `* 10` 的不對齊，導致 ↓ 分頁提示與 ankh 游標蓋住末字（off-by-2px per line × 10 行 = 20px 累積）
- **Portrait header 中文化** — 4 條 codepath 全 hook：`不列顛王 / 法師 / 尤洛 / 杜普雷`
- **Party panel 中文化** — 右側黨員列表顯示中文姓名
- **Look/Search 路徑 fragment substitution** — 「汝見階梯」「汝見一隻老鼠」等 Lua 動態組合字串走 fragment 補譯
- **「夠不著」→「搆不著」** — engine 內 hardcoded Big5 bytes typo 修正
- **Multi-paragraph split** — NPC 多段對話分段 lookup 解決 add_text greedy 累積問題

### Translation 改進（基於兩輪 editor agent + tester pass3）
- **Codex 守則之書 → 知識寶典** — 採納聖者之書 1992 權威譯（39 處 / 15 files）
- **25+ `@EN（ZH）ZH` 重字 bug 清除** — bilingual scan 後殘留的譯者重複註解
  - `@gargoyles（魔像族）族` → `@gargoyles（魔像族）`
  - `@Mantra（真言）真言` → `@Mantra（真言）`
  - `@Shrine（聖壇）聖壇` → `@Shrine（聖壇）`
  - `@Hubert（胡伯）胡伯` → `@Hubert（胡伯）`
- **「不列顛王顛王」/「貓人之貓人」/「魔像族族」** 等 12 個 NPC 重字 P0 修
- **Valor 英勇 → 勇敢** — 避免與 Courage 勇氣 撞名
- **Singularity 200 quest hint 括號錯位** — 「@Catacombs（控制）@Control（熱情）」改正
- **Reaper 死神 → 樹妖** — 聖者之書 p76 圖鑑確認
- **大烏賊** 統一（遊戲手冊 + 聖者之書 一致）
- **Dupre 「甲甲」→ 甲冑** typo
- **Chuckles quest hint** 兩 keyword 括號互換修正

### Tooling
- `tools/fix_at_duplicates.py` — 自動掃除 @EN（ZH）ZH 重字
- `tools/fix_p0_editor_round1.py` — 第一輪 P0 批次修
- `tools/fix_bilingual_brackets.py` — bilingual scan 後 canonical map post-fix
- `tools/bilingual_keywords.py` — @中文 → @english（中文）轉換
- `tools/extract_npc_keywords.py` — 198 NPC × 407 keyword 速查表

### Documentation
- `skills/u6-cht.md` — 主專案 onboarding skill
- `skills/u6-game-tester.md` — in-game testing playbook
- `dumps/editor_in_chief_report.md` — 第一輪 editor 報告
- `dumps/editor2_report.md` — 第二輪 editor 報告
- `dumps/dialog_redesign.md` — designer agent UI 設計三方案
- `dumps/distilled_sage_book.md` — 聖者之書 1992 P1-50 精華
- `dumps/distilled_manual.md` — 遊戲手冊 13 頁精華
- `dumps/sage_book_cross_ref.md` — cross-ref 決策文件
- `dumps/tester_pass3_report.md` — 實機驗證 7/9 PASS

### Screenshots（更新）
新 8 張 in-game 截圖取代 v1.0 11 張舊圖：
- Look 地板 / 牆 / 地毯
- 戰鬥訊息（魔像 輕度/重度受傷, 命危！）
- 攻擊 + 對話-無對象
- LB Quiz 答對（汝答正確 + 中文 reward）
- LB Dialog 中文化全圖

## Tester pass 3 結果

| Fix | Result | Notes |
|---|---|---|
| Codex 知識寶典 | NOT-REACHED | 需到 Caretaker NPC（路徑遠）|
| Bilingual @keyword | ✅ PASS | `healing（醫療）/ 不列顛王 / 法師` |
| 戰鬥 fragment | ✅ PASS | `搆不著！/ 杜普雷擦傷` |
| Look 路徑 | ✅ PASS | 地板/地毯/牆 |
| 存檔已載入 | ✅ PASS | 3 次 reload 均出現 |
| 對話-無對象！| ✅ PASS | 截圖確認 |
| 字型 11px UMing | 視覺確認 ✅ | log 顯示 12x12 為檔名相容性 |
| Multi-paragraph | ✅ PASS | 0 ctl byte 錯誤 |
| Quiz `(答案: keyword)` | ✅ PASS | 「汝答正確。/ 請查閱汝之典籍。」|

## Downloads（手動上傳到 GitHub Release）

由於 push 環境無 GitHub auth，binary 存在本機 `releases/` 待手動 attach：

- `u6cht-1.1-linux-x86_64.AppImage` (123 MB) — Linux 64-bit 全 bundled
- `u6cht-1.1-windows-x86.7z` (91 MB) — Windows 32-bit mingw build

### 使用

**Linux**：
```bash
chmod +x u6cht-1.1-linux-x86_64.AppImage
./u6cht-1.1-linux-x86_64.AppImage <Ultima-VI-game-dir>
```

**Windows**：
解 7-zip 後，拖原版遊戲資料夾到 `run.bat` 即可。

**自備 Ultima VI 原版檔案**（CONVERSE.A、BOOK.DAT 等），本 release 不含原版資料。

## Stats

- 199 NPC + BOOK.DAT 翻完
- 7298 hashed exact entries + ~80 plain fragments
- 兩輪 editor 審稿（共 40+ P0/P1 修正）
- 三輪 tester 實機驗證
- 一輪 designer 提交 UX redesign 三方案

## Known Issues

- LB greeting 「the noble ruler of Britannia」 後續句 偶有 fragment miss（已加 fragment）
- Cursor 在 input mode 偶與末字重疊（已修 cursor_y）
- 開頭 cinematic 動畫 未翻譯（task #66 待做）
- `?` / `help` magic command 未實作（task #57 deferred）

## Roadmap v1.2

- 開頭 cinematic 翻譯
- Help command in-game (`?` / `help` → 顯示當前 NPC 全 keyword 列表)
- Dialog UI redesign Plan 2（stride 12px、panel 128px）— designer 推薦方案
- 補齊 8 職業 + 26 魔法音節 + 8 施法材料 glossary entries

## Credits

- Owner: wicanr2 (Chun-Yu Wang) <wicanr2@gmail.com>
- Engine: ScummVM Nuvie GPL contributors
- Translation: assisted by Sonnet / Opus 多輪 agent + editor reviewer
- Font: AR PL UMing (Apache 2.0)
- Reference: 創世紀聖者之書特別版 1992 (電腦玩家雜誌, 蘇炫榮 / 高文麟編)
- Reference: Ultima VI 遊戲手冊（中文版說明書）

## License

- Engine patches: GPL v3+
- Translation data: CC BY-SA 4.0
- Font: Apache 2.0
- Tools: MIT
- Documentation: CC BY 4.0
