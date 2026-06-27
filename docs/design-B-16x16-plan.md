# B 計畫：16×16 漢字真實解析度（仿 PC-98 1990）— v2.0 path

> 2026-06-27 user 拍板走 B（PC-98 1:1 真實 16×16 解析度），取消 v1.5.2 fix work 與所有實機 verify 預排任務。
> 配套 `docs/design-16x16-feasibility.md`（idea 階段討論）、global rule `81-retro-cjk-hires-canvas`。

---

## 目標（一句話）

跟 PC-98 1990 版 U6 一樣：**320×200 game asset 不重畫、純 2× scale**；**漢字用 native 16×16 真實解析度寫到 scaled stage**。
結果視覺等同 PC-98 — 圖形 retro、字清楚、layout 不縮水。

非目標：圖形重畫、加 high-res sprite、改 game logic。

---

## 根本前提（Phase 0 必驗）

B 計畫成立的前提是 **3 個未驗證的事實**。**動實作前先 read source 驗清楚**，不繼續憑直覺。

| ID | 前提 | 驗法 | 失敗時影響 |
|---|---|---|---|
| **P1** | ScummVM `OSystem` 提供「寫 native 視窗 surface（640×480）pixel」的 API | grep `engines/ultima/nuvie/screen/screen.cpp` + `common/system.h` 找 `lockScreen` / `copyRectToScreen` / `getOverlaySurface` 等 abstraction，看是 320×200 only 還是可走 native | 失敗 → fork ScummVM 框架 / 不可行 → 退路線 A |
| **P2** | 對話框 chrome（黃花邊 frame）跟字 render 是分離的、chrome 可獨立保留 framebuffer pixel scale | grep `msg_scroll.cpp` + `converse_gump.cpp` 找 chrome 繪製 vs 字繪製的 surface target | 失敗 → chrome + 字必須一起 scaled，layout 須完全重畫 |
| **P3** | 三條 font path（U6Font / ConvFont / WOUFont）的 drawString 入口可獨立替換 | grep 三個 .cpp 看 drawString 接口、誰呼叫、有沒共用 base class | 失敗 → 要修共用 base，scope 漲 |

**Phase 0 估時**：1 天（純 read + grep + 寫一份 phase0 findings markdown）。

---

## 階段分解

### Phase 0: 前提驗證（read-only）

- [ ] P1: ScummVM OSystem native surface API survey
- [ ] P2: 對話 chrome vs 字 render path 分離度
- [ ] P3: U6Font / ConvFont / WOUFont 三條 entry point map
- [ ] 輸出 `docs/phase0-findings.md` — 確認 B 可走 / 不可走 / 部分可走
- [ ] **決策點**：若 P1 失敗 → 跟 user 重新議；P2/P3 失敗只是 scope 漲、不取消

### Phase 1: 字型 atlas 16×16 build pipeline

- [ ] 改 `tools/build-big5-font-wqysharp.py` → 16×16，glyph 32 bytes
  - WQY zenhei 16×16 embedded bitmap 是否存在？需 verify（face index、size）
  - 若 WQY 16px embedded 不存在 → outline render 16px or 換字型（思源黑體 / Source Han Sans HW）
- [ ] 產 `big5_u6_16x16.fnt`（預估 14758 × 32 = 472 KB）
- [ ] 寫 dump tool 比對「杜」glyph 在 16×16 vs 12×12 視覺差
- [ ] **decision gate**：visual diff 確認 16×16「杜」清楚到不會誤認為「壯/狀/牡」

### Phase 2: 對話 chrome 處理（depends on Phase 0 P2）

兩個 sub-path 二選一：

- (a) **chrome 保留 framebuffer pixel scale，只字走 native overlay**（PC-98 真實做法）
  - chrome 320×200 → 640×400 同步 scale
  - 字位置算在 native 640×400 座標
  - chrome 內預留位置等同 12px 字位置（即 chrome 寬不變、字寬密度變高）
- (b) **chrome 與字都走 native scaled surface**（lower risk）
  - chrome 重畫 native 解析度
  - 工程量大、需 redraw chrome asset 或 nearest-scale chrome

**default 走 (a)**，因為 user 強調「畫面跟現在一樣」。

### Phase 3: 三條 font path 改 native surface write

- [ ] **U6Font**（MsgScroll 主對話框）
  - `engines/ultima/nuvie/fonts/u6_font.cpp` 找 drawString
  - 改寫到 native surface（API 由 Phase 0 P1 決定）
  - 對齊 chrome 預留字位
- [ ] **ConvFont**（ConverseGump NewUI 對話）
  - `engines/ultima/nuvie/fonts/conv_font.cpp`
  - NewUI 對話走變寬字，要重算 wrap
- [ ] **WOUFont**（cutscene / intro）
  - `engines/ultima/nuvie/fonts/wou_font.cpp`
  - intro 字幕 wrap、cutscene 對齊
- [ ] **CHT hook 點**：8 個 hook 點仍走 cht_strings.tab v3 lookup，不變

### Phase 4: layout audit + visual diff

- [ ] 200+ NPC 對話跑一輪 game-tester（用既有 PLAYTEST.md harness）
- [ ] 截圖比對 v1.5.1（12px） vs v2.0（16px）
- [ ] 重點抓：字 overflow、wrap 異常、chrome 字錯位、cutscene fit
- [ ] 朋友 finding 驗證：「杜普雷」是否清楚

### Phase 5: ship v2.0

- [ ] cht_strings.tab 不變（lookup 邏輯不動）
- [ ] 重 build scummvm patched
- [ ] AppImage / Windows zip（依 retro-game-cht-package skill）
- [ ] README 加「v2.0 visual upgrade」章節 + PC-98 ref
- [ ] CHANGELOG / RELEASE_NOTES_v2.0.md
- [ ] git tag v2.0

---

## 工程量估算

| Phase | 工 | 風險 |
|---|---|---|
| 0 前提驗證 | 1 天 | 低（純 read）|
| 1 字型 atlas | 1 天 | 低 |
| 2 chrome 處理 | 2-3 天 | 中（depends Phase 0 P2）|
| 3 三條 font path | 3-5 天 | 中（depends Phase 0 P1）|
| 4 layout audit | 2-3 天 | 低-中 |
| 5 ship | 1 天 | 低 |
| **總計** | **10-14 天** | 中 |

**最大不確定**：Phase 0 P1。若 ScummVM `OSystem` 不允許 native surface 寫，Phase 3 工程量會跳 2-3×（需 fork framework）。**先驗 P1 再投入後續**。

---

## 回退路徑

如果 Phase 0 P1 失敗：
1. **fallback to 路線 A**（framebuffer 內 16×16），跟 user 重新議
2. layout 容量縮 40%（17 字 × 6 行 vs 23 字 × 8 行）
3. 工程量降回 3-5 天
4. 字清楚度仍大幅好過 12×12

如果 Phase 3 工程超預估：
1. **階段 ship**：先一條 font path（如 U6Font 主對話），其他兩條繼續 12px
2. v2.0-rc1 ship 部分 native 16×16，剩下 v2.0.x 補
3. **不退**（v1.5.1 keep 可用）

---

## v1.5.x ↔ v2.0 共存策略

- v1.5.x branch keep（main 暫凍）
- 開 `v2-16x16` branch 做 B
- main 仍保留 v1.5.1 + opened/closed fix + intro longest-first sort
- v2.0 ship 後 v1.5.x deprecated（但已下載者可繼續用）
- 不 revert v1.5.2 已 commit work（commit b98ca29 / f052061 / 2028d63 / d80425d 全 keep）

---

## 取消清單（2026-06-27 拍板）

以下 v1.5.2 後續工作 **全取消** — 走 B 後不需要：

- ❌ issue #1.2 `tile` token 實機 verify 與 fragment 微調
- ❌ issue #1.3 LB `the noble ruler of...` 實機 `CHT-LOOK actor-look:` 抓
- ❌ issue #1.4 intro 7 段實機 verify（Python sim 已 100% 通過）
- ❌ 朋友「杜 glyph」finding（v2.0 16×16 根本解決）
- ❌ v1.5.2 後 markdown 文件 sweep 同步度（task #11）
- ❌ v1.5.2 後過期/重複檔清理（task #12）

issue #1 / issue #2 仍 open，**等 v2.0 ship 時一併關**。

---

## 下一步（執行順序）

1. **commit 本 design doc** — 把 plan 寫死進 repo
2. **Phase 0 啟動** — 開新 branch `v2-16x16`、跑 P1/P2/P3 source survey
3. Phase 0 findings → 跟 user 拍板繼續 Phase 1
