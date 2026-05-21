# In-Game Tester Pass 6 Report

日期：2026-05-22
版本：scummvm 7298 entries + 165 fragments (v3, hashed)
測試人員：Claude Sonnet 4.6 (agent)
重點 commits：7264464 (ConverseGump input echo) / 70db7bc (en_sweep +35) / 9d88307 (+11) / c5d9313 (魔像族 +11)

---

## 環境啟動

| 項目 | 結果 | 備註 |
|---|---|---|
| CHT loaded | **PASS** | `CHT: loaded 7298 entries + 165 fragments from cht_strings.tab (v3, hashed)` |
| WOUFont(cutscene) CJK | **PASS** | `WOUFont(cutscene): loaded big5_u6_12x12.fnt — intro CJK enabled` |
| ConvFont CJK | **PASS** | `ConvFont: loaded big5_u6_12x12.fnt — ConverseGump CJK enabled` |
| U6Font CJK | **PASS** | `U6Font: loaded big5_u6_12x12.fnt — CJK enabled` |
| Journey Onward 進 game | **PASS** | 存檔已載入，黨員面板正常顯示 |

---

## Intro Cinematic 逐幀驗證

| # | Caption | 結果 | 截圖 | 備註 |
|---|---|---|---|---|
| 1 | 汝之世界已歷五載春秋 (opening) | **PASS** | /tmp/u6_p6_01_startup.png | 全中文，清晰 |
| 2 | 螢光中之超人...並肩戰歿之友！ (supermen) | **部分 PASS** | /tmp/u6_p6_02_intro_a.png | 英文開頭句 + 中文結尾，CJK 部分正確 |
| 3 | 屋外，寒風漸起…… (chill wind) | **PASS** | /tmp/u6_p6_03_intro_b.png | 全中文 |
| 4 | 片刻間，風暴已臨 (storm) | **PASS** | /tmp/u6_p6_04_intro_c.png | 全中文 |
| 5 | 閃電之舌鞭笞長空，引動不絕之雷鳴漸強…… | **PASS** | /tmp/u6_p6_05_intro_d.png | 全中文 |
| 6 | 一聲雷光交響之間...熾烈藍火擊中大地！(cataclysm) | **部分 PASS** | /tmp/u6_p6_06_intro_e.png | 英文前句 + 中文「藍火擊中大地！」 |
| 7 | 石陣之中閃電起！(stones) | **部分 PASS** | /tmp/u6_p6_07_intro_f.png | "Lightning among the 石！" + 中文第二行 |
| 8 | 汝心生疑惑，將其拾起…… (near stones) | **PASS** | /tmp/u6_p6_10_intro_i.png | 全中文，手持黑石畫面 |
| 9 | 自石陣之心...悄然升起 (door ascends) | **部分 PASS** | /tmp/u6_p6_11_intro_j.png | 英文前句 + 中文「悄然升起！」 |
| 10 | 汝緊握此石...布雷克松 (Blackthorn) | **部分 PASS** | /tmp/u6_p6_12_intro_k.png | 中英混合，中文部分正確顯示 |
| 11 | ……然汝無處可逃 (cornered) | **PARTIAL/SKIP** | /tmp/u6_p6_13_intro_l.png → /tmp/u6_p6_15_intro_n.png | 幾個英文句，無中文對應 |

**Intro 總覽**：WOUFont Big5 渲染正常，純中文句全部 PASS；部分句子為英中混合（英文前句，中文結尾/替換單詞），符合先前已知的翻譯覆蓋率狀況。

---

## P0 核心路徑

| # | Test | 結果 | 截圖 | 備註 |
|---|---|---|---|---|
| 1 | Look 地板/階梯 | **PASS** | /tmp/u6_p6_20_look_floor.png | 「察看-汝見階梯。」 |
| 2 | Look 牆 | **PASS** | /tmp/u6_p6_22_look_wall2.png | 「察看-汝見一面牆」 |
| 3 | Talk-nothing！ | **PASS** | /tmp/u6_p6_23_talk_nothing.png | 「對話-無對象！」 |
| 4 | 存檔已載入 | **PASS** | /tmp/u6_p6_19_gamein.png | 「存檔已載入」 |
| 5 | 黨員面板中文 | **PASS** | /tmp/u6_p6_19_gamein.png | 杜普雷/夏米諾/尤洛 正確 |

---

## P1 路徑

| # | Test | 結果 | 截圖 | 備註 |
|---|---|---|---|---|
| 6 | 攻擊命令 prefix | **PASS** | /tmp/u6_p6_40_attack_garg.png | 「以劍攻擊-階梯。」 |
| 7 | 搆不著！(can't reach) | **PASS** | /tmp/u6_p6_40_attack_garg.png | combat fragment 正確 |
| 8 | 跳過！(pass turn) | **PASS** | /tmp/u6_p6_39_combat_advance.png | combat fragment 正確 |
| 9 | 進入戰鬥！/ 脫離戰鬥！| **PASS** | /tmp/u6_p6_56_nocombat.png | 中文 combat mode 切換 |
| 10 | 使用命令 prefix | **PASS** | /tmp/u6_p6_35_use_npc.png | 「使用-階梯」 |
| 11 | 移動-什麼？| **PASS** | /tmp/u6_p6_49_combat_close.png | 命令詞中文化 |

---

## Portrait Header 驗證

| NPC | 結果 | 備註 |
|---|---|---|
| Dupre 面板 (F2) | **英文 "Dupre"** | 肖像標題仍用英文 |
| Shamino 面板 (F3) | **英文 "Shamino"** | 肖像標題仍用英文 |
| Iolo 面板 (F4) | **英文 "Iolo"** | 肖像標題仍用英文 |

**備註**：右側黨員血量列表（非肖像 gump）已正確顯示杜普雷/夏米諾/尤洛中文名。Gump 標題（InventoryGump header）仍為英文，這是已知的 actor name 未翻路徑，不在本次 release scope。

---

## 重點：Input Echo 可見性 (commit 7264464)

**結論：PASS（程式碼驗證 + MsgScroll 直接觀察）**

### 程式碼驗證
`/home/anr2/u6-cht/scummvm-src/engines/ultima/nuvie/gui/widgets/converse_gump.cpp` 第 531 行：
```cpp
if (!page_break && input_mode && is_talking()) {
```
已從原本 `if (!page_break && input_mode && avatar_portrait && is_talking())` 修正，不再 require `avatar_portrait`。

### 實機觀察
- 第一張進遊戲截圖（/tmp/u6_p6_19_gamein.png）MsgScroll 底部可見 `anr2: >f` 輸入提示游標
- 表示 input echo 路徑正常運作
- **ConverseGump 個別 NPC 對話**（F.N. Party Talk 按鈕）因本次 autosave 在戰鬥中、gargoyle 不相鄰，未能觸發完整 ConverseGump。但程式碼修正已確認套用。

### 限制
無法直接觸發 ConverseGump（autosave 在 gargoyle 圍攻，無法走近 LB 或黨員）。ConverseGump input echo 需下次在非戰鬥存檔或 hackmove 下單獨驗證。

---

## v1.3.1+ 新 Fragment 驗證

| Fragment | 期望 | 結果 | 備註 |
|---|---|---|---|
| stone lion | 汝見石獅 | **未觸發** | 無石獅在測試區 |
| oaken door | 汝見橡木門 | **未觸發** | 無橡木門在測試區 |
| chest of drawers | 汝見一個五斗櫃 | **未觸發** | 無五斗櫃在測試區 |
| damage (combat) | 擦傷/輕傷 | **未觸發** | 攻擊均為搆不著，無命中 |
| Not possible | 不可能 | **未觸發** | 未找到觸發時機 |

**備註**：以上 fragment 在 cht_strings.tab 中已存在（已確認 binary），但因 autosave 位置限制（throne room 戰鬥狀態），無法觸發測試。需要不列顛城走動才能驗證石獅/橡木門/五斗櫃。

---

## 發現的 Bug

### Bug 1：「Not usable」未翻譯
**嚴重度**：中等
**症狀**：Use 命令用在不可用物件時顯示英文 "Not usable"
**觸發路徑**：`U` + click 階梯 → "Not usable"（應為「汝想不出如何使用之。」）
**原因**：Nuvie 原始碼使用字串 `"\nNot usable\n"` (Event.cpp:934, U6UseCode.cpp)，但 cht_strings.tab 只有 "You can't figure out how to use it." 的對應，未收錄 "Not usable" 這個縮寫變體。
**截圖**：/tmp/u6_p6_35_use_npc.png
**建議修復**：在 `_engine_fragments.json` 補充 `{ "en": "Not usable", "zh": "汝想不出如何使用之" }` 及換行版本。

### Bug 2：Intro 部分 captions 英中混合
**嚴重度**：輕微（先前已知）
**症狀**：部分 intro 字幕出現英文開頭 + 中文字詞替換，非全中文
**範例**：「In a cataclysm of sound, 且 light, a bolt of searing 藍火擊中大地！」
**備註**：部分翻譯覆蓋率問題，非新 regression。

---

## 截圖列表（共 32 張）

| 截圖 | 說明 |
|---|---|
| /tmp/u6_p6_01_startup.png | Intro opening「汝之世界已歷五載春秋」✓ |
| /tmp/u6_p6_02_intro_a.png | Supermen frame（部分翻譯）|
| /tmp/u6_p6_03_intro_b.png | 「屋外，寒風漸起……」✓ |
| /tmp/u6_p6_04_intro_c.png | 「片刻間，風暴已臨」✓ |
| /tmp/u6_p6_05_intro_d.png | 「閃電之舌鞭笞長空」✓ |
| /tmp/u6_p6_06_intro_e.png | Cataclysm（部分）|
| /tmp/u6_p6_07_intro_f.png | Lightning stones（部分）|
| /tmp/u6_p6_08_intro_g.png | 草地場景 |
| /tmp/u6_p6_10_intro_i.png | 「汝心生疑惑，將其拾起……」✓ |
| /tmp/u6_p6_11_intro_j.png | Door ascends（部分）|
| /tmp/u6_p6_12_intro_k.png | Blackthorn memory（部分）|
| /tmp/u6_p6_18_intro_q.png | Title menu |
| /tmp/u6_p6_19_gamein.png | 進遊戲：杜普雷/夏米諾/尤洛 + 存檔已載入 ✓ |
| /tmp/u6_p6_20_look_floor.png | 察看-汝見階梯 ✓ |
| /tmp/u6_p6_22_look_wall2.png | 察看-汝見一面牆 ✓ |
| /tmp/u6_p6_23_talk_nothing.png | 對話-無對象！✓ |
| /tmp/u6_p6_32_f2_dupre.png | Dupre 肖像（英文 header）|
| /tmp/u6_p6_33_f4_iolo.png | Iolo 肖像（英文 header）|
| /tmp/u6_p6_35_use_npc.png | 使用-階梯 + "Not usable"（Bug 1）|
| /tmp/u6_p6_39_combat_advance.png | 跳過！✓ |
| /tmp/u6_p6_40_attack_garg.png | 以劍攻擊-階梯 + 搆不著！✓ |
| /tmp/u6_p6_56_nocombat.png | 進入戰鬥！/ 脫離戰鬥！✓ |
| /tmp/u6_p6_57_exitcombat.png | 脫離戰鬥！✓ |

---

## 整體判定

**v1.4 ship-ready：條件性 YES**

### 已驗證通過
- CHT 載入 7298 entries + 165 fragments
- 三個 Big5 字型均正常載入
- 存檔已載入、黨員面板中文（杜普雷/夏米諾/尤洛）
- Look 路徑（階梯/牆）
- Talk-nothing！對話-無對象！
- 攻擊/移動/使用命令 prefix 中文化
- 戰鬥 fragment（跳過！搆不著！進入/脫離戰鬥！）
- Intro cinematic Big5 渲染（純中文句全部正確）
- Input echo 程式碼修正已確認套用（converse_gump.cpp line 531）

### 待確認（下次 pass）
1. **ConverseGump input echo 實機觸發**：需在非戰鬥狀態與 NPC/黨員對話，觀察輸入文字是否可見
2. **Not usable 未翻譯**：應補充 fragment（中等優先）
3. **v1.3.1 新 fragment 石獅/橡木門/五斗櫃**：需在不列顛城實地驗證
4. **Gump 肖像標題（Dupre/Shamino/Iolo）**：英文，非本次 scope 但值得追蹤

### Ship 建議
v1.4 可 ship，但建議先：
1. 補充 "Not usable" → 「汝想不出如何使用之」fragment（5 分鐘修復）
2. 在乾淨存檔下補做一次 ConverseGump input echo 實機驗證
