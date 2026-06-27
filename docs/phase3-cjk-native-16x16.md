# B Phase 3 — CJK 16×16 真實解析度（overlay surface 路徑）

> 2026-06-27 / branch `v2-16x16`. 對照 `docs/WORKLIST.md` Phase 3。
> 截圖證明：`docs/screenshots/v2/throne_room_16x16_native.png`

---

## 結果

throne room 黨員列表 v1.5.1 → v2.0：

| 字 | v1.5.1 (12×12) | v2.0 (16×16 native) |
|---|---|---|
| 杜普雷 | 「杜」row 3 `█████··█` 像「壯」row 6 結構，朋友誤認 | 「杜」row 6-9「木」中豎+橫貫+撇捺三段分明 |
| 夏米諾 | 筆畫被擠 | 銳利 |
| 尤洛 | 筆畫被擠 | 銳利 |
| 存檔已載入 | 中等 | 16px 真實解析度 |

**朋友 finding 100% 解決**。

---

## 走的設計（queue → persistent overlay）

第一次嘗試用 **CJK render queue**：font path queue glyph，performUpdate render 完 clear queue。

**Bug**：caller (msg_scroll / ConverseGump) dirty-only paint pattern — debug log 顯示 frame 0 push 21 個 CJK、frame 1+ queue 空。每 frame `performUpdate` scale `_gameSurface` overwrite 整個 `_rawSurface`，queue 空時 CJK 區域被 game background 覆蓋 → CJK 第 1 frame 後消失。

**Fix**：queue → **persistent `_overlaySurface` (640×400)**：

```
        ┌─ caller (msg_scroll) drawString(CJK)
        │
        ▼
font path drawBig5Char
        │
        ▼
Screen::queueCJKGlyph(game_x, game_y, glyph[32], color_index)
        │
        └──> 寫 _overlaySurface (game_x*2, game_y*2) 直接 paint
              (transparent key 0x0000 跳過，黑字 nudge 0x0001)

每 frame Screen::performUpdate():
  1. 2× scale _gameSurface → _rawSurface  (overwrites)
  2. compose _overlaySurface → _rawSurface  (skip 0x0000 transparent)
  3. _rawSurface->update()
```

關鍵差別：`_overlaySurface` pixel **persistent across frame**，CJK 寫一次後留著，每 frame compose 重新蓋到 _rawSurface 上面。

## 改動 surface

- `scummvm-src/engines/ultima/nuvie/screen/screen.h`：`_cjkQueue` 移除 → `_overlaySurface` 改 init
- `scummvm-src/engines/ultima/nuvie/screen/screen.cpp`：
  - `set_screen_mode`：alloc `_overlaySurface` (640×400) + transparent fill
  - `queueCJKGlyph`：直寫 _overlaySurface (16×16 1bpp → native pixel)，名稱保留避免 font path 改名
  - `performUpdate`：scale `_gameSurface` → compose `_overlaySurface` → update
- `scummvm-src/engines/ultima/nuvie/fonts/u6_font.cpp`：BIG5_GLYPH_BYTES 24→32 + drawBig5Char → queueCJKGlyph
- `scummvm-src/engines/ultima/nuvie/fonts/conv_font.cpp`：同上 (CFB5_GLYPH_BYTES + advance 14→16)
- `scummvm-src/engines/ultima/nuvie/fonts/wou_font.cpp`：同上 (WB5_GLYPH_BYTES + drawBig5Char only，drawBig5CharToShape 暫不動)
- `scummvm-src/engines/ultima/nuvie/fonts/font_manager.cpp`：big5_u6_12x12.fnt → big5_u6_16x16.fnt（U6Font + ConvFont）
- `scummvm-src/engines/ultima/nuvie/script/script_cutscene.cpp`：同上 (WOUFont cutscene)
- `working/game/big5_u6_16x16.fnt`：placed (472KB, gitignored)

## ScummVM log baseline (Phase 3)

```
CHT: loaded 7298 entries + 189 fragments from cht_strings.tab (v3, hashed)
WOUFont(cutscene): loaded big5_u6_16x16.fnt — intro native 16×16 CJK enabled
ConvFont: loaded big5_u6_16x16.fnt — ConverseGump native 16×16 CJK enabled
U6Font: loaded big5_u6_16x16.fnt — native 16×16 CJK enabled
```

## 已知 caveat（待 Phase 4 audit）

1. **滑鼠 cursor 卡在左上角 (0,0)** — 截圖看見 cursor sprite 不跟滑鼠移動，可能 cursor render path 沒走 _gameSurface、寫 _rawSurface direct 被 scale overwrite。需 audit `cursor.cpp`。
2. **WOUFont::drawBig5CharToShape 仍 12-row iteration** — cutscene 中 shape-internal CJK（如 intro 字幕在 background shape 中渲染）字下半 4 row 被砍。改寫需 shape 16×16 area，留 Phase 4 處理。
3. **對話換內容時 overlay stale**：若 caller dirty-only 不重 paint CJK，舊 CJK 在 _overlaySurface 殘留。要嘛 (a) 加 Screen::invalidateOverlay region（caller 寫 _gameSurface chrome 時同步 clear overlay），(b) 改 caller 每對話 always full redraw。Phase 4 跑 game-tester 確認哪些路徑會踩到。
4. **intro cinematic 還沒驗** — 用 PLAYTEST.md harness 跑 intro 看 7 段中文是否全 16×16 顯示。
5. **conv_garg_font (魔像族字型) 未 load 16×16** — font_manager.cpp 中 `conv_garg_font` 沒 call initBig5。Phase 4 驗有需要再加。

## Reference

- `docs/phase2-screen-dual-surface.md` — Screen 雙 surface 架構（Phase 2）
- `docs/phase1-font-survey.md` — WQY Sharp 16×16 字型 atlas
- `docs/screenshots/v2/throne_room_16x16_native.png` — 截圖證據
