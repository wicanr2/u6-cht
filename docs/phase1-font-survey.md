# B Phase 1 — 16×16 字型 atlas findings

> 2026-06-27 / branch `v2-16x16`. 對照 `docs/WORKLIST.md` Phase 1 checklist 1.1-1.5。

---

## 1.1 字型選定：WenQuanYi Zen Hei Sharp（16×16 embedded）

`python3-freetype` 列出 4 個系統字型 embedded bitmap：

| 字型 | face_idx | embedded sizes |
|---|---|---|
| WenQuanYi Zen Hei Regular | 0 | （outline only）|
| WenQuanYi Zen Hei Mono | 1 | （outline only）|
| **WenQuanYi Zen Hei Sharp** | **2** | **12 / 13 / 14 / 15 / 16** |
| AR PL UMing (CN/HK/TW/TW MBE) | 0-3 | 11 / 12 / 13 / 14 / 15 / 16 |
| Noto Sans CJK Bold (JP/KR/SC/TC) | 0-3 | (outline only) |
| Noto Serif CJK Bold (JP/KR/SC/TC) | 0-3 | (outline only) |

**選 WQY Sharp 16×16**：跟 v1.x 用的 12×12 同字型家族，視覺風格一致、字符 coverage 同源、玩家無斷層感。

退選：AR PL UMing TW 16×16（4 variant 都可選，若 WQY 某字 fallback 失敗可備用）。

## 1.2-1.3 build pipeline

- `tools/build-big5-font-16x16.py` 仿 `build-big5-font-wqysharp.py`，layout 12×12 → 16×16
- glyph 24 → **32 bytes**（16 rows × 2 bytes/row, 16 bits MSB-first, no padding）
- linear index 算法不變（94 × 157 = 14758 slots）
- 輸出：`dumps/big5_u6_16x16.fnt`，**472,256 bytes**（跟預估完全一致）

baseline 校正：WQY Sharp 16px ascent ~13，`bitmap_top` 13 → row_offset 0；其餘字 row_offset 動態計算。

## 1.4-1.5 朋友 finding 驗證：「杜壯狀牡」12×12 vs 16×16

朋友 2026-06-27 回報 v1.5.1 玩 throne room 看到「杜普雷」分不清是杜 / 壯 / 狀 / 牡。

12×12 (current v1.5.1) — **結構撞針**：

```
杜 row 3-4:  █████··█    壯 row 6:  ████···█    狀 row 6:  ████··█·    牡 row 5:  ··██···█
              ·██·██████              ·█·█···█              ·█·█··█·              ███····█
```

**杜的「木」row 3 `█████`** 在 12px 解析度下變 5 px 連續橫筆，**視覺類似「丬」三筆 + 橫**。row 4 木的撇捺被擠成 `·██·██████`，跟右半「土」連起來。

16×16 (v2.0) — **結構分明**：

```
杜 row 4-10:
  ··██··█████████    ← 「木」橫筆貫穿
  ··███·····█·····    ← 木的左豎 + 撇起點
  ·█·█·█····█·····    ← 木的左撇 + 中豎 + 右捺
  ·█·█·█····█·····    ← 同上延伸
  █··█······█·····    ← 撇捺分開到底

壯 row 6-13:
  ·····██████████    ← 「士」上橫
  ·····█····█·····
  ██████····█·····    ← 「士」中橫 + 「丬」第三筆
  ··█··█····█·····    ← 「丬」三筆 + 「士」中豎
  （重複到 row 13）
  ·█···█·███████    ← 「士」底橫

狀 row 1-4:
  ·····█····█·····
  ··█··█····█·█···    ← 「犬」的點 row 2 出現
  ··█··█····█··█··    ← 「犬」右下捺
  ··█··█····█··█··

牡 row 7-9:
  █···█··███████    ← 「土」上橫
  ····█·····█·····    
  ····███···█·····    ← 「土」中橫 + 「牜」豎
```

**結論**：16×16 杜的「木」（中豎 + 橫貫 + 左右撇捺）跟壯/狀的「丬」（三筆平行垂直）視覺完全不同。**朋友 finding 100% 被 16×16 解決**。

## Phase 1 完成 — 進 Phase 2

- ✅ 字型 atlas 工程 OK
- ✅ 朋友 finding decision gate 通過
- 472KB 字型檔 .gitignored（dumps/ 內），工具 + finding md 入 commit
- 下一步：Phase 2 overlay layer + chrome 處理

## Reference

- `docs/WORKLIST.md` § Phase 1
- `tools/build-big5-font-16x16.py`
- `tools/dump_font_glyph.py`
- `dumps/big5_u6_16x16.fnt`（gitignored binary）
