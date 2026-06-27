# 16×16 漢字 feasibility — 仿 PC-98 1990 路線

> 起源：使用者 finding（2026-06-27）「PC-98 版 U6 把 16×16 漢字塞進去而且畫面跟現在一樣」。
> 核心觀念：**ScummVM 有 source 可改，重點是想法（能不能 fit + layout 怎麼樣），實作是手段**。

---

## 1. 事實（已查證 / 不憑記憶）

### 1.1 PC-98 版 U6（PonyCanyon 1991）

| 項 | 值 | 來源 |
|---|---|---|
| 解析度 | **640×400**（NEC 原生）| ultimacodex.com Computer_Ports_of_Ultima_VI |
| 16 色 palette | yes（EGA 改編，少於 DOS）| 同上 |
| 圖形重畫？ | **不重畫**，純 2× scale | 同上：「None of the graphics were redrawn and instead simply scaled up for the new resolution」 |
| 漢字 | 「**利用了 640×400 高解析度**」（≈ native 16×16 等效）| 同上 |
| 字型來源 | NEC PC-9801 BIOS 內建 JIS X 0208 16×16 漢字 ROM（標準）| PC-98 平台慣例 |
| 開發商 | Pony Canyon | mobygames |

**翻譯**：PC-98 1990 年就用了「**320×200 game asset 直接 2× scale 到 640×400 + 漢字用 native 16×16 畫在放大後 framebuffer**」這招。30 年後我們的 retro-cjk-hires-canvas rule 重新發現同樣 pattern。

### 1.2 我們現況（ScummVM Nuvie + u6-cht v1.5.x）

| 項 | 值 |
|---|---|
| ScummVM 視窗 | 640×480 |
| 內部 framebuffer | 320×200（U6 native）|
| Render 到視窗 | 2× pixel scale 到 640×400 + 80px 餘下 chrome |
| 漢字 atlas | **12×12**（WQY Sharp embedded bitmap）|
| 字實際視覺 dpi | 12px（atlas）× 2 scale = 24px 視窗顯示，但 detail 仍只 12px |
| 行高 stride | 12px |
| 主對話框 ≈ | 280×100 framebuffer pixel ≈ 23 字寬 × 8 行 |

### 1.3 為何 12px 字辨識率不佳

12px 解析度下複雜部首（木 / 丬 / 牜）共用 3-4 個 pixel 寬，**結構性不可分**。
今天驗證的「杜 vs 壯 vs 狀 vs 牡」就是這個。11px 反而更分明（row 多一條）但工程意義不大。

---

## 2. 兩條 idea 路線

### 路線 A：framebuffer 內 16×16（最小改動）

把字型 atlas 換 16×16，line stride 12 → 16，寫到原 320×200 framebuffer。

| 影響 | 變化 |
|---|---|
| 字 atlas | 24 bytes/glyph → **32 bytes/glyph**（rebuild 工具改 12 → 16）|
| 對話框可容 | 23 字寬 × 8 行 → **17 字寬 × 6 行**（容量降 ~40%）|
| 視窗看字 dpi | 24px（16 × 2 scale）— 視覺更大 |
| 字實際解析度 | 16px（清楚許多）|
| layout 改動 | 行高 hook、wrap 演算法、所有 U6Font/ConvFont/WOUFont 三條路徑都要對齊 |
| 工程量 | **中**（純字型 + stride，不動 ScummVM 框架）|
| 缺點 | 320×200 framebuffer 寫 16×16 字「比例違和」（原版字 8×8、現在塞 2× 大的）|

**白話**：跟 PC-98 不一樣（PC-98 字寫到 640×400 native）— 但**比現況 12×12 清楚很多**，工程最小。

### 路線 B：scaled stage 16×16 真實解析度（PC-98 等效）

字渲染推到 native 640×400 stage，game 邏輯仍 320×200 — **真正模仿 PC-98 1990 做法**。

| 影響 | 變化 |
|---|---|
| game asset | **不動**（320×200 framebuffer 維持原樣，pixel scaled）|
| 字 atlas | 16×16 |
| 字寫的 surface | **native 視窗 surface（640×400），不是 framebuffer** |
| 對話框可容 | 跟現況一樣（17-23 字寬 × 8 行，因為以視窗 pixel 計算）|
| 字實際 dpi | **16px** 真實解析度（不被 framebuffer 限制）|
| layout 改動 | 對話框 chrome 仍走 framebuffer pixel scale；字 overlay 在 chrome 之上、用 scaled 座標 |
| 工程量 | **大**（需 ScummVM OSystem API 給 native surface write、要切兩層 render pipeline）|
| 結果 | **跟 PC-98 1990 看起來一樣**：圖形 retro、字清楚 |

**白話**：完全照 PC-98 路線，但要動 ScummVM 框架。

### 路線 A vs B 取捨

| 維度 | A | B |
|---|---|---|
| 字清晰度 | 好（16px atlas）| **最好**（16px 真實解析度）|
| 對話容量 | 縮約 40% | **不變** |
| 工程量 | 中 | 大 |
| 違和感 | 略有（字比 game tile 大 2 倍）| 無 |
| 風險 | 對話 wrap 要重新 audit | ScummVM API 可能不允許 native overlay |
| v1.5.x scope | 可能塞得進 | v2.0 級重構 |

---

## 3. 還沒驗證的前提（要做 B 之前必須先確認）

- **P1**：ScummVM Nuvie 是否提供「在 native 視窗 surface 寫 pixel」的 API？
  - 看 `engines/ultima/nuvie/screen/screen.cpp` 跟 `OSystem::lockScreen()` 行為
  - 若不行，B 等同 fork ScummVM framework — 工程級暴漲
- **P2**：U6 對話 chrome（黃色花邊文字框）尺寸是寫死在 framebuffer 還是 scaled？
  - 若寫死 framebuffer pixel，B 的「字 scaled / chrome 不 scaled」會排版錯位
  - 修法：對話框 chrome 也要走 scaled overlay
- **P3**：cutscene / book viewer 字渲染走的是同一條路徑嗎？
  - WOUFont 是 cutscene-only，ConvFont 是 ConverseGump，U6Font 是 MsgScroll
  - 三條都要對齊到新 pipeline，工作量 × 3

---

## 4. 我的初步建議（給使用者拍板）

按「想法 vs 實作」的優先順序：

1. **先確認 idea 對不對**（P1-P3 read engine source 半天）— 不動實作
2. **若 A 可接受視覺違和**（17 字寬 × 6 行的對話框 OK）→ 走 A，v1.5.x 或 v1.6 ship
3. **若一定要 PC-98 看起來一樣**（容量不變、字清楚） → 走 B，當 v2.0 大重構，估 1-2 週工程
4. **若都太遠** → 接受 12×12 是 retro 限制，但在 README 加註「字型解析度限制，部分形近字（杜/壯/狀/牡）建議搭配上下文判讀」

**ROI 試算**：
- 路線 A：3-5 天工程，把 200+ NPC 譯文重 audit wrap、3 個 font hook 改 stride — 字清楚度大幅提升、玩家辨識率改善
- 路線 B：1-2 週工程（含 ScummVM 框架探查），完全 1:1 仿 PC-98 1990 體驗
- 不修：0 工程，已 ship v1.5.1 可用

要走哪條？

---

## 5. References

- [Computer ports of Ultima VI — Ultima Codex Wiki](https://wiki.ultimacodex.com/wiki/Computer_Ports_of_Ultima_VI)（PC-98 640×400 + 2× scale + Japanese leverages high resolution 出處）
- [Ultima VI: The False Prophet — Wikipedia](https://en.wikipedia.org/wiki/Ultima_VI:_The_False_Prophet)（背景）
- [MobyGames PC-98 screenshots gallery](https://www.mobygames.com/game/pc98/ultima-vi-the-false-prophet/screenshots/)（實機畫面，需開瀏覽器看；本機 WebFetch 403）
- [Hardcore Gaming 101 — NEC PC-98 vs Sharp X68000 vs FM TOWNS](https://hg101.proboards.com/thread/13641/nec-sharp-x68000-fujitsu-towns)（三平台對照）
- 我的 global rule `~/.claude/rules/81-retro-cjk-hires-canvas.md`（拉高內部畫布 / pixel scaling + native CJK 16×16 — 30 年後重新發現 PC-98 1990 同一做法）
