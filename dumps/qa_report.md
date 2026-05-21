# Ultima VI 繁中化 QA 報告（第二輪 Sampling）

**日期**：2026-05-21  
**校對員**：QA Bot (claude-sonnet-4-6)  
**覆蓋範圍**：`dumps/translations/*.json`，共 8,638 條譯文  

---

## 1. en 欄位匹配（Check 1）

**結果：31 筆 mismatch（佔 0.36%）**

集中在 2 個 NPC 檔案：原始文本有差異（可能是來源 JSON 版本不同，或 batch 切分後對不上）。

| 檔案 | en 欄位（前 70 字元） |
|------|----------------------|
| 049_Culham | `'"...Sing \'ra,\' my friends, sing \'ra!\'"'` |
| 095_Charlotte | `'"Good $T, $G. How may I help you?"'` |
| 095_Charlotte | `'"Hello again, $G. Welcome back."'` |
| 095_Charlotte | `'"My name is Charlotte. Charlotte Weaver."'` |
| 095_Charlotte | `'"I am a @weaver. It\'s what I do."'` |
| 095_Charlotte | `'"I take @wool and turn it into cloth. It\'s rather simple."'` |
| 095_Charlotte | `'"Honesty forces me to admit that I am the humblest person in New Magen'` |
| 095_Charlotte | `'"I don\'t say it to boast, but simply because it is the truth."'` |
| 095_Charlotte | `'"It is the most humble of occupations, and I am quite good at humility'` |
| 095_Charlotte | `'"I get my @wool from Marissa, who lives in @Paws."'` |
| 095_Charlotte | `'"She also has a brother named @Arbeth. He lives there, too."'` |
| 095_Charlotte | `'"I\'ll also weave @silk thread into cloth, if you have some and want me'` |
| 095_Charlotte | `'"I can\'t help you there."'` |
| 095_Charlotte | `'"What would you like to @buy?"'` |
| 095_Charlotte | `'"I\'ll take that off your hands."'` |
| 095_Charlotte | `'"I\'m sorry, I don\'t have a need for that."'` |
| 096_Dunbar | `'"Welcome to the Humble Palate, friend!"'` |
| 096_Dunbar | `'"Good to see you again, friend!"'` |
| 096_Dunbar | `'"I\'m Dunbar, the innkeeper."'` |
| 096_Dunbar | `'"Serving others is the humblest occupation I could imagine. And I @lov'` |
| 096_Dunbar | `'"I serve @food and @drink to the good people here."'` |
| 096_Dunbar | `'"I can offer you some @fish, @ale, @mead or @wine."'` |
| 096_Dunbar | `'"And some @mutton, of course."'` |
| 096_Dunbar | `'"I get my fish from Conor. He used to be a guild head, you know."'` |
| 096_Dunbar | `'"Strange thing, though. At night sometimes there\'s a glowing light nea'` |
| 096_Dunbar | `'"Don\'t know what to make of it."'` |
| 096_Dunbar | `'"Come back and see me again!"'` |
| 096_Dunbar | `'"I\'m afraid I can\'t help there."'` |
| 096_Dunbar | `'"What would you like to @buy?"'` |
| 096_Dunbar | `'"Here you go. Enjoy your meal!"'` |
| 096_Dunbar | `'"Sorry, I\'m all out of that today."'` |

**原因分析**：`095_Charlotte.json` 與 `096_Dunbar.json` 的 en 值與 `npc_extracted/` 對應 JSON 的 `text` 欄位不一致。可能是翻譯時來源文本做了後處理（去引號、空白標準化），導致 hash 對不上。`049_Culham` 僅 1 筆（特殊字元引號）。

**影響**：這 31 筆在執行時 lookup 表查不到，**不會被替換**，玩家看到英文原文。

---

## 2. Big5 5C trail byte 風險字（Check 2）

**結果：468 條字串含風險字（跨 163 個檔案，佔 8,638 條的 5.4%）**

5C trail byte 風險字清單（本次檢查集合）：`許 功 年 橋 朗 校 縛 笑 敵 聰 暢 演 澳 犁 邏 煩 屋 誣`

### 出現頻率最高的 10 個檔案

| 檔案 | 含風險字條數 |
|------|------------|
| 081_Tobatha.json | 10 |
| 086_Yorl.json | 10 |
| 010_Chuckles.json | 10 |
| BOOK_DAT.json | 10 |
| 089_Marney.json | 9 |
| 056_Andrea.json | 8 |
| 087_Dezana.json | 8 |
| 083_Gideon.json | 7 |
| 109_Timothy.json | 7 |
| 170_Lensmaker.json | 7 |

### 前 30 條樣本

| 風險字 | 檔案 | 譯文（前 50 字） |
|-------|------|----------------|
| 許 | 193_Compassion.json | 「汝對慈悲仍有許多須學習之處。」 |
| 許 | 193_Compassion.json | 「即便最兇猛的野獸，亦不乏些許憐憫之心。」 |
| 煩 | 178_Mole.json | 鼴鼠聽著，有些不耐煩。 |
| 年 | 178_Mole.json | 他是給了我一把鏟子，沒錯——但那是我入行這麼多年見過最劣等的鏟子！ |
| 聰 | 178_Mole.json | 「俺尋思你最好去問個比俺聰明的人。」 |
| 年 | 081_Tobatha.json | 「但汝可叫我@老太太，年輕人。」 |
| 年 | 081_Tobatha.json | 「對我得叫@老太太，年輕人，尊老愛幼！」 |
| 年 | 081_Tobatha.json | 「莫再胡鬧，年輕人，說吧，汝要什麼。」 |
| 年 | 081_Tobatha.json | 「這就是現在的年輕人！一個個都沒禮貌！」 |
| 煩 | 081_Tobatha.json | 「莫拿這種事來煩老身！」 |
| 年 | 081_Tobatha.json | 「汝等年輕人以為什麼都是免費的！」 |
| 年 | 081_Tobatha.json | 「汝這年輕人還算不差。」 |
| 年 | 145_Myles.json | 一個年幼的人類孩童。 |
| 敵 | 016_Gwenneth.json | 「聽士兵說，@魔像族乃強悍敵手。」 |
| 笑 | 016_Gwenneth.json | 她笑了笑。「在尤洛朋友面前，我不便多言他事。」 |
| 年 | 016_Gwenneth.json | 「半年後再來，可能還有一具。」 |
| 年 | 132_Smith.json | 「我們幾年前就把不列顛王從地下世界救出來了！」 |
| 敵 | 132_Smith.json | 「嘿，汝已遇見汝的天敵、汝的末日，他的名字叫史密斯！」 |
| 笑 | 132_Smith.json | 你看見伊歐羅用肘推了推杜普雷的肋骨。「你欠我一杯，」他笑嘻嘻地說。 |
| 笑 | 033_Mariah.json | 雀斑佳人，笑靨迷人。 |
| 許 | 198_Spirituality.json | 「汝對靈性仍有許多須學習之處。」 |
| 笑 | 052_Martin.json | 一位臉色紅潤、笑容可掬的客棧老闆。 |
| 許 | 052_Martin.json | 「唔，或許改天，好嗎？」 |
| 笑 | 107_Hendle.json | 「這讓在下在這個酒館裡有點不受歡迎！」他大笑。 |
| 笑 | 107_Hendle.json | 他大笑，然後繼續說：「不，朋友，晚些來在下的鋪子。」 |
| 笑 | 107_Hendle.json | 亨德爾朝$Y微笑，「那要#1金，有興趣嗎？」 |
| 笑 | 150_Zeke.json | 他向你露出泛黃的牙齒笑著。 |
| 年 | 086_Yorl.json | （須確認） |
| 年 | 089_Marney.json | （須確認） |
| 年 | 056_Andrea.json | （須確認） |

**注意**：此項「風險」不等於一定出錯。5C trail byte 問題取決於 engine 的 Big5 decode 路徑——若 engine 已有 bypass patch，可能不觸發。但若尚未確認 patch 覆蓋完全，這 468 條都是潛在顯示亂碼點。**「年」、「笑」、「許」、「敵」** 出現最頻繁，需優先驗證。

---

## 3. 佔位符遺失（Check 3）

**結果：2 條（佔 0.023%）**

| 檔案 | 遺失 | en | zh |
|------|------|----|----|
| 016_Gwenneth.json | `#7` | `"Will you take #7 gold for that $0, $Y?"` | `「$Y，七金幣換此$0，可乎？」` |
| 016_Gwenneth.json | `#7` | `"Done!" $N hands $Y #7 gold pieces and takes the $0.` | `「成交！」$N付$Y七金幣，取走$0。` |

**分析**：兩條均為購買對話，譯者把 `#7`（動態金額）翻成中文「七金幣」——若 `#7` 是執行時代入的變數金額，這會導致金額永遠顯示「七」而非實際值。若 `#7` 是常數（因商品固定售7金），則無害。**需確認 `#7` 語意**。

---

## 4. @keyword 標記丟失（Check 4）

**結果：3 條（佔 0.035%）**

| 檔案 | 遺失 keyword | en | zh |
|------|-------------|----|----|
| 083_Gideon.json | `@beliefs` | `"She, like her mother, is strong in her @beliefs."` | `「她如其母一般，信念堅定。」` |
| 066_Gwenno.json | `@Stones` | `"Oh, Selganor sent you, did he? I bet you want to learn '@Stones'."` | `「哦，瑟爾嘉諾派汝來的嗎？吾猜汝想學《石頭》。」` |
| 021_Daver.json | `@British` | `"Lord @British gave the runes to the lords of the eight cities."` | `不列顛王便將符文授予八城之領主。` |

**分析**：
- `083_Gideon.json`：`@beliefs` 是 conv trigger keyword。玩家若輸入 "beliefs"，NPC 應有對應回應。丟失此 @ 標記表示觸發條件消失。
- `066_Gwenno.json`：`@Stones` 可能是曲目 keyword。譯者以書名號代替，破壞觸發。
- `021_Daver.json`：`@British` 是 NPC 名稱 trigger。已轉譯為「不列顛王」但無 @ prefix，觸發條件消失。

---

## 5. 名詞漂移（Check 5）

### 5.1 總覽

| 術語 | 標準譯法 | 標準出現次數 | 非標準 | 說明 |
|------|---------|------------|--------|------|
| Lord British | 不列顛王 | 49 | 2（陛下） | 輕微 |
| Avatar | 聖者 | 117 | 0 | 一致 |
| gargoyle/gargoyles | 魔像/魔像族 | 199 | 1 | 幾乎一致 |
| Britannia | 不列顛尼亞 | 44 | 1 | 幾乎一致 |
| Britain（城市） | 不列顛城 | 11 | 4（僅「不列顛」） | 輕微漂移 |
| Codex | 守則之書 | 34 | 5（智典/法典/其他） | **中度漂移** |
| shrine | 聖壇 | 25 | 2（神殿） | 輕微 |

### 5.2 嚴重漂移：Codex

**問題最嚴重**：同一術語 "Codex" 在不同 NPC 有三種不同譯法：

| 譯法 | 使用處 | 條數 |
|------|-------|------|
| 守則之書 | 絕大多數 NPC（033, 030, 165, 166, 169, 168, 174 等）| 34 |
| 智典 | 200_Singularity.json（4條）| 4 |
| 法典 | 141_Sin'Vraal.json（1條）| 1 |

原定標準為「智典」（見 MEMORY.md），但全域實際使用「守則之書」佔壓倒多數。`200_Singularity.json` 雖用「智典」，但其餘 34 條全用「守則之書」，對玩家造成混亂。

### 5.3 輕微漂移細節

**Lord British（非標準）**：
- `006_Nystul.json`：`"the only one I have ever seen is that which Lord British..."` → 「唯陛下手中所持之一枚」（Lord British 被隱去，改以「陛下」代稱）
- `008_Tholden.json`：`"'Twas founded by Lord British."` → 「乃陛下所創立。」

**Britannia（非標準）**：
- `043_Zellivan.json`："I grew up near Castle Britannia." → 「吾是在不列顛城堡附近長大的。」（Castle Britannia 被譯為「不列顛城堡」而非「不列顛尼亞城堡」）

**Britain（無「城」字）**：
- `182_Phoenix.json`：不列顛（缺「城」）
- `184_Daros.json`：@Britain不列顛（缺「城」）
- `147_Sylaina.json`：不列顛（缺「城」）
- `151_Eckhart.json`：不列顛（缺「城」）

**shrine（神殿）**：
- `155_Caradon.json` 2 條將 "Shrine" 譯為「神殿」而非「聖壇」

**gargoyle（非標準）**：
- `164_Beh Lem.json`：1 條因主語為魔像，譯者以「吾族」代替，en 無對應魔像詞但語意正確。

---

## 結論

### 是否可以發布？

**建議：帶條件發布**。非阻斷性問題，但有幾項必修。

### 優先級

#### P0 — 必修（阻斷執行正確性）

| 問題 | 影響 | 行動 |
|------|------|------|
| Check 1：`095_Charlotte`（16筆）+ `096_Dunbar`（14筆）+ `049_Culham`（1筆）en mismatch | 共 31 條在執行時不替換 → 玩家看英文 | 比對 `npc_extracted/` 原始文本，修正 en 欄位空白/引號差異 |
| Check 3：`016_Gwenneth.json` 中 `#7` 被翻為「七」| 若 `#7` 是動態值，金額永遠錯誤 | 確認 `#7` 語意；若是動態值需還原 `#7` |
| Check 4：`083_Gideon.json` @beliefs、`066_Gwenno.json` @Stones、`021_Daver.json` @British 丟失 | 對話 keyword trigger 失效，玩家無法觸發對應對話分支 | 在 zh 中加回 @keyword（中文版或保留英文 @tag） |

#### P1 — 強烈建議修（影響術語一致性）

| 問題 | 影響 | 行動 |
|------|------|------|
| Codex：「守則之書」vs「智典」vs「法典」三分 | 術語不一致，玩家困惑 | 統一為一個譯法（建議全改「智典」或全改「守則之書」）；141_Sin'Vraal「法典」必須改 |
| Britain：4 條缺「城」字 | 讀者可能混淆城市與地名 Britannia | 補「城」字 |
| shrine：2 條「神殿」 | 不一致 | 改為「聖壇」 |

#### P2 — 可下一輪修（低優先）

| 問題 | 影響 | 行動 |
|------|------|------|
| Check 2：468 條 5C trail byte 風險字 | 若 engine patch 未覆蓋，約 5.4% 字串可能顯示亂碼 | 驗證 patch 覆蓋完整性；若有缺口則針對「年/笑/許/敵/煩/聰」高頻字替換同義詞 |
| Lord British：2 條「陛下」代稱 | 輕微，上下文可接受 | 可改也可保留 |
| Britannia：1 條「不列顛城堡」 | 語意可接受 | 低優先 |
| gargoyle：1 條「吾族」代稱 | 語意無誤，上下文特殊（魔像自述）| 可保留 |

---

## 整體錯誤密度

| 類別 | 錯誤數 | 密度（/8,638）|
|------|--------|--------------|
| Check 1 en mismatch | 31 | 0.36% |
| Check 2 5C 風險字（有待確認）| 468 | 5.42% |
| Check 3 placeholder drop | 2 | 0.023% |
| Check 4 @keyword drop | 3 | 0.035% |
| Check 5 名詞漂移（Codex）| 5 | 0.058% |
| **技術錯誤小計（P0+P1）** | **46** | **0.53%** |
| **含 5C 風險總計** | **509** | **5.89%** |

技術錯誤（排除 5C 風險）密度 **0.53%**，屬於可接受範圍。5C trail byte 問題需視 engine patch 狀態決定是否納入必修。
