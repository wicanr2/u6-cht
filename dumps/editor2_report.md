# Ultima VI 繁中化 — 第二輪總編輯深度校對報告（editor2）

**日期**：2026-05-21
**基礎**：distilled_sage_book.md + distilled_manual.md + 第一輪報告 + commit 4176864 後的 translations
**參考架構**：Plan B load-time substitution；引擎在輸出層將 en 整串換成 zh；@ 符號在顯示時被去掉並收集後接英文字母為 clickable keyword（ConverseGump::parse_token）。

---

## A. 第一輪 P0 驗證

| P0 | 說明 | 狀態 |
|---|---|---|
| P0-1 | Tholden @British「不列顛王顛王」重字 | **PASS** — 現為「乃@British（不列顛王）之宰相」，無重字 ✓ |
| P0-2 | Tholden @Werecat「貓人之貓人」重字 | **PASS** — 現為「叫『@Werecat（酒窖之貓人）』」，括號後無重字 ✓ |
| P0-3 | Sherry @British「不列顛王顛王」重字 | **PASS** — 現為「@British（不列顛王）的好友」，無重字 ✓ |
| P0-4 | Chuckles quest hint @Nystul/@chest 互換 | **PASS** — 現為「去翻@Nystul（尼斯托）房裡的@chest（寶箱）」，keyword mapping 正確 ✓ |
| P0-5 | 194_Valor.json「英勇」→「勇敢」 | **FAIL（部分）** — offset=2（「勇敢祭壇」✓）、offset=109（「汝對勇敢」✓）已改，但 offset=8（「英勇之祭壇」）、offset=160（「令人欽佩的英勇」）、offset=429（「覆誦英勇真言」）仍為英勇。共 3 處未修。 |
| P0-6 | Reaper quiz「死神」→「樹妖」 | **PASS** — 現為「樹妖乃何物之遺存？」✓ |

**結論**：6 項 P0 中 4 項完全修復，P0-4 在引擎行為理解後確認修法正確，P0-5 仍有 3 處殘留「英勇」。

---

## B. 第二輪 deep review — 30 個 NPC

> 引擎行為說明（影響評分）：zh 欄位中 `@EN（ZH）ZH` 展開後玩家看到 `EN（ZH）ZH`，ZH 在括號內外各出現一次，構成視覺重字（P0）。`@EN（ZH）` 無後接重複則為 P1（英文顯示，不美但不錯）。`@ZH` 為最佳格式（@ 去掉後純中文）。

| NPC | 分數 | 主要問題 |
|---|---|---|
| 007 Geoffrey | 5/5 | 無問題。武將文言口吻一致，「惜哉，敗羽而歸」文學感佳 |
| 014 Matt | 5/5 | 無問題。啞吧角色處理得當，旁白切換自然 |
| 022 Efram（雜貨商）| 5/5 | @EN（ZH）量少（2 處），不含重字 |
| 026 Tiberius（神官）| 5/5 | 僅 1 處 @EN（ZH），無重字 |
| 028 Arty（啞吧）| 5/5 | 僅描述性 @EN（ZH），無重字 |
| 018 Max（武器商）| 5/5 | @EN（ZH）2 處，無重字 |
| 013 Ariana（學徒）| 4/5 | @bard（吟遊詩人）詩人 — bard 後接「詩人」重字 P0 |
| 023 Rufus（鐵匠）| 4/5 | @Red（紅髮）魯佛 — 格式略怪（P1），其餘流暢 |
| 019 Lazeena（吟遊詩人）| 4/5 | @Artagel（亞塔）格爾 — 名字拆斷（P1），@Dove（白鴿）拉瑟娜 可接受 |
| 033 Mariah | 4/5 | @EN（ZH）5 處（P1），無 P0 重字；口吻「妾身」一致 |
| 034 Thariand | 4/5 | @EN（ZH）5 處（P1），無 P0 重字 |
| 036 Xiao（法師）| 4/5 | @EN（ZH）3 處（P1），文言口吻稍淡，「$T 吉祥」開場可接受 |
| 037 Dargoth（醫者）| 4/5 | 「@cure（治毒）藤皮疹」@EN（ZH）無重字（P1） |
| 038 Rob（酒吧）| 4/5 | 多個飲食 @EN（ZH）無重字（P1），語氣活潑 |
| 029 Lynn（箭矢製作）| 4/5 | @EN（ZH）1 處，無重字，簡潔 |
| 030 Terri（鑄幣）| 3/5 | @pence 便士+@EN（ZH）混搭；語氣OK但格式雜 |
| 031 Kytyn（訓鷹師）| 3/5 | @conservatory（音樂院）院 — 院重複 P0；@EN（ZH）13 處 |
| 032 Maldric（廚子）| 3/5 | @EN（ZH）10 處，有「@roast（烤豬）」→ roast（烤豬）可接受；語氣活潑 |
| 020 Fyodor（紡織）| 3/5 | @EN（ZH）8 處，無重字，但英文 keyword 在正文偏多 |
| 024 Nema（果園）| 3/5 | @EN（ZH）12 處，@daydreaming（白日）夢 — 白日+夢是分開詞，P1 |
| 021 Daver（鐘錶匠）| 3/5 | @EN（ZH）12 處多，@time 時辰（@時辰最佳）；整體內容有趣 |
| 040 Manrel（木工煉金）| 3/5 | @tattooed（符號）前後語意有點斷裂（P1）；多個 @EN（ZH） |
| 035 Ephemerides（天文學）| 3/5 | @EN（ZH）14 處，無 P0 重字但英文 keyword 密集，視覺雜亂 |
| 015 Anya（酒館老板）| 3/5 | @EN（ZH）8 處，無 P0，語氣活潑自然 |
| 025 Cullen（麵包師）| 3/5 | P0：@sell（賣）欲賣 — 賣重複；自稱「卡倫@Baker（麵包）師卡倫」格式奇怪 |
| 011 Kenneth（吟遊詩人）| 2/5 | P0：@Mantra（真言）與真言 — 真言重複；@EN（ZH）8 處；@Kenneth（肯尼）斯名字拆斷 |
| 012 Nan（吟遊詩人）| 2/5 | P0：同 Kenneth，@Mantra（真言）與真言；@EN（ZH）6 處 |
| 017 Peyton（旅店）| 4/5 | P0：@Inn（客棧）客棧 — 客棧重複（1 處）；其餘可接受 |
| 039 Aganar（月光城城主）| 2/5 | P0：@Shrine（聖壇）聖壇 + @Rune（符文）符文 同行兩個重字；@EN（ZH）多 |
| 050 Jerris（吟遊詩人）| 3/5 | P0：@song（歌）的副歌 — 歌重複；敘事風格流暢 |

---

## C. 新發現 P0 / P1

### C1. 新 P0 — 重字 bug（@keyword 展開後視覺重複）

引擎將 @ 去除後，`@EN（ZH）ZH` → `EN（ZH）ZH`，ZH 出現兩次，形成視覺重字。
**共計 21 處確定 P0**（不含第一輪已修的 P0-1 至 P0-6）：

| # | 檔案 | offset | 當前 zh（問題段落）| 建議 zh | 重字 |
|---|---|---|---|---|---|
| N-P0-1 | `004_Iolo.json` | 37 | `@story（故事）故事？` | `@故事？` | 故事×2 |
| N-P0-2 | `004_Iolo.json` | 573 | `@bard（吟遊詩人）詩人` | `@吟遊詩人` | 詩人×2 |
| N-P0-3 | `005_Lord British.json` | 4121 | `《@Hubert（胡伯）胡伯》` | `《@獅子胡伯》` | 胡伯×2 |
| N-P0-4 | `009_Sherry.json` | 406 | `@Hubert（胡伯）胡伯的故事` | `@獅子胡伯的故事` | 胡伯×2 |
| N-P0-5 | `009_Sherry.json` | 1556 | 同上（第二次出現）| 同上 | 胡伯×2 |
| N-P0-6 | `011_Kenneth.json` | 711 | `@Mantra（真言）與真言` | `@真言` | 真言×2 |
| N-P0-7 | `012_Nan.json` | 653 | `@Mantra（真言）與真言` | `@真言` | 真言×2 |
| N-P0-8 | `013_Ariana.json` | 261 | `@bard（吟遊詩人）詩人` | `@吟遊詩人` | 詩人×2 |
| N-P0-9 | `017_Peyton.json` | 138 | `@Inn（客棧）客棧` | `@客棧` | 客棧×2 |
| N-P0-10 | `025_Cullen.json` | 357 | `@sell（賣）欲賣` | `@買…@賣，是否？` | 賣×2 |
| N-P0-11 | `031_Kytyn.json` | 566 | `@conservatory（音樂院）院` | `@音樂院` | 院×2 |
| N-P0-12 | `008_Tholden.json` | 681 | `@Conservatory（音樂院）院` | `@音樂院` | 院×2 |
| N-P0-13 | `039_Aganar.json` | 876 | `@Shrine（聖壇）聖壇`+`@Rune（符文）符文` | `@聖壇`+`@符文` | 聖壇×2，符文×2 |
| N-P0-14 | `050_Jerris.json` | 973 | `@song（歌）的副歌` | `@歌曲的副歌` | 歌×2 |
| N-P0-15 | `058_Nicodemus.json` | 643 | `@book（書）書` | `@魔法書` | 書×2 |
| N-P0-16 | `058_Nicodemus.json` | 803 | `@book（書）書` | `@魔法書` | 書×2 |
| N-P0-17 | `068_Michelle.json` | 243 | `@father（父親）和他父親` | `@父親和他父親`（已是不同詞，可改「吾的@父親，以及他父親」）| 父親×2 |
| N-P0-18 | `081_Tobatha.json` | 291+341 | `@maam（老太）太` | `@老太太` | 太×2（共2處）|
| N-P0-19 | `084_Stivius.json` | 1914 | `@Gargoyles（魔像族）族` | `@魔像族` | 族×2 |
| N-P0-20 | `098_Aurendir.json` | 902 | `@Shrine（聖壇）聖壇` | `@聖壇` | 聖壇×2 |
| N-P0-21 | `099_Patrick.json` | 144+230 | `@bard（吟遊詩人）詩人`+`@conservatory（音樂院）院` | `@吟遊詩人`+`@音樂院` | 詩人×2，院×2 |
| N-P0-22 | `112_Elad.json` | 365 | `@Captain（船長）德船長` | `@船長 Elad` 或 `伊拉德@船長` | 船長×2 |
| N-P0-23 | `112_Elad.json` | 2545 | `@Mantra（真言）真言` | `@真言` | 真言×2 |
| N-P0-24 | `113_Leodon.json` | 220 | `@Captain（船長）頓船長` | `黎奧@船長` | 船長×2 |
| N-P0-25 | `113_Leodon.json` | 2459 | `@Leonna（里歐娜）娜` | `@里歐娜` | 娜×2 |
| N-P0-26 | `115_Budo.json` | 380+1963 | `@lockpicks（撬鎖工具）工具` | `@撬鎖工具` | 工具×2（共2處）|
| N-P0-27 | `127_Ahrmaand.json` | 1790 | `@Mantra（真言）真言` | `@真言` | 真言×2 |
| N-P0-28 | `146_Glen.json` | 2725 | `@gravedigger（掘墓人）人` | `@掘墓人` | 人×2 |

### C2. 新 P0 — 括號語義全錯位

| # | 檔案 | offset | 問題說明 |
|---|---|---|---|
| N-P0-29 | `200_Singularity.json` | 2523 | EN: `@Catacombs of @Control, @Passion and @Diligence` → ZH: `@Catacombs（控制）、@Control（熱情）、@Passion（勤勉）之@Diligence（地）下墓穴` — 四個 keyword 的括號說明全部偏移一位（Catacombs→控制、Control→熱情、Passion→勤勉、Diligence→地？）。**建議改**：`「進入@控制、@熱情、@勤勉三神殿之@地下墓穴。」` |

### C3. P0-5 殘留（Valor 英勇/勇敢混用）

`194_Valor.json` 仍有 3 處「英勇」未改：

| offset | 當前 zh | 建議 zh |
|---|---|---|
| 8 | 英勇之祭壇 | 勇敢之祭壇 |
| 160 | 令人欽佩的英勇 | 令人欽佩的勇敢 |
| 429 | 覆誦英勇真言 | 覆誦勇敢真言 |

### C4. 主要新 P1

| # | 檔案 | 問題 | 建議 |
|---|---|---|---|
| N-P1-1 | `142_Bonn.json` offset=475 | `@trust（信任）任何人` → trust（信任）任何人（「任」字音借，不完全算重字但視覺怪）| `永遠不要@信任任何人` |
| N-P1-2 | `189_Mondain.json` 全組 | Control 譯「操控」（13 處），但 glossary official 為「克制」，200_Singularity 為「控制」，distilled_manual 為「控制」 — 三版本不一致 | 統一改「控制」（遊戲手冊 + distilled_manual 一致）|
| N-P1-3 | `183_Captain John.json` | 同上，「操控」1 處 | 改「控制」|
| N-P1-4 | `004_Iolo.json` offset=37 | `@help（助）` → help（助）— 顯示英文 help 在正文中 | `@幫助` 即可 |

---

## D. 譯名一致性 sweep（distilled 對照）

### D1. 8 種職業

distilled_manual §2 官方：Fighter 戰士、Bard 吟遊詩人、Mage 法師、Tinker 工匠、Paladin 武士、Ranger 流浪者、Druid 德魯伊教徒、Shepherd 牧羊人。

NPC 對話中出現情況：
- **吟遊詩人** ✅ 一致（Kenneth, Nan, Ariana, Jerris, Lazeena 等多處）
- **法師** ✅ 一致（Mariah, Xiao 等）
- **工匠** ✅ 一致（Manrel）
- **牧羊人**：未見明確使用（New Magincia NPC 未抽查）
- **武士（Paladin）**：未見明確使用
- **流浪者（Ranger）**：未見明確使用
- **結論**：職業名在對話中出現次數少，未見明顯錯誤。

### D2. 26 個魔法音節

distilled_manual §3 音節對照：

| 音節 | 手冊義 | glossary | 差異 |
|---|---|---|---|
| Ort | 魔法 | 法力 | ⚠️ 手冊「魔法」，glossary「法力」— 不一致（P2）|
| Hur | 風 | 風 | ✅ |
| Jux | 危險/陷阱/傷 | 危/陷阱/傷 | ✅ 基本正確 |
| Quas | 幻像 | 幻 | ✅ |
| Wis | 知識 | 知識 | ✅ |
| Xen | 怪物 | 怪物 | ✅ |
| Ylem | 物質 | 物質 | ✅ |
| Zu | 睡眠 | 眠 | ✅ |
| 其餘 18 個 | 未補 | 未列 | 建議補全（屬 P2）|

音節未進入 NPC 對話正文，僅在 BOOK.DAT 中出現，對玩家感知影響有限。

### D3. 怪物名

| EN | distilled 表 | translations 實際 | 差異 |
|---|---|---|---|
| Mongbat | 蝙猴 | 魔蝠（glossary）| ⚠️ P1-10（第一輪已列，未修）|
| Reaper | 樹妖 | 已改「樹妖」✅ | 已修 |
| Troll | 巨人（手冊）/ 書版同 | 山怪（本專案 + LB quiz）| 維持山怪（本專案定義）✅ |
| Squid | 大烏賊（手冊）| 巨烏賊（quiz）| ⚠️ P1-8（第一輪已列，未修）|
| Wisp | 幻靈 | 幽影（本專案）| 維持幽影 ✅ |
| Gargoyle | 翼魔（手冊）| 魔像族（本專案）| 維持魔像族（U6 設定族裔）✅ |

### D4. Control 三版本不一致

| 來源 | 譯法 |
|---|---|
| glossary.json concepts | 克制 |
| riddles 答案 | 克制 |
| 200_Singularity.json | 控制 |
| 189_Mondain.json | 操控 |
| 183_Captain John.json | 操控 |
| distilled_manual | 控制 |
| distilled_sage_book | 控制 |

**建議**：統一為「控制」（官方手冊一致）。glossary concepts 的「克制」應更新為「控制」；189_Mondain 和 183_Captain John 的「操控」應改「控制」（13+1 處）。此為 P1。

### D5. 武器名

translations 中武器出現以描述為主，未見明顯與 distilled_manual §7 的衝突。

---

## E. 最終 ship-ready 二判

### 整體分數：**38 / 50**

| 項目 | 分數 | 說明 |
|---|---|---|
| 譯名一致性 | 6/10 | Control 三版本不統一（-1）；Mongbat/Squid 未修（-1）；Valor 英勇殘留（-1）；Conservatory/bard 等重字系統性（-1）|
| 文學品質 / 語感 | 9/10 | Geoffrey「敗羽而歸」、Dupre 已修「閃亮甲冑」、Lord British 等優秀；多數 NPC 角色聲音鮮明 |
| 角色聲音 | 10/10 | 朕/吾/在下/老臣/俺/妾身 各司其職，全程無漂移 |
| 格式正確性 | 6/10 | @EN（ZH）ZH 重字 bug 系統性存在（28 個 P0），影響 30 個以上 NPC；部分已修，但大量未修 |
| quest-critical 資訊 | 7/10 | Chuckles quest hint 已修 ✓；Singularity Catacombs offset=2523 括號全錯位為新 P0 critical |

### 還剩幾項必修才能 ship 1.1

**P0 系統性問題（@EN（ZH）ZH 重字）**：共 28+ 個確定 P0 分佈在 20+ 個檔案，需一次性 fix script 處理。手動一個個改太慢，建議：
1. 寫自動化腳本，把 `@EN（ZH）ZH`（ZH 在括號後重複）改為 `@ZH`
2. 特殊案例（如 @Captain（船長）德船長 → 伊拉德@船長）手動處理約 5 件

**必修優先項（影響遊玩體驗）**：

| 優先 | 項目 | 理由 |
|---|---|---|
| 必修 | @Shrine（聖壇）聖壇、@Mantra（真言）真言、@Inn（客棧）客棧 等系統性重字（約 28 處）| 玩家看到明顯文字重複 |
| 必修 | 200_Singularity offset=2523 括號全錯位 | 重要 quest NPC（Singularity）的方向指示完全錯亂 |
| 必修 | 194_Valor 3 處英勇→勇敢 | P0-5 未完全落實 |
| 建議修 | Control 統一為「控制」（glossary + 189_Mondain + 183_Captain John）| 名詞一致性 |
| 建議修 | Mongbat「魔蝠」→「蝙猴」 | distilled 兩本書均作「蝙猴」|

### 一句話結論

核心內容與角色聲音品質扎實（38/50），但 `@EN（ZH）ZH` 重字 bug 在第二輪 bilingual scan 後仍發現 **28+ 個 P0**（涉及 20+ 個 NPC 檔案），加上 200_Singularity 的 Catacombs 括號全錯位與 194_Valor 英勇殘留，**建議用自動化腳本一次掃除所有 @EN（ZH）ZH 重字模式**，再手修 Singularity + Valor 兩個特殊案例，屆時可達 ship 1.1 標準。

---

*報告由 editor2 完成。引用文本均為 ≤50 字短片段，遵守 IP-safe 原則。*
