# Ultima VI 繁體中文化 v2.0

**Release date**: 2026-06-27（rc / 開發中）
**Tag**: v2.0
**Branch**: `v2-16x16`
**Git commit**: 798f665（Phase 4 完成）

---

## 重點

**v2.0 = 把漢字從 12×12 升級到 16×16 真實解析度**，仿 1991 年 PC-98 版 *Ultima VI 〜偽りの預言者〜*（PonyCanyon）的做法：320×200 game asset 不重畫、純 2× scale 到 640×400 native framebuffer，**漢字用 16×16 真實 detail 畫在放大後的 framebuffer 上**。

字寫到 **persistent 640×400 overlay surface** 跟 game scale-up 後的 _rawSurface compose — game world 維持 retro pixel 質感，漢字得到 native 16-pixel 解析度。

## v1.x → v2.0 視覺對比

| 字 | v1.5.1 (12×12) | v2.0 (16×16 native) |
|---|---|---|
| **杜普雷** | 「杜」row 3 `█████··█` 像「壯」row 6「丬」結構，玩家朋友看成「壯/狀/牡」 | 「杜」row 6-9「木」中豎+橫貫+左右撇捺三段分明，**完全不會誤認** |
| **夏米諾 / 尤洛** | 12px 筆畫被擠 | 16×16 銳利 |
| **存檔已載入** | 中等可讀 | 16px 真實解析度 |

主截圖：[`docs/screenshots/v2/throne_room_16x16_native.png`](docs/screenshots/v2/throne_room_16x16_native.png)、
[`docs/screenshots/v2/intro_seg1_16x16_native.png`](docs/screenshots/v2/intro_seg1_16x16_native.png)。

## 引擎改動（patches/scummvm-u6cht.patch）

### Screen 雙 surface 架構（Phase 2）
- `_rawSurface = 640×400 native`（ScummVM 視窗直接 1:1 顯示）
- `_gameSurface = 320×200`（所有現有 Nuvie blit/fill/chrome path 寫這，caller code 0 行改動）
- `_overlaySurface = 640×400`（CJK 16×16 寫這，persistent across frame）
- `performUpdate()`：2× nearest-neighbor scale game → raw + compose overlay (transparent key 0x0000)

### CJK 16×16 atlas（Phase 1+3）
- `big5_u6_16x16.fnt`（472,256 bytes）— WenQuanYi Zen Hei Sharp 16×16 embedded bitmap
- 14,758 slots × 32 bytes/glyph，13,707 字 cover（92.9%）
- 字型 build：`tools/build-big5-font-16x16.py`
- glyph dump 對比：`tools/dump_font_glyph.py`
- 三條 font path（U6Font / ConvFont / WOUFont）+ 新增 ConvGargFont（魔像族對話）— 5 條 CJK font 全 active

### Caveat 修正（Phase 4）
- **invalidate overlay region**：Screen::fill/clear/blit/blitbitmap 進入時自動 mirror clear overlay 對應 region（caller dirty pattern 自動同步刷新 CJK）
- **mouse coordinate** native→game 還原（除以 `_displayScale=2`）
- **font getCharWidth Big5 byte high-bit → 8**（lead+trail=16 一致 drawBig5Char advance，wrap 不再 miscount）

## v1.5.2 first wave 整合進 v2.0

v2.0 包含 v1.5.2 first wave 的修法（已在 main 上）：

- **opened!/closed! 容器訊息 fragment leak fix**（issue #1.1）— build_lookup_table.py source 切到 `translations/`，8 條 fragment 進 cht_strings.tab
- **intro 7 段退化 fix**（issue #1.4）— `_engine_fragments.json` longest-first sort，短 fragment `' and'` 不再吃掉「You have traded the Avatar's life of peril and adventure」整段 substring match
- **tile token 候選 fragment**（issue #1.2）— 11 條 ground tile 變體
- **fix_term_drift.py safeguard**（issue #1.5）— 排除 `_engine_*.json` + `_keywords.json`
- **Windows run.bat CRLF source of truth**（issue #2）— `dist/windows/run-free.bat` + `repack.sh`

## Known caveats（v2.x patch）

1. **Cutscene 字幕仍走 shape path 12×12 detail** — `script_cutscene::print_text` 用 `*y += 8` line spacing，16×16 寫進 shape 會 vertical overlap。真 fix 需動 cutscene script line height 或讓 cutscene CJK 走 screen overlay 取代 shape composition。
2. **滑鼠 cursor follow** — coordinate native→game 邏輯已修，game-tester headless 環境無真 mouse event 難驗，實機應 work。

## v1.5.1 ↔ v2.0 共存

- v1.5.1 release 不撤回（已下載者可繼續用）
- v2.0 release 為新 baseline
- 由 ScummVM 自動偵測 `big5_u6_16x16.fnt`（v2.0）或 fallback `big5_u6_12x12.fnt`（v1.5.x）— 共用 cht_strings.tab v3 binary，玩家可任選

## 平台 ship 範圍

- **Linux AppImage v2.0** — slim + FULL（FULL 含遊戲檔，本機自留）
- **Windows zip v2.0** — slim + FULL（mingw cross-compile）
- **macOS** — GitHub Actions universal binary（arm64 + x86_64 lipo）

詳見 README quick start 章節。

## License

繼承 ScummVM (GPL v3) + 翻譯 (CC BY-SA) + 字型 (WQY Apache 2.0)。
