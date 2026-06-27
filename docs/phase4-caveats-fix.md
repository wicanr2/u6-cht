# B Phase 4 — 5 caveats audit & fix

> 2026-06-27 / branch `v2-16x16`. WORKLIST Phase 4 audit + fix Phase 3 留下的 5 個 caveat。

---

## 修法總覽

| # | Caveat | 修法 | 狀態 |
|---|---|---|---|
| 1 | 滑鼠 cursor 卡左上 | `Screen::get_mouse_location` 把 `Events::getMousePos()` (native pixel) 除以 `_displayScale` → game-space | ✅ 修了，**Iter 3 verified**：xdotool mousemove (240, 240) + screenshot 看到 cursor 白色箭頭 sprite 在 mouse 位置（`docs/screenshots/v2/cursor_follow_240_240.png`） |
| 2 | WOUFont::drawBig5CharToShape 12-row clip | **Iter 1**: revert 12-row；**Iter 2 後**: cutscene `*y += _line_h` 動態 14-px / 8-px → restore 16-row。再 caveat: cinematic dialog box 高度 fixed，Lua 4-chunk image_print (each wrap break) 累積 y = 8 + 4×14 = 64 px > box ~40 px → 長 chunk 仍 vertical overlap | ⚠ box height + Lua chunk 設計衝突，需動 cinematic source / Lua chunk timing。intro 短 chunk (1-2 行 fit) OK，長 chunk 留 v2.x |
| 3 | 對話換內容 overlay stale | `Screen::invalidateOverlayRegion` helper + `Screen::fill/clear/blit/blitbitmap` 進入時 mirror clear overlay 對應 region | ✅ 修了，chrome refresh 自動清舊 CJK，font path 重 draw 新 CJK |
| 4 | intro 字幕 16×16 audit | font getCharWidth Big5 byte (high bit) 統一 return 8（lead+trail=16 跟 advance 一致）→ wrap 算法不再 miscount | ✅ 修了 horizontal advance；vertical 受 cutscene `*y += 8` 限制（caveat 2 partial 同源） |
| 5 | conv_garg_font (魔像族) 未 load 16×16 atlas | `font_manager.cpp` 加 `((ConvFont *)conv_garg_font)->initBig5(big5_path)` | ✅ 修了，ScummVM log 出現「ConvGargFont: loaded big5_u6_16x16.fnt」|

---

## 主成果（throne room / 對話 / portrait header）

- **杜普雷 / 夏米諾 / 尤洛** — 16×16 真實解析度，朋友 finding 100% 解決
- **存檔已載入** — 16×16
- **anr2 / HP 數字** — ASCII 12px 仍同 v1.5.x
- 對話框換內容無 stale CJK 殘留（invalidate 機制）
- ConvGarg 魔像族對話路徑也升 16×16

screenshot: `docs/screenshots/v2/throne_room_16x16_native.png` (Phase 3)
+ `docs/screenshots/v2/throne_room_caveats_fixed.png` (Phase 4 post-fix)
+ `docs/screenshots/v2/intro_seg1_16x16_native.png` (intro 第 1 段)

## 剩餘的 v2.x patch 工作（不阻 v2.0 ship）

1. **cutscene 字幕 16×16 真實解析度** — 需改 `script_cutscene::print_text` `*y += 8` → 動態 line height (CJK 16 / ASCII 8)，或者 cutscene CJK 走 screen overlay 取代 shape composition
2. **WOUFont::drawBig5CharToShape 16-row** — 跟 1 同源，cutscene line spacing 修了才能展開
3. **cursor 在實機 (mouse event 進來時) 跟隨** — coordinate fix 邏輯對，需玩家驗

## 驗證 ScummVM log（baseline）

```
CHT: loaded 7298 entries + 189 fragments from cht_strings.tab (v3, hashed)
WOUFont(cutscene): loaded big5_u6_16x16.fnt — intro native 16×16 CJK enabled
ConvFont: loaded big5_u6_16x16.fnt — ConverseGump native 16×16 CJK enabled
ConvGargFont: loaded big5_u6_16x16.fnt — gargoyle convo native 16×16 CJK enabled
U6Font: loaded big5_u6_16x16.fnt — native 16×16 CJK enabled
```

5 條 CJK font path 全 active。

---

## 改的檔

scummvm-src/engines/ultima/nuvie/screen/screen.{h,cpp}:
- 加 `invalidateOverlayRegion(game_x, game_y, w, h)` helper
- 加 `Screen::fill / clear / blit / blitbitmap` 進入時 call invalidateOverlayRegion
- 加 `get_mouse_location` 除以 `_displayScale` 還原 game-space coord

scummvm-src/engines/ultima/nuvie/fonts/wou_font.cpp:
- `getCharWidth(c)`：Big5 byte (`c >= 0x80`) return 8
- `drawBig5CharToShape`：revert 回 12-row（避免 cutscene vertical overlap）

scummvm-src/engines/ultima/nuvie/fonts/conv_font.cpp:
- `getCharWidth(c)`：同上 Big5 byte return 8

scummvm-src/engines/ultima/nuvie/fonts/font_manager.cpp:
- conv_garg_font 加 `initBig5(big5_path)` + log

next: Phase 5 ship v2.0。
