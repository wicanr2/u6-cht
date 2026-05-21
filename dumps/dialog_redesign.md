# Ultima VI 繁中化 — 對話框重新設計報告

**作者**: UI/UX Designer Agent  
**日期**: 2026-05-21  
**版本**: v1.0  
**參考**: tester_pass3_report.md、editor2_report.md、docs/screenshots/*.png（11 張）

---

## A. 現況問題清單

### A1. 從截圖直接觀察（11 張截圖實機對照）

#### A1-1. cursor 座標系統錯位（嚴重）

- 來源：`msg_scroll.cpp:998` `drawCursor(area.left + left_margin + 8 * cursor_x, area.top + cursor_y * 8)`
- 問題：cursor Y 軸用 `cursor_y * 8`（8px stride），但 drawLine 已改為 `line_y * 10`（10px stride）
- 效果：每行累積 2px 偏移，到第 10 行已偏差 20px。cursor / 旋轉 Ankh / ↓ 提示符號全部顯示在錯誤位置，與文字重疊或落在文字下方空白處
- 截圖觀察：`07_combat_zh.png`、`08_attack_zh.png` 中可見 `↑` 游標符號 (`†`) 出現在行末緊貼文字，位置略低

#### A1-2. 末行溢出 panel 框外（嚴重）

- 數學推導：scroll_height=10，stride=10px，total=10×10=100px；panel 高度 `SCROLLWIDGETGUMP_H=100px`（加上 top padding 4px → 實際可用 96px，或包含 bottom 邊框更少）
- `MSGSCROLL_U6_HEIGHT=10`，classic UI `scroll_height * 8 = 80px`（panel 高度 80px）
- 現況：stride 從 8→10 但 panel 沒有跟著加高，最後 1-2 行可能被裁切或擠壓到框線外
- 截圖觀察：`07_combat_zh.png` 中「Anr2 輕度受傷。」最後一行底部接近 panel 下框

#### A1-3. 分頁過早觸發（中等）

- 來源：`msg_scroll.cpp:592` `if (autobreak && line_count > scroll_height - 1)`
- 問題：`scroll_height=10` 但因中文字高 12px 實際視覺上只能舒適顯示 8 行。在 autobreak 模式（NPC 長對話），10 行全部塞滿後才觸發 page_break，視覺上最後 2 行被擠壓到 panel 邊緣
- 效果：玩家看到的對話密度過高，閱讀體驗差

#### A1-4. ConverseGump scroll_height=10 vs Big5 12px 不匹配（嚴重）

- `ScrollWidgetGump::init` 設 `scroll_height = 10`，`SCROLLWIDGETGUMP_H = 100px`
- 每行 stride 10px（drawLine 第 144 行 `y += 10`）
- Big5 字型實際高度 12px → 每行有 2px 溢出到下一行 row 的頂端
- 截圖觀察：`10_lb_dialog.png` 中「非也，此答有誤」在 panel 內顯示但底部有輕微截切

#### A1-5. portrait label 區中文超寬（中等）

- `portrait_view_gump.cpp:143` `getCenter(actor_name_tr.c_str(), 138)` — label 置中範圍 138px
- 原版英文 NPC 名稱最多 12 char（如「Lord British」= 96px）
- 中文名如「不列顛王」= 4字×16px=64px → 尚可（在 138px 內）
- 但更長中文名如「月光城城主」= 6字×16px=96px → 仍在 138px 內
- 真正問題：GUI_FONT_GUMP 的 getCenter 計算是以 ASCII 字元寬度計算，對 Big5 雙位元組字元（每字顯示 16px 但 getCenter 可能只算 8px per byte）會造成置中偏移
- 截圖：`10_lb_dialog.png` 中「Lord British」標籤以 ASCII GUI_FONT 顯示（非 Big5 字型），中文轉換後若用 CHT translate 傳回中文字，GUI_FONT_GUMP 無法正確渲染 Big5

#### A1-6. 混合英中行無法正確斷行（低）

- 截圖：`09_talk_nothing.png` 中「>Attack with sword-地板．」英文 + 中文混合行
- `msg_scroll.cpp:420-425` 的 Big5 pair 偵測只處理純 Big5 token
- 混合行斷行依 `total_length` 計算（ASCII 字元數），Big5 字算 2 cells 但顯示 16px，可能造成行末提早或延遲換行

#### A1-7. clearCursor 只清 8×8 px，但 Big5 cursor 可能更大（低）

- `clearCursor(x, y)` → `screen->fill(bg_color, x, y, 8, 8)`
- 若 cursor 落在 Big5 字上，只清 8×8 像素，會殘留半個漢字的橘色底

#### A1-8. autobreak 邊界：scroll_height-1=9 行觸發 page_break（低）

- 對話 NPC 長段落一頁只能放 9 行（第 10 行觸發分頁），但 9 行中文 × 12px = 108px > 100px panel
- 實際上 autobreak 應在 7-8 行就觸發才合理

---

### A2. 從測試報告觀察

| 問題 | 來源報告 | 嚴重度 |
|------|----------|--------|
| 字型 log 顯示 12x12，但 Fix #7 要求 11px UMing | tester_pass3 §Fix #7 | 中 |
| 部分中文行尾有游標 `†` 符號露出在文字之後（xdotool 殘留 bug 外，原生 drawCursor 座標也有問題）| tester_pass3 §BUG-1 | 低 |
| 「汝見 a fireplace」混合顯示 | tester_pass3 §BUG-3 | 很低 |
| 混合行斷行（英文 + 中文）| tester_pass3 §BUG-4 | 很低 |
| `@EN（ZH）ZH` 重字 28 處，可能加重行長計算錯誤 | editor2 §C1 | 中 |

---

## B. 三個設計方案

### 方案一：保守方案 — Cursor 修正 + Stride 對齊

**目標**：最小 engine 改動，在現有 80/100px panel 尺寸內讓中文可讀。

#### 整體 layout（classic UI 模式，U6 原版 MsgScroll）

```
┌─────────────────────────────────────────┐  ← panel 高度維持 80px（scroll_height * 8）
│ 存檔已載入                              │  行 0  y=0
│ anr2:                                   │  行 1  y=8
│ >窺看－汝見地板                         │  行 2  y=16
│ anr2:                                   │  行 3  y=24
│ >†                                      │  行 4  y=32
│                                         │  行 5  y=40
│                                         │  行 6  y=48
│                                         │  行 7  y=56
│                                         │  行 8  y=64
│                                         │  行 9  y=72  ← 最後行底部=72+8=80px = 剛好
└─────────────────────────────────────────┘
```

**問題**：stride 8px，Big5 字 12px 高，每行重疊 4px → 字仍模糊重疊，只是 panel 不溢出。

**修法（方案一核心）**：

1. 縮減 scroll_height：`MSGSCROLL_U6_HEIGHT` 10 → **8 lines**
2. stride 維持 10px（已改）
3. panel 高 80px：8 lines × 10px = 80px，剛好容納（但 Big5 12px 高仍有 2px 溢出到下行間距）
4. cursor stride 修正：`drawCursor` y 改為 `cursor_y * 10`（與 drawLine 一致）
5. clearCursor 改為 `screen->fill(bg_color, x, y, 8, 12)` 清 12px 高

**行數 × 字數**：
- 行數：8 lines
- 每行字數：17 cells → 8 中文字 + 1 ASCII（因 Big5=2 cells/字）
- 有效中文容量：8 × 8 = 64 中文字/頁

**font size + stride**：
- 字型：12x12 Big5（現用）
- stride：10px（現用）
- 數學：12px 字高 / 10px stride = 2px 超出（可接受，底部 2 row 通常是空白）

**cursor 位置設計**：
- 修正 `drawCursor` 和 `clearCursor` 的 y 計算：`cursor_y * 10` 取代 `cursor_y * 8`
- 分頁 ↓ cursor 出現在 `scroll_height - 1` 行（第 7 行）末尾

**portrait label 處理**：
- 不改動。中文名已透過 CHT translate 傳入 `font->textOut()`，GUI_FONT_GUMP（bitmap ASCII font）無法渲染 Big5
- 暫時解決：若 translate 傳回原始 ASCII 名稱，label 正常顯示；若傳回中文，需確保 U6Font 接管 label 繪製

**engine 改動量**：
- `msg_scroll.h`：`MSGSCROLL_U6_HEIGHT` 10 → 8（1 行）
- `msg_scroll.cpp`：`drawCursor` y 計算（1 行）、`clearCursor` 高度（1 行）
- 共約 **3-5 行**修改

**優點**：改動最小，穩定性高，不需要改 bitmap  
**缺點**：8 lines 容量非常有限，長 NPC 對話分頁更頻繁；12px/10px stride 仍有輕微溢出

---

### 方案二：適度擴張 — NewUI Panel 加高 + stride 整齊化

**目標**：修正 ScrollWidgetGump（NewUI 模式）的尺寸，讓 12px 字型與 12px stride 完美對齊。

#### 整體 layout（NewUI ConverseGump，加高版）

```
╔══════════════════════════════════════════════════╗  ← 188px 寬（同 portrait gump 寬）
║  ┌──────────────────────────────────────────┐   ║
║  │ 不列顛王                                 │   ║  ← portrait label 區（12px 高）
║  │ [portrait 56×64]  STR DEX INT ...        │   ║  ← portrait + stats（原版）
║  └──────────────────────────────────────────┘   ║
╠══════════════════════════════════════════════════╣  ← 分隔線
║  行 0  你好，旅人。吾乃不列顛王，             ║  y= 4
║  行 1  此地之主。汝從何方而來？               ║  y=16
║  行 2  healing（醫療）/ repeat（重述）        ║  y=28
║  行 3  > you say: |                           ║  y=40
║  行 4                                         ║  y=52
║  行 5                                         ║  y=64
║  行 6                                         ║  y=76
║  行 7                                         ║  y=88
║  行 8                                         ║  y=100
║  行 9  ↓ [page break cursor]                  ║  y=112
╚══════════════════════════════════════════════════╝  ← 總高 128px（text area）
```

**說明**：
- `SCROLLWIDGETGUMP_H` 100 → **124px**（10 lines × 12px stride + 4px top padding）
- `SCROLLWIDGETGUMP_W` 200 → **200px**（維持）
- stride 改為 `y += 12`（取代現在的 `y += 10`）
- scroll_height 維持 10 lines
- `drawCursor` y 改為 `cursor_y * 12`
- `clearCursor` 改為 `screen->fill(bg_color, x, y, 16, 12)`（寬度改 16 以涵蓋 Big5 字游標）

**行數 × 字數**：
- 行數：10 lines
- 每行字數：(200 - 16) / 16 = **11 中文字**（扣掉左右各 8px padding 和 scroll arrow 8px）
- 有效中文容量：10 × 11 = **110 中文字/頁**

**font size + stride**：
- 字型：12x12 Big5（現用 `big5_u6_12x12.fnt`）
- stride：**12px**（數學整齊，字高=行距，0px 溢出）

**cursor 位置設計**：
- 旋轉 Ankh cursor 用 `cursor_y * 12` 計算，精確落在當前行底部
- ↓ page break cursor 出現在 row 9（最後行），不超出 panel

**portrait label 處理**：
- portrait gump 尺寸 188×91 不變
- label 區域（`area.top + 6`，寬 138px）改為：若 actor_name_tr 含 Big5，改用 ConvFont（U6Font）渲染，而非 GUI_FONT_GUMP
- 實作：在 `portrait_view_gump.cpp:147` 的 `font->textOut()` 加入 Big5 偵測，若有中文改呼叫 `conv_font->drawString()`

**engine 改動量**：
- `scroll_widget_gump.h`：`SCROLLWIDGETGUMP_H` 100 → 124（1 行）
- `scroll_widget_gump.cpp`：`y += 10` → `y += 12`（1 行）；cursor/clearCursor（2 行）
- `portrait_view_gump.cpp`：label 渲染邏輯（約 10-15 行）
- NewUI 背景 bitmap `portrait_bg.bmp` 若有固定高度需重繪（需確認）
- 共約 **20-30 行**修改 + 可能 1 張 bitmap 重製

**優點**：stride=font_size=12px，數學完美，10 行容量充足  
**缺點**：需確認 NewUI gump bitmap 是否有固定高度限制；portrait 區域 label 需改用 Big5 字型渲染（中等改動）

---

### 方案三：激進方案 — 全新 dialog gump（10px 字 + 12 lines + portrait 重排）

**目標**：重新設計整個 ConverseGump，10px 字型，12 行，portrait 移至對話框側邊，最大化中文容量。

#### 整體 layout

```
┌──────────────────────────────────────────────────────────────────┐
│  [P]  不列顛王                                                   │  ← header bar 20px
│  ┌──┐ ────────────────────────────────────────────────────────── │
│  │  │  行 0  你好，旅人。吾乃不列顛王，此地之主。              │
│  │肖│  行 1  汝從何方而來？吾與汝有諸多事宜商討。              │
│  │像│  行 2  healing（醫療）/ repeat（重述）                    │
│  │  │  行 3  > you say: |                                        │
│  └──┘  行 4  ...                                                  │
│         行 5  ...                                                  │
│         行 6  ...                                                  │
│         行 7  ...                                                  │
│         行 8  ...                                                  │
│         行 9  ...                                                  │
│         行 10 ...                                                  │
│         行 11 ...                                     ↓            │
└──────────────────────────────────────────────────────────────────┘
 ←─────────────────── 320px ────────────────────────────────────────→
 ↕ 170px total
```

**佈局細節**：
- 總寬：320px（原 NewUI 右側面板寬度）
- 總高：170px（12 lines × 10px stride + 40px header + 10px padding）
- portrait 縮小版（56×48px）嵌入對話框左側，header bar 顯示 NPC 名稱（Big5 字型）
- 文字區：右側 250px 寬，12 lines

**行數 × 字數**：
- 行數：**12 lines**
- 每行字數：(250 - 8) / 10 = **24 中文字**（10px 字）
- 有效中文容量：12 × 24 = **288 中文字/頁**（是現況的 3.6 倍）

**font size + stride**：
- 字型：**10px Big5**（需新建字型）
- stride：**10px**（數學整齊）
- 問題：AR PL UMing 無 10px embedded bitmap。需從 12px bitmap 縮小 → threshold binarize
  - 具體做法：`convert big5_u6_12x12.fnt -resize 83% -threshold 50% big5_u6_10x10.fnt`（概念，需實作 fnt 格式的 pixel rescaler）
  - 風險：10px 的部分筆劃（如「書」「靈」「醫」等複雜字）在 threshold 後可能缺筆或糊
  - 備選：使用 WQY MicroHei 10px（以 FreeType rasterize 到 10px，比 UMing 在小尺寸下更可讀）

**cursor 位置設計**：
- `cursor_y * 10`（stride=10px，cursor 計算天然對齊）
- 旋轉 Ankh / ↓ cursor 出現在 portrait 右側文字區的最後行末尾
- clearCursor 10×10px（與 10px 字等高等寬）

**portrait label 處理**：
- portrait 縮至 56×48px，嵌入對話框左上角
- header bar（全寬 320px，高 20px）中央顯示 NPC 名（Big5 U6Font 渲染，16px 或 10px）
- 原 portrait_view_gump 188×91 gump 停用，改用全新 ConverseGump 類別

**engine 改動量**：
- 新建 `ConverseGump.h/.cpp`（完整新 gump class）：約 **200-300 行**
- 新建 `big5_u6_10x10.fnt`（字型縮小工具）：1 個 Python/C script，約 80 行
- 修改 Converse 入口以使用新 gump：約 **30 行**
- 需修改 portrait 縮放/裁切邏輯：約 **20 行**
- 共約 **350-450 行**新增/修改

**優點**：最大容量，portrait+name 合一，stride=font_size 數學整齊，現代感強  
**缺點**：改動量龐大；10px 字型品質風險高；全新 gump class 需重新測試 edge case

---

## C. 推薦方案

**推薦：方案二（適度擴張）**

### 理由

#### 1. 讀者群偏好
Ultima VI 繁中化的目標讀者是懷舊玩家，接受復古像素風格但對可讀性有基本要求。12px Big5 字在截圖中清晰度已足夠（對比 `11_uming_11px.png` 的字型測試），10px 字可能對年長玩家造成閱讀壓力。方案二維持 12px 字型，對讀者最友善。

#### 2. 實作成本
- 方案一（3-5 行）：改動太小，core 問題（stride=10 vs font=12px 的 2px 溢出）未解決，視覺品質比方案二差但省工不多
- 方案二（20-30 行 + 1 bitmap）：適中，1-2 天可完成，風險低
- 方案三（350-450 行 + 字型工具）：工作量是方案二的 15 倍，10px 字型品質不確定，不適合 v1.1 sprint

#### 3. 視覺品質
- 方案二的 `stride=12 = font_height=12` 是數學上最整齊的設計，無 overlap、無 gap，每行字都完整顯示
- 10 lines × 11 字/行 = 110 字/頁，對 NPC 對話（平均段落 60-80 字）足夠，page_break 頻率大幅降低
- portrait label 改用 Big5 字型渲染，解決「不列顛王」等中文名稱渲染問題

#### 4. 相容性
方案二只修改 NewUI（ScrollWidgetGump），classic UI（MsgScroll）可分別調整，不互相干擾。

---

## D. 推薦方案（方案二）的 5 個 implementation steps

### Step 1：修正 line stride，讓數學整齊

**目標**：`stride = font_height = 12px`，消除 2px 溢出問題。

**檔案**：`/home/anr2/u6-cht/scummvm-src/engines/ultima/nuvie/views/scroll_widget_gump.cpp`

修改第 144 行：
```cpp
// 舊
y += 10;
// 新
y += 12;  // CHT: stride = Big5 font height (12px), zero vertical overlap
```

**驗證**：啟動遊戲，觀察中文行之間無重疊，ASCII 行之間有 4px 行距（acceptable）。

---

### Step 2：修正 cursor Y 軸計算

**目標**：`drawCursor` 和 `clearCursor` 的 y 座標與 stride 一致。

**檔案**：`/home/anr2/u6-cht/scummvm-src/engines/ultima/nuvie/gui/widgets/msg_scroll.cpp`

```cpp
// drawCursor（第 998 行附近）
// 舊
drawCursor(area.left + left_margin + 8 * cursor_x, area.top + cursor_y * 8);
// 新
drawCursor(area.left + left_margin + 8 * cursor_x, area.top + cursor_y * 12);  // CHT: stride 12

// clearCursor（第 994 行附近）
// 舊
clearCursor(area.left + 8 * cursor_x, area.top + cursor_y * 8);
// 新
clearCursor(area.left + 8 * cursor_x, area.top + cursor_y * 12);  // CHT: stride 12
```

**同時修正 clearCursor 的清除範圍**（`msg_scroll.cpp:1016`）：
```cpp
// 舊
screen->fill(bg_color, x, y, 8, 8);
// 新
screen->fill(bg_color, x, y, 16, 12);  // CHT: cover full Big5 glyph + stride
```

**驗證**：觸發 page_break，確認 ↓ cursor 出現在正確行末；輸入模式中旋轉 Ankh 不與文字重疊。

---

### Step 3：加高 NewUI panel 以容納 10 lines × 12px stride

**目標**：`SCROLLWIDGETGUMP_H` 加高到至少 `10 × 12 + 4（top padding）+ 4（bottom padding）= 128px`

**檔案**：`/home/anr2/u6-cht/scummvm-src/engines/ultima/nuvie/views/scroll_widget_gump.h`

```cpp
// 舊
static const int SCROLLWIDGETGUMP_H = 100;
// 新
static const int SCROLLWIDGETGUMP_H = 128;  // CHT: 10 lines * 12px + 8px padding
```

同時調整 `arrow_down_rect` 的 y 座標（在 `scroll_widget_gump.cpp` constructor 中），讓 ↓ scroll arrow 出現在新的底部位置。

**注意**：若 `portrait_bg.bmp` bitmap 有固定高度（需用 `file` 或 `identify` 指令確認實際 px），需同時重繪 bitmap 或改為程式動態填色（推薦後者，避免 bitmap 依賴）。

**驗證**：啟動 NewUI 模式，確認 panel 框線完整包住 10 行文字，無截切。

---

### Step 4：portrait label 改用 Big5 字型渲染

**目標**：NPC 名稱（如「不列顛王」「法師」「尤洛」）在 portrait label 區域以 Big5 U6Font 正確渲染，不再依賴 GUI_FONT_GUMP（ASCII only）。

**檔案**：`/home/anr2/u6-cht/scummvm-src/engines/ultima/nuvie/views/portrait_view_gump.cpp`

在 `Display()` 函式的 label 渲染區塊（第 142-147 行附近）：

```cpp
// 現況（只支援 ASCII GUI_FONT_GUMP）
Common::String actor_name_tr = CHTranslate::get()->translate(actor->get_name());
w = font->getCenter(actor_name_tr.c_str(), 138);
font->textOut(screen->get_sdl_surface(), area.left + 29 + w, area.top + 6, actor_name_tr.c_str());

// 改後（偵測 Big5，分支處理）
Common::String actor_name_tr = CHTranslate::get()->translate(actor->get_name());
bool has_cjk = ((uint8)actor_name_tr[0] >= 0xA1 && actor_name_tr.size() >= 2);
if (has_cjk && conv_font != nullptr) {
    // 用 U6Font（Big5）渲染，手動計算置中
    uint16 str_px = actor_name_tr.size() / 2 * 16;  // Big5: 2 bytes = 16px
    int x_center = area.left + 29 + (138 - str_px) / 2;
    conv_font->drawString(screen, actor_name_tr.c_str(), x_center, area.top + 6, 0x08, 0);
} else {
    // 原 ASCII 路徑
    w = font->getCenter(actor_name_tr.c_str(), 138);
    font->textOut(screen->get_sdl_surface(), area.left + 29 + w, area.top + 6, actor_name_tr.c_str());
}
```

**前置條件**：`PortraitViewGump` 需持有 `conv_font` 指標（ConvFont/U6Font instance），需在 `init()` 中初始化（參考 ConverseGump 的 ConvFont 取得方式）。

**驗證**：與「不列顛王」對話，portrait header 正確顯示「不列顛王」中文；與英文名 NPC 對話仍正常。

---

### Step 5：autobreak 閾值調整 + 全面驗證

**目標**：autobreak 在 8 行（而非 9 行）觸發 page_break，避免最後 2 行被擠壓到 panel 底部框線。

**檔案**：`/home/anr2/u6-cht/scummvm-src/engines/ultima/nuvie/gui/widgets/msg_scroll.cpp`

```cpp
// 現況（第 592 行）
if (autobreak && line_count > scroll_height - 1)
    set_page_break();

// 改後（預留 2 行 padding buffer 應對 Big5 12px 的視覺佔用）
// scroll_height=10，希望在 8 行滿時觸發
if (autobreak && line_count > scroll_height - 3)  // CHT: -3 instead of -1, 2-line visual buffer
    set_page_break();
```

**然後執行完整驗證**：
1. 進入遊戲，與 Lord British 對話（長段落 NPC），確認每頁最多顯示 8 行中文，無截切
2. 測試 page_break cursor：↓ 符號出現在正確位置，按鍵後正確翻頁
3. 測試旋轉 Ankh cursor：對話結束時 Ankh 出現在最後一行末尾，不遮擋文字
4. 測試 portrait label：「不列顛王」「法師」「尤洛」等名稱正確顯示
5. 截圖存入 `docs/screenshots/12_dialog_v2.png`

---

## E. Risks 與 Fallback

### Risk 1：portrait_bg.bmp 有固定高度限制

**描述**：若 bitmap 硬編碼高度無法配合 `SCROLLWIDGETGUMP_H=128px`，panel 底部會露出背景色或裁切。

**Fallback**：
- 選項 A：重繪 `portrait_bg.bmp`（增加 28px 高度）
- 選項 B：在 `ScrollWidgetGump::Display()` 改為程式動態填色（`screen->fill(bg_color, ...)`），不依賴 bitmap
- 建議先用 `identify portrait_bg.bmp` 確認實際尺寸，再決定

### Risk 2：conv_font 在 PortraitViewGump 不可用

**描述**：U6Font（ConvFont）可能在 portrait gump 初始化時還未建立，導致 null pointer。

**Fallback**：
- 在 Step 4 的 Big5 渲染分支加 null check（已包含在範例程式碼中）
- 若無 conv_font，fallback 到 ASCII 路徑（名稱保持英文，退化但不崩潰）
- 長期：在 `PortraitViewGump::init()` 加入 ConvFont 取得邏輯（參考 `ConverseGump` 的做法）

### Risk 3：10px 字型品質不達標（方案三風險）

**描述**：若未來嘗試方案三，10px Big5 字型從 12px downscale 後，複雜漢字（醫、靈、藥）可能缺筆。

**Fallback**：
- 使用 WQY MicroHei 10px（FreeType rasterize，保留 hinting），品質優於 bitmap downscale
- 若 10px 仍糊：退回 11px（`big5_u6_11x12.fnt` 現有字型），stride 改 11px
- 若仍不滿意：完全放棄方案三，回到方案二

### Risk 4：autobreak 閾值調整影響 classic UI

**描述**：`MSGSCROLL_U6_HEIGHT=10`（classic UI）的 autobreak 邏輯與 NewUI 共用，`-3` 可能讓 classic UI 的 ASCII 對話分頁過早。

**Fallback**：
- 加入 game_type 判斷：
  ```cpp
  int page_threshold = (is_cjk_mode && game_type == GAME_U6) ? 3 : 1;
  if (autobreak && line_count > scroll_height - page_threshold)
  ```
- 或僅在 `ScrollWidgetGump` 子類別中 override autobreak 行為

### Risk 5：Step 2 cursor 修正影響 classic UI 座標

**描述**：`drawCursor` 修正為 `cursor_y * 12` 後，classic UI（stride 仍 10px）的 cursor 位置會比文字低 2px/行（第 10 行累積 20px 偏差）。

**Fallback**：
- 在 `MsgScroll::drawCursor()` 加入虛函式或 stride 成員變數：
  ```cpp
  virtual int get_line_stride() { return 8; }  // base: classic UI 8px
  // ScrollWidgetGump override:
  int get_line_stride() override { return 12; }  // NewUI: 12px
  ```
- 讓 `drawCursor` 用 `get_line_stride()` 取代 hardcoded 8，子類別各自回傳正確 stride

---

*報告完成。推薦主程式優先實作 Step 1-3（pure engine 改動，約 1 天），確認視覺後再進行 Step 4-5。*

*本報告純設計文件，不含程式碼修改，所有 code snippet 為說明用參考。*
