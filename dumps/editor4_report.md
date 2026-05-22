# Ultima VI 繁中化 — 第四輪總編輯深度校對報告（editor4）

**日期**：2026-05-22
**基礎版本**：v1.4（commit 0834eed）
**前三輪 editor**：editor1（P0-1～P0-6）、editor2（25 個重字 bug）、editor3（E3-P0-1/2 + 6 個 P1）
**本輪範圍**：抽查 20 個新 NPC（040–091 段，不重複前三輪）、PDF 交叉比對、格式 sweep、整體三判

---

## A. 抽查 20 NPC 評分表

### 抽查範圍
040_Manrel、041_Penumbra、042_Derydlus、043_Zellivan、045_Stelnar、047_Heftimus、051_Arvin、053_Peer、055_Le'nard、057_Utomo、058_Nicodemus、060_Boskin、063_Isabella、070_Dale、072_Trebor、076_Whitsaber、082_Trenton、085_Marta、089_Marney、091_Quenton

### 評分表（1=差；5=優）

| # | NPC | 分數 | 評語 |
|---|---|---|---|
| 1 | 040_Manrel | 4 | 木工+煉金術+刺青故事完整；`@tattooed（符號）`括號語義略混（見 B 節）；文白一致 |
| 2 | 041_Penumbra | 4 | 占卜師長篇詐騙對話流暢；「日蝕之女」精準；quest clue（紫/藍鏡片）準確完整 |
| 3 | 042_Derydlus | 3 | 主體 OK；`@drink（飲品）杯`語義怪異（見 B 節）；`他微笑道`誤加說話語氣詞（見 B 節） |
| 4 | 043_Zellivan | 4 | Jhelom 城主風格到位；`@tales故事`缺括號（P1 格式問題）；其餘準確 |
| 5 | 045_Stelnar | 4 | 武士口吻生動；「靈魂林」地名一致；Shamino 引介對話正確；魔像族/辛弗拉處理得當 |
| 6 | 047_Heftimus | 4 | 海盜乞丐口音（俺）貫徹全篇；`doubloon`→`銀幣`（應為金幣）小失誤；整體5分但此扣一 |
| 7 | 051_Arvin | 4 | 酒館老闆短促語氣合適；商品翻譯（餐包/麥酒/蜂蜜酒/葡萄酒/口糧）與 distilled 一致 |
| 8 | 053_Peer | 5 | 造船師短篇幽默對話（「父親不會拼字」笑話）完整傳達；`@ships（大船）` / `@skiffs（小艇）`清晰 |
| 9 | 055_Le'nard | 4 | 膽小裁縫口音（哈、哈囉）完整；`@tunics（短）上衣`括號截斷（P1 格式問題，見 B 節） |
| 10 | 057_Utomo | 3 | Utomo 外國人破英文口吻保留得宜；`@kill（殺好）人`嚴重語義錯誤（P0，見 B 節）；`@Omdu Yaf`維持原語正確 |
| 11 | 058_Nicodemus | 5 | 魔法師老者語氣生動；法術/材料術語與 distilled 手冊完全吻合；一處`天佑我`改回`吾`即可 |
| 12 | 060_Boskin | 4 | 盜賊方言（俺）角色語氣一致；孩子/道德爭辯完整呈現；`@out（出去）`語義正確 |
| 13 | 063_Isabella | 4 | 密諾克市長高雅口吻；`@sacrifice（奉獻）`誤用（應為「犧牲」，見 C 節）；其餘準確 |
| 14 | 070_Dale | 4 | 玻璃工匠口吻活潑；`@Glassblower（玻璃）工匠`漏「吹製」職稱精確度（見 B 節）；寶石/玻璃劍 OK |
| 15 | 072_Trebor | 5 | 與 053_Peer 同模板（不同城市船匠），翻譯一致且完整 |
| 16 | 076_Whitsaber | 3 | 崔西克市長（昔日海盜）雙重人格對話生動；**多處 吾/我 同句混用**（P1，見 B 節）；「summ」真言保留正確 |
| 17 | 082_Trenton | 3 | Skara Brae 自傲市長語氣到位；`@rigging（爬桅）杆`誤譯（見 B 節）；`吾/我`混用 26 處（P1）；Honor→大人翻法正確（非美德用法） |
| 18 | 085_Marta | 4 | 農村主婦用`我`全程一致（刻意現代語風格）；語句輕快；無 bug |
| 19 | 089_Marney | 3 | 詩意場景翻得流暢美麗；`@killed`格式錯誤（P0，見 B 節）；`吾/我/汝/你`四種混用（P1）；`吾鎮`+`我父親`同句漂移 |
| 20 | 091_Quenton | 5 | 幽靈無聲敘事氣氛完美；場景描寫（旋渦/強風/寒意）忠實原文且文學性強 |

**平均分：3.95 / 5.0**

---

## B. 新發現 P0 / P1

### P0（必修，影響遊戲邏輯或格式崩潰）

| # | 檔案 | offset | 問題 | EN | 現行 ZH | 建議 ZH |
|---|---|---|---|---|---|---|
| E4-P0-1 | `057_Utomo.json` | 1098 | `@kill（殺好）`語義嚴重錯誤——括號只抓了「kill good」前半，讓「好人」分裂出括號外，讀來成「去@kill（殺好）人」，意思變成「殺好人」 | `'@kill good people with me'` | `去@kill（殺好）人` | `去@kill（殺害）好人` |
| E4-P0-2 | `089_Marney.json` | 1595 | `@killed`缺右括號，且整句閉引號遺失 | `"Yorl gave it back to me after he was @killed.` | `「尤爾在父親@killed被殺後，將它還給了我。` | `「尤爾在父親@killed（被殺）後，將它還給了我。」` |

### P1（建議修，不影響執行但損及品質）

| # | 檔案 | offset | 問題 | EN | 現行 ZH | 建議 ZH |
|---|---|---|---|---|---|---|
| E4-P1-1 | `042_Derydlus.json` | 99 | `@drink`在 EN 作動詞（「have a drink with me」），ZH 展開`（飲品）杯`讀起來語義怪，且飲品+杯重疊 | `Come have a @drink with me!` | `來和吾@drink（飲品）杯！` | `來和吾@drink（飲）一杯！` |
| E4-P1-2 | `042_Derydlus.json` | 536 | `He smiles.`→`他微笑道。`——「道」隱含說話，但此句無對話 | `He smiles.` | `他微笑道。` | `他微微一笑。` |
| E4-P1-3 | `043_Zellivan.json` | 649 | `@tales`直接接`故事`，缺括號（全局 @word+CJK 無括號模式 314 處，此為典型案例，但 Zellivan 是正式貴族角色，格式不一致更明顯） | `The songs and @tales do the heart good` | `@tales故事` | `@tales（故事）` |
| E4-P1-4 | `047_Heftimus.json` | 83 | `doubloon`（西班牙金幣）→「銀幣」，幣種錯誤 | `Spare a doubloon fer an old seahand?` | `老海手能討幾枚銀幣嗎？` | `老海手能討幾枚金幣嗎？` |
| E4-P1-5 | `055_Le'nard.json` | 342 | `@tunics（短）上衣`——括號只含「短」，「上衣」被推到括號外，導致 keyword 展開結果「短上衣」被截開 | `@tunics and @dresses` | `@tunics（短）上衣` | `@tunics（短上衣）` |
| E4-P1-6 | `063_Isabella.json` | 739 | `@sacrifice（奉獻）`——本專案 Sacrifice 美德統一用「犧牲」（見 distilled_sage_book 決議），此處寫「奉獻」不一致；且 off=1052 直接寫「奉獻聖符」 | `the city of @sacrifice` | `@sacrifice（奉獻）之城` | `@sacrifice（犧牲）之城` |
| E4-P1-7 | `070_Dale.json` | 115 | `@Glassblower（玻璃）工匠`——Glassblower 特指「玻璃吹製師」，譯為「玻璃工匠」遺漏職業特色 | `I am Dale the @Glassblower` | `@Glassblower（玻璃）工匠戴爾` | `@Glassblower（玻璃吹製師）戴爾` |
| E4-P1-8 | `076_Whitsaber.json` | 632 | 同一句話同一說話者混用「我」/「吾」：「為我保密，吾便…」 | `If thou wouldst but promise to keep my secret, I'll give thee the map!` | `若汝肯承諾為我保密，吾便將地圖交予汝！` | 統一為`若汝肯承諾為吾保密，吾便將地圖交予汝！` |
| E4-P1-9 | `082_Trenton.json` | 794 | `@rigging`譯為「爬桅杆」語義誤——rigging 指帆索/索具（名詞）而非「爬桅」動作 | `rigging the masts or swabbing the decks` | `@rigging（爬桅）杆或擦甲板` | `@rigging（索具）或擦甲板` |
| E4-P1-10 | `089_Marney.json` | 1737 | 同句混用文言「吾鎮」與現代語「我父親」 | `"I am sorry for our town. You see, my father was the caretaker..."` | `「為吾鎮感到抱歉。汝知道，我父親是符文石的保管人。」` | `「為吾鎮感到抱歉。汝知道，吾父乃符文石的保管人。」` |

---

## C. 名詞一致性 Sweep

### C1. 已確認一致（抽查 20 NPC）

| 術語 | 狀態 |
|---|---|
| 知識寶典 (Codex) | ✅ 全程一致 |
| 魔像族 (Gargoyle) | ✅ 全程一致 |
| 聖壇 (Shrine) | ✅ 全程一致（本批次） |
| 符文 (Rune) | ✅ 全程一致 |
| 真言 (Mantra) | ✅ 全程一致 |
| 吟遊詩人 (Bard) | ✅ 全程一致（045 Stelnar 正確使用） |
| 幽影 (Wisp) | ✅ 045_Stelnar 正確用「幽影」 |
| 靈魂林 (Spiritwood) | ✅ 045_Stelnar 正確 |

### C2. 殘留不一致（本批次新發現）

| 術語 | 問題 | 涉及檔案 |
|---|---|---|
| Sacrifice | `063_Isabella` 用「奉獻」（off=739, 1052），主流為「犧牲」 | 063_Isabella |
| 吾/我 同句混用 | `076_Whitsaber` 至少 4 處同句或連句混用（off=632, 2016）；`082_Trenton` 全檔 26 處「我」混用（含`在下`+`我`模式） | 076, 082 |
| 我/汝 與 吾/汝 混用 | `089_Marney` 用「我/你」基調（現代）但 4 處散落「吾/汝」（文言），造成人物語感漂移 | 089 |

### C3. distilled PDF 新發現未採納項

**distilled_sage_book.md** 對照：

| 術語 | 聖者之書 | 我們現況 | 建議 |
|---|---|---|---|
| Control（三原則之一）| 控制 | 混用：183 用「操控」、200 用「控制」、部分 NPC 用「克制」 | editor3 已列 E3-P1-3，尚未修。v1.5 應統一為「克制」（主流 NPC 用法）|
| Mongbat | 蝙猴 | 魔蝠 | 維持魔蝠（已建立） |
| Reaper | 樹妖 | 收割者樹妖 | 可考慮簡化為「樹妖」 |
| Empath Abbey | 神交修道院 | 共感修道院 | 維持共感修道院 |

**distilled_manual.md** 對照（本批次 063_Isabella 涉及）：

| 術語 | 手冊 | 我們 | 結論 |
|---|---|---|---|
| Sacrifice | 奉獻 | 犧牲 | 維持「犧牲」（主流；但 063 需修） |
| Minoc | 米諾克 | 密諾克 | ⚠️ 手冊用「米諾克」，我們用「密諾克」——兩者並存，063_Isabella 用「密諾克」一致但與手冊有分歧 |

---

## D. v1.5 推薦修法

### 優先級排序

**必修（P0）**

1. `057_Utomo` off=1098：`@kill（殺害）好人`——現行「殺好」讓壞人說話變「殺好人」，與劇情矛盾
2. `089_Marney` off=1595：補全 `@killed（被殺）` 括號並加閉引號

**高優先（P1，影響角色一致性）**

3. `063_Isabella` off=739 & 1052：Sacrifice→犧牲（美德術語統一）
4. `076_Whitsaber` 整檔：統一 吾/我 為「我」（此角色說話帶海盜/市長混合風格，用現代「我」更合適）或全統一為「吾」
5. `082_Trenton` 整檔：整理 吾/我/在下 三分法（市長角色「在下」為主，第一人稱建議統一）
6. `089_Marney` off=1737：`我父親`→`吾父`（與全檔主基調對齊，或反過來把 4 個「吾」改「我」）

**一般（格式清理）**

7. `042_Derydlus` off=99：`@drink（飲）一杯`
8. `042_Derydlus` off=536：`他微笑。`
9. `047_Heftimus` off=83：`銀幣`→`金幣`
10. `055_Le'nard` off=342：`@tunics（短上衣）`
11. `070_Dale` off=115：`@Glassblower（玻璃吹製師）`
12. `082_Trenton` off=794：`@rigging（索具）`

**全局格式 sweep（可批次處理）**

- `@word+CJK無括號`模式共 314 處（20% 無括號）。主要集中在 178_Mole（俺字風格，無括號符合俗語感），但若要統一應加括號。建議以 NPC 為單位逐一決策，而非全局強改。

**前三輪遺留（確認仍未修）**

- E3-P1-1：Valor 美德（044/049/127/160）統一為「勇敢」
- E3-P1-2：Honor（197_Honor 祭壇「榮耀」→「榮譽」）
- E3-P1-3：183_Captain John「操控」→「克制」

---

## E. 整體 Ship-Ready 三判

### 評分維度（各 10 分）

| 維度 | 分數 | 說明 |
|---|---|---|
| 意思準確性 | 8 | 本批 20 NPC 中 2 個 P0 錯誤（Utomo kill、Marney killed），其餘大致準確；doubloon/rigging 等小失誤 |
| 術語一致性 | 7 | 八德術語主體一致；Sacrifice（奉獻/犧牲）、Control（操控/克制/控制）仍有殘留不一致 |
| 文白風格 | 7 | 多數 NPC 各有一致口吻（Heftimus俺、Boskin俺、Marney我、正式 NPC 吾/汝）；但 Whitsaber/Trenton/Marney 有內部漂移 |
| 格式正確性 | 7 | P0 @killed 括號缺失；314 處 @word+CJK 無括號（多數為舊有風格決定而非 bug）；整體尚可 |
| 市場完成度 | 8 | 7298 entries 翻完；主線 NPC 全數覆蓋；edge case（ghost Quenton、外語 Utomo）處理精良 |

### 總分

**37 / 50**

### 三判結論

**Conditionally Ship-Ready（條件式可發布）**

v1.4 可作為 stable release，條件：
- 修 P0 x2（E4-P0-1, E4-P0-2）——約 10 分鐘
- 修 E3-P0-1/2（Gwenno）——已列入前輪待辦

修完 4 個 P0 後可正式 tag **v1.5** 為 production。

P1 共 10 項建議在 v1.5 一起批次處理（預估 1-2 小時），可顯著提升整體分數至 42/50。

術語一致性（Valor/Honor/Control）已反覆被 editor2/3/4 標記，建議在 v1.5 以 Python 批次 patch 一次解決，勿再靠手動逐一修改。

---

## 附錄：重點 NPC 片段引用

（依規定 ≤ 50 字）

> **057_Utomo off=1098 [P0]**
> EN: `'@kill good people with me'` → ZH: `去@kill（殺好）人`
> 括號截斷導致語義反轉，壞人台詞變成「殺好人」指令

> **089_Marney off=1595 [P0]**
> EN: `after he was @killed` → ZH: `父親@killed被殺後`（閉引號遺失）

> **076_Whitsaber off=632 [P1]**
> `若汝肯承諾為我保密，吾便將地圖交予汝！` ——我/吾同句

> **042_Derydlus off=536 [P1]**
> EN: `He smiles.` → ZH: `他微笑道。`——「道」誤加說話語氣

---

*本報告由 editor4 生成，基於對 20 NPC 全文人工比對 + 自動化格式掃描。*
*建議於 v1.5 修完所有 P0（共 4 個：E3-P0-1/2 + E4-P0-1/2）後正式 release。*
