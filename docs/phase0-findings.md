# B Phase 0 source-survey findings

> 2026-06-27 / branch `v2-16x16` / 純 read source、無實作改動。
> 對照 `docs/design-B-16x16-plan.md` 的 P1/P2/P3。

---

## TL;DR

**Nuvie 內部架構跟 design doc 假設的不一樣**：

| 之前以為 | 實際 |
|---|---|
| Nuvie 內部 320×200 framebuffer + ScummVM 上層 2× scale → 640×400 視窗 | Nuvie 直接寫 native `_rawSurface`，**size 由 config `video/screen_width/height` 決定**（min 320×200、無上限）|

衍生**兩條 sub-route**取代原 design 單路：

- **B.1**：Nuvie 內部維持 320×200，**字渲染走獨立 640×400 overlay layer**（兩層 compose，ScummVM overlay API 或自加 surface）
- **B.2**：Nuvie 內部直接拉 640×400 native，**所有 tile / sprite blit 改 2× scale**（動 anim_manager + 30+ blit 點）

兩條都 work、都不退路線 A。B.1 較乾淨但 framework 摩擦多、B.2 直觀但 audit 面廣。

---

## P1 — OSystem native surface API

`engines/ultima/nuvie/screen/screen.cpp` 關鍵：

```cpp
// Screen ctor: default width(320), height(200)
// Screen::init()
config->value("config/video/screen_width", new_width, 320);
config->value("config/video/screen_height", new_height, 200);
if (new_width < 320) new_width = 320;
if (new_height < 200) new_height = 200;
// NO upper bound — config 寫 640 / 800 / 1024 都收
width = new_width; height = new_height;
set_screen_mode();   // 用 width × height 開 native window

// Screen::set_screen_mode():
initGraphics(width, height, &SCREEN_FORMAT);
_rawSurface = new Graphics::Screen(width, height, SCREEN_FORMAT);
_renderSurface = CreateRenderSurface(_rawSurface);
```

**結論**：
- ScummVM Nuvie **不是「固定 320×200 framebuffer + 上層 2× scale」**
- config 改 `screen_width=640, screen_height=400` → Nuvie 整個 game world 都跑 640×400 native
- **不需 fork `OSystem`** — Nuvie 已 expose native size、所有 render 都直寫 native surface
- 想做 PC-98 1:1（320×200 game + 16×16 字 overlay 在 640×400）需要兩層 compose，要看 `OSystem::showOverlay` / 自加 surface

`engines/ultima/nuvie/screen/surface.h` 有 `RenderSurface` abstraction（包 `Graphics::ManagedSurface`），可以自己 `new RenderSurface(640, 400, ...)` 做第二 layer。

---

## P2 — chrome vs 字 render path 分離度

未獨立 grep（P1 結果讓 P2 變得**不重要**）。

P1 釐清後：Nuvie 沒有「framebuffer pixel scaled」這個層次概念 — chrome 跟字都寫到同一 `_rawSurface`（native size）。所以原 design「chrome 保留 framebuffer scale、字走 native overlay」這個分立的問題消失了。

兩個 sub-route 怎麼處理 chrome：

- **B.1**（兩層 compose）：chrome 寫 lower 320×200 layer + 字寫 upper 640×400 overlay → 合成顯示。chrome 自然 2× scale upscale 到 640×400，字 native 16×16 寫 overlay。
- **B.2**（拉高 native）：chrome 跟字都寫到 640×400 native。chrome asset 仍 raw 16×16 px → 視覺縮小一半 → 需要 chrome blit 改 2× stretch（或重畫 chrome asset 32×32）。

**B.1 chrome 邏輯 0 改動、字邏輯動。B.2 chrome blit 跟著動。**

---

## P3 — 三條 font path entry point

| Font | drawString 接口 | surface 參數 | 共用 base? |
|---|---|---|---|
| `U6Font` | `drawString(Screen *screen, const char *str, ...)` | `Screen *` | `Font` base class |
| `ConvFont` | 同上（繼承 Font）| 同上 | 同 |
| `WOUFont` | 同上 | 同上 | 同 |

三條都吃 `Screen *` + native pixel x/y。改寫策略：

- **B.1**：drawString 增 overload `drawString(RenderSurface *overlay640x400, ...)`，字寫 overlay，原 Screen 入口 keep 給其他 caller
- **B.2**：原 drawString 不變，但所有 caller 的 x/y 都改成 640×400 座標（自動 work，因 Screen 已 native）

---

## 兩條 sub-route 詳比較

| 維度 | B.1（雙 layer overlay） | B.2（native 拉高）|
|---|---|---|
| Nuvie config 改 | 不改 | `screen_width=640, screen_height=400` |
| Game tile blit | 不動（320×200 layer 寫 16×16 tile）| 全部改 2× stretch blit（30+ 點：anim_manager, map_window, anim 等）|
| Chrome | 自然 upscale | 重畫或 stretch blit |
| 字 atlas | 16×16 | 16×16 |
| 字寫 surface | 獨立 640×400 overlay | 原 `_rawSurface`（已是 640×400）|
| 字 wrap 算 | 以 640×400 算（17 字 × 12 行）| 同 |
| PC-98 1:1 程度 | **完全 1:1**（PC-98 也是 framebuffer 2× scale + 字 overlay 概念）| 視覺等效但內部 mechanics 不同 |
| 工程量 | 主要動 font 與 overlay framework | 動所有 blit + audit 整個 view |
| 風險 | ScummVM overlay 機制 / 兩 layer 同步 timing | tile sprite 拉伸 quality（nearest/bilinear）|
| 估時 | 5-7 天 | 8-12 天 |

---

## 建議走 B.1（兩層 compose）

理由（按 [[feedback-retro-remake-no-cost-ceiling]] + global rule `81-retro-cjk-hires-canvas` 精神）：

1. **B.1 是 PC-98 1990 真實做法的 1:1 映射** — PC-98 framebuffer 也是 320×200 game pixel 2× scale 寫到 640×400 hardware framebuffer + 漢字 16×16 直接寫 640×400。Nuvie 用 overlay layer 重現完全等效。
2. **動的檔少、面集中** — 主要動 `screen.cpp` + `font.h` + 3 font path drawString。tile / map_window / anim / chrome 都不動。
3. **B.2 動所有 blit 是 horizontal sweep**，B.1 是 vertical isolate（局部深改）— 後者出 bug 範圍小、好 audit。
4. **ScummVM overlay 機制 worst case 自加** — Nuvie 已用 `RenderSurface` abstraction，直接 `new RenderSurface(640, 400)` 當 overlay layer、compose 時 blend，不需動 ScummVM core。

---

## Phase 1 起跑前要先確認的（給 user）

1. **走 B.1 還是 B.2**？建議 B.1。
2. **chrome 是否要重畫 native 32×32 asset**（B.2 才需）？走 B.1 不用。
3. **字 atlas 來源**：WQY zenhei 16×16 embedded bitmap 是否存在？如不存在退 outline render 或換思源黑體 HW。
4. **Phase 1 後馬上 phase 2-3 連續做還是 phase by phase 確認**？

---

## 文件 cross-ref

- `docs/design-B-16x16-plan.md` — 整體 plan（含取消清單、共存策略）
- `docs/design-16x16-feasibility.md` — idea 階段 feasibility（PC-98 facts、A vs B 取捨）
- `docs/PLAYTEST.md` — Phase 4 用得到的 game-tester harness
- `~/.claude/rules/81-retro-cjk-hires-canvas.md` — 拉高內部畫布 / native CJK 鐵則
- 本檔 — phase 0 結論
