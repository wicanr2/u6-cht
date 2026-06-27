# v2.0 Worklist — B.1（兩層 compose、PC-98 1:1 漢字 16×16）

> Branch: `v2-16x16`。design doc: `docs/design-B-16x16-plan.md`。Phase 0 findings: `docs/phase0-findings.md`。
> 規則：第一性原理拆解、老遊戲重製不考慮成本、不退方案 A。

---

## Phase 0 — source survey ✅

- [x] P1 OSystem native surface API：Nuvie 直接寫 native `_rawSurface`、size = config `video/screen_{width,height}`、無上限。`RenderSurface` abstraction 可加 overlay layer，不需動 ScummVM core。
- [x] P2 chrome vs 字 render path：P1 結果讓 P2 變不重要 — 兩層 compose 自然分離。
- [x] P3 三條 font path：`U6Font` / `ConvFont` / `WOUFont` 都繼承 `Font` base、`drawString(Screen*, ...)`。B.1 加 overlay 重載即可。

→ 結論：B.1 可行、5-7 天估時。

---

## Phase 1 — 16×16 字型 atlas build pipeline

- [ ] **1.1 確認 WQY zenhei 16×16 embedded bitmap 是否存在**
  - 用 `freetype` 查 `wqy-zenhei.ttc` `face.available_sizes`
  - 若不存在：退 outline render 16px，或換思源黑體 / Source Han Sans HW / Noto Sans CJK
  - 輸出：`docs/phase1-font-survey.md` 紀錄選擇與 atlas size
- [ ] **1.2 寫 `tools/build-big5-font-16x16.py`**
  - 仿 `tools/build-big5-font-wqysharp.py`：layout 12×12 → 16×16
  - glyph 24 bytes → **32 bytes**（16 rows × 2 bytes/row, 16 bits + 0 padding）
  - linear index 算法不變（94 × 157 = 14758 slots）
  - 總大小 = 14758 × 32 = **472,256 bytes**
- [ ] **1.3 build `dumps/big5_u6_16x16.fnt`**
- [ ] **1.4 寫 `tools/dump_font_glyph.py`** — 給 codepoint 印 ASCII art glyph（12×12 vs 16×16 對比）
- [ ] **1.5 prove 朋友 finding 修掉**：dump「杜壯狀牡」16×16 vs 12×12 並排，**16×16 必須結構分明不混淆**
  - 若失敗：考慮 (a) 換字型、(b) 試 hint tweak
- [ ] **1.6 commit Phase 1 工具與輸出**（字型 atlas .fnt 本身是 binary、依 .gitignore 不入；工具入）

**Decision gate**：1.5 通過才進 Phase 2。

---

## Phase 2 — overlay layer 與 chrome 處理

- [ ] **2.1 grep ScummVM `RenderSurface` + `Graphics::ManagedSurface` API** — 確認可獨立 `new RenderSurface(640, 400, ...)` 而不影響主 `_rawSurface`
- [ ] **2.2 改 `engines/ultima/nuvie/screen/screen.cpp`**
  - 加 `RenderSurface *_overlaySurface` (640×400)
  - 加 `Screen::getOverlay()` 與 `Screen::composeOverlay()` API
  - `composeOverlay`: 用 alpha blend 把 overlay 寫回 `_rawSurface`（最後 present 前）
- [ ] **2.3 改 `Screen::performUpdate`** — present 前 call composeOverlay
- [ ] **2.4 driver smoke test**：launch scummvm + 在 overlay 寫一塊紅色 rectangle，看 native window 是否上下 layer compose 出來
- [ ] **2.5 commit Phase 2**

**Decision gate**：2.4 看到 overlay 跟 game world 同時顯示、不互蓋、不錯位。

---

## Phase 3 — 三條 font path 改寫 overlay

- [ ] **3.1 `Font` base class：加 overlay-aware drawString 重載**
  - `engines/ultima/nuvie/fonts/font.h` / `.cpp`
  - 新接口：`drawStringOverlay(RenderSurface *overlay640, const char *str, uint16 x, uint16 y, ...)`
  - 原接口 keep（給 ASCII 路徑用）
- [ ] **3.2 U6Font 16×16 載入**
  - `u6_font.cpp`：載 `big5_u6_16x16.fnt`
  - 改 CJK 渲染走 `drawStringOverlay`（座標轉 ASCII px → overlay 2× px）
  - ASCII 仍走原 12px 路徑寫 `_rawSurface`
- [ ] **3.3 ConvFont 16×16 載入**
  - `conv_font.cpp`：同上
  - NewUI ConverseGump 用：text x/y 從 320×200 座標 × 2 → 640×400 overlay
- [ ] **3.4 WOUFont 16×16 載入**
  - `wou_font.cpp`：同上
  - cutscene 字幕 wrap 改 native px
- [ ] **3.5 CHT hook 點不動** — cht_strings.tab v3 lookup 仍走 `CHTranslate::translate()`、回 Big5 bytes、由 font path 渲染
- [ ] **3.6 漏翻 SOP 驗證** — 既有 8 個 hook 點打 `CHT-LOOK` debug 仍正常
- [ ] **3.7 commit Phase 3**

**Decision gate**：3.7 後啟動 ScummVM 看 throne room — 黨員列表「杜普雷」字明顯比 v1.5.1 清楚、不誤認。

---

## Phase 4 — layout audit + visual diff

- [ ] **4.1 跑 PLAYTEST.md game-tester harness**
  - throne room：黨員列表、Look LB、Use 箱子、對話 LB
  - intro 7 段截圖
  - combat 跑一場（cheat 觸發 gargoyle 或走野外）
- [ ] **4.2 視覺對比 v1.5.1 vs v2.0** — 24 張關鍵截圖並排
  - 朋友 finding：「杜普雷」三字必須 visually distinguishable
- [ ] **4.3 layout issue 收集**：wrap 異常、chrome 字錯位、cutscene fit
- [ ] **4.4 layout fix iteration**（如有問題）
- [ ] **4.5 update `docs/PLAYTEST.md`** — v2.0 截圖時機、新 layout 像素數
- [ ] **4.6 commit Phase 4**

---

## Phase 5 — ship v2.0

- [ ] **5.1 重 build patched ScummVM**（Linux native + Windows mingw cross）
- [ ] **5.2 Linux AppImage v2.0**（slim + FULL，依 `retro-game-cht-package` skill）
- [ ] **5.3 Windows zip v2.0**（slim + FULL）
  - 沿用 `dist/windows/run-free.bat` / `run-full.bat` CRLF source
  - 帶 `big5_u6_16x16.fnt` + 不帶 `big5_u6_12x12.fnt`（淘汰）
- [ ] **5.4 README 加 v2.0 章節** — PC-98 1990 致敬、16×16 漢字真實解析度故事
- [ ] **5.5 RELEASE_NOTES_v2.0.md**
- [ ] **5.6 CHANGELOG.md 加 v2.0 entry**
- [ ] **5.7 git tag v2.0、push tag、merge `v2-16x16` → main**
- [ ] **5.8 GitHub Release v2.0 上傳 slim 版（FULL 留 local，含 IP）**
- [ ] **5.9 關 issue #1 + #2** 附 release link + 致謝
- [ ] **5.10 task #11 markdown sweep + task #12 過期檔清理**（v1.5.2 cancel 後重新排）

---

## 取消項（不做）

- ❌ issue #1.2 tile token 實機 verify（B.1 跟 leak 字串無關，留 v2.x patch 處理）
- ❌ issue #1.3 LB the noble ruler 實機 debug（同上）
- ❌ issue #1.4 intro 退化（v1.5.2 first wave longest-first sort 已修，Python sim 100% 通過）
- ❌ v1.5.2 rc 發布（直接跳 v2.0）

---

## 共存策略

- `main` branch 凍結在 v1.5.1 + v1.5.2 first wave (commits d80425d / 2028d63 / f052061 / b98ca29 / 3772561)
- `v2-16x16` branch 上做 Phase 1-5
- v2.0 ship 後 merge 回 main、tag v2.0
- v1.5.1 release 仍可下載（不撤回）

---

## 工程量總覽

| Phase | 估時 | 風險 |
|---|---|---|
| 0 source survey | ✅ 1 小時 | 低 |
| 1 字型 atlas | 1 天 | 低 |
| 2 overlay layer | 1-2 天 | 中（overlay 機制）|
| 3 三條 font path | 2-3 天 | 中（CHT 路徑保持）|
| 4 layout audit | 1-2 天 | 低-中 |
| 5 ship | 1 天 | 低 |
| **合計** | **6-9 天** | 中 |

---

## Reference

- [feedback-first-principles-step-by-step](https://github.com/wicanr2/u6-cht/blob/main/) — 拆問題到根
- [feedback-retro-remake-no-cost-ceiling](https://github.com/wicanr2/u6-cht/blob/main/) — 成本不是 decision factor
- global rule `81-retro-cjk-hires-canvas` — 拉高內部畫布 / 原生 CJK 16×16
- `docs/PLAYTEST.md` — game-tester harness（Phase 4 用）
- `skills/u6-cht.md` — engine hook 點清單（Phase 3 用）
