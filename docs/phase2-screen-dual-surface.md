# B Phase 2 — Screen 雙 surface 架構

> 2026-06-27 / branch `v2-16x16`. 對照 `docs/WORKLIST.md` Phase 2.

---

## 設計

ScummVM Nuvie `Screen` 內部從單 surface 改成「3 surface」分工：

```
┌──────────────────────────────────────────────────────────┐
│  ScummVM 視窗 (e.g. 640×480, user 設)                    │
│  ↑ ScummVM 上層 1:1 顯示（不再 2× scale）                │
│ _rawSurface  : Graphics::Screen   (640×400 native)       │ ← 最終 output
│  ↑ Screen::performUpdate() — 2× nearest scale 上來        │
│ _gameSurface : Graphics::ManagedSurface (320×200)        │ ← game logic
│  ↑ 所有 Nuvie blit/fill/blitbitmap caller 透過           │
│ _renderSurface (RenderSurface wrapper over _gameSurface) │
└──────────────────────────────────────────────────────────┘

(Phase 3 加：_overlaySurface 640×400 alpha blend → _rawSurface 中段)
```

## 為什麼這設計

- **caller-facing API 不變** — Screen.width=320 / Screen.height=200 對外、所有現有 fill/blit caller 完全不動
- **native 解析度真實 640×400** — Phase 3 字寫 _rawSurface direct 拿 16×16 真實解析度（不被 down-scale）
- **ScummVM 上層 1:1** — 不再依賴 ScummVM scaler、Nuvie 內部完全掌控 pipeline
- **PC-98 1990 真實映射** — 與當年 NEC PC-9801 BIOS 機制完全等效

## 改動 surface

只動 2 個檔：

- `engines/ultima/nuvie/screen/screen.h` — 加 `_gameSurface`、`_overlaySurface`（Phase 3 用）、`_displayScale=2`
- `engines/ultima/nuvie/screen/screen.cpp`
  - constructor / destructor 初始化 / 釋放新 surface
  - `set_screen_mode()`：native_w/h = width × _displayScale；`initGraphics(640,400)`；new _rawSurface(640,400)；new _gameSurface(320,200)；`_renderSurface = CreateRenderSurface(_gameSurface)`
  - `performUpdate()`：2× nearest-neighbor scale _gameSurface → _rawSurface（16bpp 直寫 raw bytes，每 src pixel 寫 2×2 block）

caller code 一行不動。30+ blit/fill 路徑（anim_manager、map_window、chrome、msg_scroll ASCII…）透過 `_renderSurface->pixels` 寫，自然 redirect 到 _gameSurface。

## Phase 2.4 driver smoke test

兩階段：

**Smoke 1**：在 `_renderSurface->pixels` (10,10)-(60,60) 寫 50×50 紅 rect。
- 結果：throne room 截圖左上角清楚紅色方塊、約 100×100 px（驗 ScummVM 上層 2× scaler 正常）
- 收：`Screen::performUpdate` hook 點 + raw pixel write + ScummVM update mechanism 全 work

**Smoke 2**：Screen 雙 surface 完整實裝 + 紅 rect 移除。
- 結果：throne room 截圖跟 v1.5.1 完全一樣（chrome、map、黨員列表、對話框 100% 正常）
- 收：dual-surface + 2× internal scale + Nuvie pipeline 同等視覺
- ScummVM log: `Setting 640 x 480 -> 640 x 480 -- 1`（1× scaler，之前 v1.5.1 是 `-- 2`）
- 對外 caller 完全不需改

## 驗證 checklist

- [x] build OK（screen.h 改 private 觸發 ultima libultima.a 整 lib 重編，LINK 成功）
- [x] launch + load slot 2 → throne room 顯示
- [x] CHT load 正常：`CHT: loaded 7298 entries + 189 fragments`
- [x] 視覺 vs v1.5.1：chrome / map / 黨員 / 對話 / 字 全相同
- [x] 無 error / assert / crash
- [x] ScummVM scaler 從 2× → 1×（內部 framebuffer 已是 native res）

## 下一步：Phase 3

加 _overlaySurface 640×400 + Font path drawString 走 overlay direct，字 16×16 真實解析度。

預期 throne room「杜普雷」字會明顯比 v1.5.1 清楚（朋友 finding 解決）。
