# U6 繁中化 Plan B In-Game Talk Path 驗證報告
**日期**：2026-05-21
**測試者**：自動 game tester
**引擎**：`/home/anr2/u6-cht/scummvm-src/scummvm` (fresh build)
**Display**：`DISPLAY=:2` (Xephyr 800×600)

---

## 1. 環境啟動驗證

### ScummVM 啟動 + 字型載入
日誌確認三個 font 系統全部載入成功：

```
WOUFont(cutscene): loaded big5_u6_12x12.fnt — intro CJK enabled
ConvFont: loaded big5_u6_12x12.fnt — ConverseGump CJK enabled
U6Font: loaded big5_u6_12x12.fnt — CJK enabled
CHT: loaded 7181 entries from cht_strings.tab (binary v1)
```

- 截圖 `u6_tester_01_startup.png`：遊戲 intro 播放正常（過場動畫）
- 截圖 `u6_tester_02_postesc.png`：主選單顯示 "Journey Onward"
- 截圖 `u6_tester_03_journey.png`：存檔載入，顯示 "Game Loaded"，party 成員 (anr2/Dupre/Shamino/Iolo) 全部 HP 90

**結論**：環境啟動 PASS。3 個 Big5 font msg 確認，7181 條 lookup 載入完成。

---

## 2. Talk NPC 路徑測試結果

### 2a. Talk Lord British (Conv VM NPC)

**操作**：click map → `t` → `KP_2`（向南），成功觸發 LB 對話

**結果**：**部分翻譯成功**
- LB 的錯誤答案回應：**「非也，此蓋有翼訂」** → Big5 顯示正確，單行清晰可讀
- 截圖：`u6_tester_18_lb_answer.png`、`u6_tester_19_lb_chinese.png`
- LB 開場詞（"But I must make sure 'tis truly thee."）→ 英文（lookup 未收錄）
- LB 結語（"Find thy Compendium, then come speak with me again."）→ 英文

### 2b. Talk Iolo (Party Member Conv VM)

**操作**：click map → `t` → click Iolo sprite (精確點擊)，成功觸發 Iolo 對話

**結果**：**多個翻譯條目成功渲染**

| Keyword | 預期中文 | 實際顯示 | 狀態 |
|---------|---------|---------|------|
| `name` | 「在下不記憶所及…」（唸作 Yo-low）| 顯示 Big5，但多行 wrap 重疊 | 部分 OK |
| `gwen` / `wife` | 「噢，閣下他日當請葛雯教你一曲。」| 顯示 Big5，但多行 wrap 重疊 | 部分 OK |
| `bard` | （Stones 曲子對話）| 英文（lookup 有收但 key 不匹配？）| MISS |
| `job` | —— | 英文（未收錄）| 英文 |

- 截圖：`u6_tester_40_talk_party2.png` ← **Talk-Iolo 觸發，顯示「汝見your old Friend Iolo.」（半中半英）**
- 截圖：`u6_tester_42_iolo_name.png` ← **Iolo name 回應，Big5 3行渲染（有 wrap bug）**
- 截圖：`u6_tester_49_gwen.png` ← **Gwenno 回應，Big5 渲染（有 wrap bug）**

### 2c. 重要發現：無 [ctl byte 0xXX] 錯誤

全部測試過程中，**日誌完全沒有出現 `[ctl byte]` 錯誤**。先前擔心的 Conv VM `0xA1-0xFE` bytecode 與 Big5 lead byte 衝突問題，在實際遊戲操作中**未被觸發**。Iolo、LB 的所有對話均正常進入翻譯 hook。

---

## 3. Look NPC 測試

**操作**：click map area（Look 命令自動觸發）

| Look 目標 | 期待 | 實際顯示 | 截圖 |
|-----------|------|---------|------|
| 地板 | 汝見地板 | `Look-汝見地板` ✓ | `u6_tester_51_look_dupre.png` |
| 地毯 | 汝見一張地毯 | `Look-汝見一張地毯。汝於此處搜尋，得無物。` ✓ | `u6_tester_06_focus_map.png` |
| 牆 | 汝見一面牆 | `Look-汝見一面牆` ✓ | `u6_tester_08_back.png` |
| Avatar (anr2) | 汝見 anr2 | `Look-汝見anr2` ✓ | `u6_tester_09_state.png` |
| Dupre（地圖上）| 汝見杜普雷 | `Look-汝見杜普`（截斷）| `u6_tester_23_talk_north.png` |

**Portrait header**（點擊 Iolo 肖像）：顯示 "Iolo"（英文），名字未透過 CJK hook 翻譯。Portrait header 繞過 lookup，屬已知限制。

---

## 4. 已知不翻譯字串清單

以下字串在測試中以英文顯示：

| 字串 | 分類 |
|------|------|
| "Game Loaded" | UI 系統訊息 |
| "Dupre barely wounded." | 戰鬥訊息 |
| "X grazed" / "wounded" | 戰鬥傷害訊息 |
| "Talk-nothing!" | 命令回饋 |
| "Talk-what?" | 命令回饋 |
| "Find thy Compendium, then come speak with me again." | LB 結語（未收錄） |
| "I've been a crossbow maker for so long, I've gotten weary of it." | Iolo job（未收錄） |
| "Yes, it's always been a hobby of mine." | Iolo bard（lookup 有但 key 不匹配）|
| "Have you heard the piece 'Stones' that I composed some years ago?" | Iolo bard（同上）|
| "Well, anr2, do you need help with something?" | Iolo greeting（未收錄或 $P 變數問題）|
| Portrait header 名字 (Iolo / Lord British) | Portrait GUI 繞過 hook |

---

## 5. Bug / 異常清單

### Bug 1：ConverseGump 中文 word-wrap 重疊（嚴重度：中）
- **現象**：長於 ~7 個漢字的翻譯字串在 ConverseGump 中以 2 欄方式渲染，字元重疊。
- **截圖**：`u6_tester_42_iolo_name.png`、`u6_tester_49_gwen.png`
- **根因**：ConvFont word-wrap 邏輯以英文字元寬度（~6-8px）計算換行，12px CJK 字符超出一行容量後被折行，但沒有以完整字元為單位換行，造成雙欄重疊。
- **短字串 OK**：「非也，此蓋有翼訂」（7 漢字）在 LB 對話中顯示正常，截圖 `u6_tester_19_lb_chinese.png`。
- **修復方向**：ConvFont 需要感知 CJK 字元寬度（每個 Big5 double-byte = 12px，英文 = 6px），調整 wrap threshold。

### Bug 2：ScummVM crash（一次）
- **現象**：在向北移動並點擊地圖非 NPC 位置後，遊戲黑屏並自動重啟
- **截圖**：`u6_tester_36_talk_skel.png`（黑屏）
- **嚴重度**：中（能自動重啟，非卡死）
- **可能原因**：點擊地圖外區域觸發空指標，或移動至邊界 tile
- **後續**：重啟後遊戲正常恢復

### Bug 3：「汝見your old Friend Iolo.」混合語言
- **現象**：Iolo 初始對話 "your old friend Iolo." 顯示為「汝見your old Friend Iolo.」
- **原因**：lookup 的 key 大小寫或 $P 佔位符不匹配，前半 "汝見" 來自另一個 prefix 翻譯，後半 "your old Friend Iolo." 原文未匹配
- **嚴重度**：低（對話開頭的描述文字，不影響主線劇情）

### Bug 4：文字截斷於 Gump 右邊界
- **現象**：「非也，此蓋有翼訂」中的 "訂" 可能是截斷的
- **根因**：ConverseGump 寬度固定，Big5 字元無法超出邊界
- **嚴重度**：低

---

## 6. Ship-ready 判斷

**Plan B in-game Conv VM 中文對話路徑可以上線，但有一個必須修復的視覺 bug：ConverseGump 長字串 word-wrap 重疊問題會讓多數 NPC 翻譯對話在顯示時嚴重變形、難以閱讀，在 word-wrap 修復前不建議公開發布。**

**具體情況**：
- 短翻譯（≤7漢字）：正常渲染 ✓
- 長翻譯（>7漢字）：重疊變形 ✗
- [ctl byte] 錯誤：無 ✓（Con VM Big5 lead/bytecode 衝突已不復現）
- 翻譯覆蓋率：只有已收錄 7181 條中匹配的字串才翻譯，其餘英文顯示

---

## 附件：截圖清單

| 截圖 | 說明 |
|------|------|
| `u6_tester_01_startup.png` | ScummVM 啟動 intro |
| `u6_tester_02_postesc.png` | 主選單 |
| `u6_tester_03_journey.png` | Game Loaded，party 列表 |
| `u6_tester_06_focus_map.png` | **Look 地毯「汝見一張地毯。汝於此處搜尋，得無物。」** |
| `u6_tester_08_back.png` | Look 牆「汝見一面牆」 |
| `u6_tester_13_t_cmd.png` | Talk 命令觸發 ">Talk-†" |
| `u6_tester_18_lb_answer.png` | **LB 中文回應「非也，此蓋有翼訂」初現** |
| `u6_tester_19_lb_chinese.png` | **LB 中文「非也，此蓋有翼訂」清晰截圖** |
| `u6_tester_40_talk_party2.png` | **Talk-Iolo 觸發，「汝見your old Friend Iolo.」** |
| `u6_tester_42_iolo_name.png` | **Iolo name 中文（Big5 wrap 重疊 bug）** |
| `u6_tester_49_gwen.png` | **Iolo Gwenno 中文（Big5 wrap 重疊 bug）** |
| `u6_tester_51_look_dupre.png` | Look 地板「汝見地板」 |
