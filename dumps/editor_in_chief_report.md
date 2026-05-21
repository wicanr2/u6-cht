# Ultima VI 繁中化 — 總編輯校對報告
**日期**：2026-05-21
**參考來源**：
- 《創世紀聖者之書特別版》電腦玩家 1992（以下稱「聖者之書」）p51-83
- 《創世紀 6 遊戲手冊》中文版（以下稱「遊戲手冊」）p1-13
- `/home/anr2/u6-cht/dumps/sage_book_cross_ref.md`（第一輪 p1-50 成果）
- `/home/anr2/u6-cht/dumps/translations/*.json`（全部 206 NPC + BOOK.DAT）
- `/home/anr2/u6-cht/dumps/glossary.json`

---

## A. 譯名一致性新發現

### A1. 聖者之書 p51-83 新出現之權威譯名

#### 職業名（遊戲手冊 p30-34 + 聖者之書 p31-33）

遊戲手冊明確提供 8 種職業的官方中文譯法：

| EN | 遊戲手冊 | 本專案 glossary | 現況 |
|---|---|---|---|
| Fighter | 戰士 | （未列入 glossary） | ⚠️ 需補入 |
| Bard | 吟遊詩人 | 吟遊詩人 | ✅ 一致 |
| Mage | 法師 | 法師 | ✅ 一致 |
| Druid | 德魯伊教徒 | （未列） | ⚠️ 遊戲手冊用「德魯伊教徒」，長達 6 字 |
| Tinker | 工匠 | 工匠 | ✅ 一致 |
| Paladin | 武士 | （未列） | ⚠️ 遊戲手冊譯「武士」；聖者之書 p33 同 |
| Ranger | 流浪者 | （未列） | ⚠️ 遊戲手冊「流浪者」；聖者之書 p33 同 |
| Shepherd | 牧羊人 | （未列） | ⚠️ 遊戲手冊「牧羊人」；聖者之書 p33 同 |

**建議**：glossary.json 的 `concepts` 區塊補入上述職業，NPC 對話中出現 `paladin / ranger / shepherd` 等字時統一採用。

#### 怪物名（聖者之書 p75-80 U6 怪物誌）

聖者之書 p79 明確列出 U6 怪物中文：

| EN | 聖者之書 | 本專案 glossary | 差異 |
|---|---|---|---|
| Acid Slug | 酸液蛞蝓 | （monsters 未列） | 需補 |
| Alligator | 短吻鱷 | （未列） | 需補 |
| Ant, giant | 巨蟻 | （未列） | 需補 |
| Bat, giant | 大蝙蝠 | （未列） | 需補 |
| Corpser | 拖屍怪 | （未列） | 需補 |
| Mongbat | 蝙猴 | **魔蝠** | ⚠️ **不一致** — 聖者之書 p79 圖說「蝙猴」，U6 怪物誌確認 |
| Gazer | 多眼妖 | （未列） | 需補 |
| Headless | 無頭怪 | 無頭怪 | ✅ |
| Reaper | 樹妖 | （未列） | 注意：聖者之書 p80 U6 圖說作「樹妖」（非「死神」）|
| Cyclops | 獨眼巨人 | （未列） | 需補 |
| Slime | 黏怪 | （未列） | 需補 |
| Wisp | 幽靈 → 幻靈 | **幽影** | ⚠️ 聖者之書 p80 「幻靈」；本專案「幽影」——維持幽影較有辨識度 |
| Silver Serpent | 銀蛇 | （未列） | 需補 |
| Tangle Vine | 纏人藤 | （未列） | 需補（LB quiz 題目中出現） |
| Daemon | 惡魔 | 惡魔 | ✅ |
| Drake | 小龍 | （未列） | 需補 |
| Hydra | 九頭龍 | （未列） | 需補 |
| Rotworm | 腐蟲 | （未列） | 需補（LB quiz 題目出現） |

#### 施法材料（聖者之書 p58 + 遊戲手冊 p38-39）

遊戲手冊 p38 和聖者之書 p58 提供完整中文材料名：

| EN / 縮寫 | 遊戲手冊中文 | 本專案現有 | 差異 |
|---|---|---|---|
| Sulfurous Ash (As) | 硫磺灰 | （未在 glossary items 列） | 需補 |
| Garlic (Ga) | 大蒜 | （未列） | 需補 |
| Ginseng (Gi) | 人蔘 | （未列） | 需補 |
| Mandrake Root (Ma) | 曼陀羅根 | （未列） | 需補（游戲手冊 p39：「受陀羅根」，疑印刷錯字；正確應為「曼陀羅根」）|
| Blood Moss (Mo) | 血苔 | （未列） | 需補 |
| Nightshade (Ni) | 龍葵 | （未列） | 需補 |
| Black Pearl (Pe) | 黑珍珠 | （未列） | 需補 |
| Spider's Silk (Si) | 蜘蛛絲 | （未列） | 需補 |

#### 咒語名（遊戲手冊 p59-75）

遊戲手冊提供 8 環全部咒語的中文名，與本專案 glossary 比對：

| EN | 遊戲手冊 | 本專案 | 差異 |
|---|---|---|---|
| Create Food | 製造食物 | （未列） | 需補 |
| Detect Magic | 偵測魔法 | （未列） | 需補 |
| Detect Trap | 偵測陷阱 | （未列） | 需補 |
| Dispel Magic | 解除魔法 | （未列） | 需補 |
| Douse | 熄滅術 | （未列） | 需補 |
| Harm | 傷害術 | （未列） | 需補 |
| Heal | 治療術 | （未列） | 需補 |
| Help | 助力之術 | （未列） | 需補 |
| Ignite | 點燃術 | （未列） | 需補 |
| Infravision | 夜眼術 | （未列） | 需補 |
| Magic Arrow | 魔法箭 | （未列） | 需補 |
| Poison | 毒之術 | （未列） | 需補 |
| Light | 魔法照明 | （未列） | 需補 |
| Dispel Field | 解除力場 | （未列） | 需補 |
| Fireball | 火球術 | （未列） | 需補 |
| Gate Travel | 月門傳送術 | （未列） | 需補 |
| Resurrect | 復活術 | （未列） | 需補 |
| Mass Kill | 群體殺死 | （未列） | 需補 |
| Time Stop | 時間停止 | （未列） | 需補 |
| Tremor | 天崩地裂 | （未列） | 需補 |

**重要發現**：遊戲手冊咒語中文名整體風格與本專案一致（術語簡明），但幾個名稱值得注意：
- **Seance**：遊戲手冊譯「靈魂術」→ 本專案未見，宜採此名
- **Peer**：遊戲手冊譯「靈視術」→ 本專案未見
- **Summon**：遊戲手冊「召喚術」→ 本專案「召喚術」（推測一致）
- **Death Wind**（8 環）：遊戲手冊「死亡之風」→ 可參考

#### 地名補充（遊戲手冊 p21-29）

遊戲手冊 p22-25 對八大城市有固定中文描述，有幾個地名值得對照：

| EN | 遊戲手冊 | 本專案 glossary | 差異 |
|---|---|---|---|
| Isle of the Avatar | 聖者之島 | （未列） | 需補入 |
| Serpent's Hold | 海蛇堡（p29）| 巨蛇堡 | ⚠️ 遊戲手冊作「海蛇堡」，本專案「巨蛇堡」。「Silver Serpent」U6 明確是「銀蛇」非「海蛇」，維持**巨蛇堡**較貼切 |
| Empath Abbey | 天人感應院（p22）| 共感修道院 | ⚠️ 遊戲手冊另一種譯法，本專案「共感修道院」更準確 |
| Lost Hope Bay | 失望灣（p24）| （未列） | 需補「失望灣」 |
| Bloody Plains | 血腥平原（p25）| （未列） | 需補 |

#### 武器名（遊戲手冊 p42-45 + 聖者之書）

| EN | 遊戲手冊 | 本專案 | 差異 |
|---|---|---|---|
| Two-handed Hammer | 雙手大鐵鎚 | （未列）| 需補 |
| Morningstar | 流星鎚 | （未列） | 需補 |
| Mace | 鐵鎚 | （未列） | 需補 |
| Dagger | 七首（匕首）| （未列） | 需補（遊戲手冊 p43 「七首」似為「匕首」排版誤字） |
| Spear | 矛頭（長矛） | （未列） | 需補 |
| Flask of Flaming Oil | 燃燒油（火瓶） | （未列） | 需補 |
| Body Armour | 護甲 | （未列） | 需補 |

---

### A2. 重要概念詞新發現

#### 遊戲手冊 p16 Lord British 給玩家信件

手冊 p16 的 LB 信件提及幾個概念詞：
- 「**美德之殿**」（Shrine of Virtue）→ 本專案「聖壇」✅
- 「**月光之石**」（Moonstone）→ 本專案「月光石」✅
- **「控制、熱情與勤勉」**（Control, Passion, Diligence）→ 本專案「操控、熱情、勤勉」，遊戲手冊用「控制」非「操控」。

⚠️ **建議**：「Control」改譯「控制」（遊戲手冊權威譯法）。目前 183_Captain John.json 用「操控」，需與遊戲手冊統一。

#### 遊戲手冊 p33-36 旅行系統

- 「**月之門**」(Moongate) → 本專案 ✅
- 「**月之石**」→ 本專案「月光石」，遊戲手冊稱「月光之石」，差別不大
- 「**紅色月之門**」（red Moongate）→ 本專案未見固定譯法，Nystul 的「紅色之門」可接受

---

## B. 翻譯品質深度抽查

以下對 12 個 NPC 做 line-by-line literary 審稿。

---

### B1. Lord British（005）★★★★★ 優

**整體**：王者口吻用「朕」，語感莊重。

| 原文 | 現譯 | 評語 |
|---|---|---|
| "the noble ruler of Britannia." | 不列顛尼亞之賢君。 | ✅ 簡練 |
| "'Tis good to see thee again." | 見汝復歸，朕心甚悅。 | ✅ 「甚悅」有古典感 |
| "Much hath happened since thou last departed our realm." | 汝離去後，國中已歷諸多變故。 | ✅ 流暢 |
| "Though 'tis a heavy burden in such @troubled times as these." | 然此亂世，此乃沉重之@擔。 | ⚠️ **P2**：「此乃沉重之擔」稍顯生硬，可改「此擔甚重」；「@擔」作 keyword 顯示形式怪異，建議考慮 @burd 保英文或 @重擔 |
| "We are fortunate indeed that fate hath brought thee here in our hour of need." | 幸有命運將汝帶至此，正當吾國危難之時。 | ✅ |
| "Stay strong in thy commitment to the eight virtues." | 當堅守汝對八大美德之信念。 | ✅ |

---

### B2. Dupre（002）★★★★☆ 良

**整體**：豪邁武夫口吻「兄弟」稱呼，與英文 you 語氣相符。

| 原文 | 現譯 | 評語 |
|---|---|---|
| "a ruggedly handsome man, wearing a gleaming suit of armor." | 一名粗獷英挺的男子，身披一襲閃亮的甲甲。 | ⚠️ **P1**：「甲甲」重字！應為「身披一襲閃亮甲冑」 |
| "'Twas a fine @tournament." | （未見此條，不抽） | — |
| "Wink wink, nudge nudge, say no more..." | 眨眼示意，戳一下肋骨，不必多說…… | ✅ Monty Python 風味保留 |
| "It's Dupre - sounds like dew pray, remember?" | 是杜普雷——聽起來像『朝露之禱』，記得吧？ | ✅ 雙關處理得宜 |

---

### B3. Shamino（003）★★★★☆ 良

| 原文 | 現譯 | 評語 |
|---|---|---|
| "a quiet man, who almost seems to be a creature of the forest." | 一位沉靜之人，宛如森林之生靈。 | ✅ 詩意 |
| "Shamino Salle' Dacil." | 夏米諾薩列。 | ⚠️ **P2**：刪去「達席爾」部分，雖受 byte 限制，但名字截斷感覺突兀。可用「夏米諾薩。」補點號讓其看起來像全名的縮寫 |
| "I help my @friends when they need it." | @friends（朋友）有難時，我便相助。 | ⚠️ **P1**：「@friends（朋友）」的格式在遊戲中顯示為「@friends（朋友）有難時」，括號注釋混在正文裡語感很差。應採「@朋友有難時，我便相助。」並在 keyword section 對應 |

---

### B4. Iolo（004）★★★★☆ 良

| 原文 | 現譯 | 評語 |
|---|---|---|
| "your old friend Iolo." | 汝舊識尤洛是也。 | ✅ |
| "Iolo's the only name I remember having." | 在下記憶所及，唯『尤洛』一名而已。 | ✅ 自稱「在下」恰當 |
| "If you want me to @gather all our gold together..." | 若閣下欲令在下@gather（匯集）眾人之金幣交由閣下攜帶，但說無妨。 | ⚠️ **P2**：「@gather（匯集）」在正文顯示括號注釋，與遊戲風格不符。建議改「若閣下欲令在下@匯集眾人之金幣」（keyword mapping 對應 @gath→@匯集） |

---

### B5. Nystul（006）★★★★★ 優

自稱「老朽」，語感一致，古文歎詞「奇也」有文人氣質。全組優秀。

| 原文 | 現譯 | 評語 |
|---|---|---|
| "She has studied many languages, and perhaps she can decipher this book for thee." | 她通曉諸種語言，或可為汝解讀此書。 | ✅ |
| "Best ask Lord British about it." | 此事最好請教不列顛王。 | ✅ |

---

### B6. Tholden（008）★★★★☆ 良

自稱「老臣」，對應 Chancellor（宰相）身份。

| 原文 | 現譯 | 評語 |
|---|---|---|
| "Records to keep, festivals to plan, I'm so busy..." | 要記帳冊，要籌節慶，老臣忙得很…… | ✅ 有活潑感 |
| "I am Tholden von Bazillius, Chancellor to Lord @British." | 老臣索登·馮·巴齊柳斯，乃@British（不列顛王）顛王之宰相。 | ⚠️ **P0**：「@British（不列顛王）顛王」多了一個「顛王」！應為「乃@British（不列顛王）之宰相」。現在文字在遊戲中會顯示「乃不列顛王顛王之宰相」造成重字 bug |
| "'The @Werecat of the Wine Cellar'..." | 老臣有個綽號叫『@Werecat（酒窖之貓人）之貓人』 | ⚠️ **P0**：同樣問題，「@Werecat（酒窖之貓人）之貓人」會重複。應改「老臣人稱『@酒窖之貓人』」 |

---

### B7. Sherry（009）★★★★★ 優

老鼠擬聲詞、「俺/奴家/大人」三層人稱用得生動一致，是本專案最有趣的 NPC 之一。

| 原文 | 現譯 | 評語 |
|---|---|---|
| "I am Lord @British's friend, @Sherry." | 俺乃@British（不列顛王）顛王的好友@Sherry（雪莉）是也。 | ⚠️ **P0**：同 Tholden 問題，「不列顛王顛王」重字 bug |
| "Dust mice are no friends of mine!" | 塵球可不是俺的朋友! | ✅ 意譯巧妙 |
| "Squeak, squeak, @squeak!" | 吱、吱、@squeak（吱吱）! | ⚠️ **P2**：建議括號改放在句外或改作「吱、吱、@吱吱！」更自然 |
| "Travelling with you is fun!" | 跟大人同遊真有趣! | ✅ |

---

### B8. Chuckles（010）★★★★☆ 良

押韻段精彩，但有幾個括號注釋問題。

| 原文 | 現譯 | 評語 |
|---|---|---|
| "Ho eyo he hum, I've got a @clue!" | 叮叮咚咚噹啷噹，俺有@clue（線索）特意俏！ | ⚠️ **P1**：括號「（線索）」打斷韻律。建議「叮叮咚咚噹啷噹，俺有@線索最緊要！」 |
| "'Cause Dick and Harry both called in sick." | 因為張三李四都告病請假了。 | ✅ 在地化成功（Tom, Dick, Harry → 張三李四）|
| "It said 'ankh ankh!'" | 牠說『鵝是聖者！』 | ⚠️ **P1**：原本 riddles 記錄說「牠說『安克！』」（honk/ankh 雙關），但正文卻改成「鵝是聖者！」，兩者不一致。應統一為「牠說『安克！安克！』」（保留原音）|
| "Search the @chest in @Nystul's room." | 翻翻@chest（寶箱）托房裡那只@Nystul（寶箱）。 | ⚠️ **P0**：quest 關鍵 hint 嚴重混亂！「@Nystul（寶箱）」顯示「尼斯托」但此處顯示「寶箱」且兩個@keyword 譯法矛盾。應改「去翻@尼斯托（Nystul）房裡的@寶箱（chest）。」 |

---

### B9. Gwenneth（016）★★★★☆ 良

弓店店主，語氣恰當。

| 原文 | 現譯 | 評語 |
|---|---|---|
| "'Tis called a boomerang, and it is a most bizarre ranged weapon." | 名曰飛去來器，乃極為奇特之遠程兵器。 | ✅ |
| "Iolo blushes humbly." | 尤洛謙遜地紅了臉。 | ✅ |
| "\"recongize\"（原文拼字錯）" | 「我認得汝！」 | ✅ 正確忽略原文拼字錯誤 |
| "Much demand for bows these days, what with the @gargoyles!" | 如今@gargoyles（魔像族）族肆虐，弓的需求大增！ | ⚠️ **P1**：「@gargoyles（魔像族）族」多「族」字，顯示時成「魔像族族肆虐」 |

---

### B10. Captain John（183）★★★★★ 優

最重要的橋梁 NPC，魔像三原則哲學對話層次清晰。

| 原文 | 現譯 | 評語 |
|---|---|---|
| "I have been here in the catacombs, @studying the @gargoyles." | 數年來我一直身在這地下墓穴，@studying研究@gargoyles魔像。 | ⚠️ **P1**：「@studying研究」是英文 keyword 夾雜中文正文，視覺混亂。建議改「數年來我一直身在地下墓穴，@研究@魔像。」並更新 keyword mapping |
| "And the sum of all the principles is Singularity." | 而所有原則之總和，即為一體性。 | ✅ 「一體性」譯 Singularity 在此語境完全準確 |
| "May thy persistence and precision lead to success." | 願恆毅與精準引領汝走向成功。 | ✅ 魔像告別祝詞，莊重有力 |

---

### B11. Lord British Compendium Quiz（005 batch 3）★★★★★ 優

問題用古文體，答案 keyword 保留英文（copy protection 設計），格式正確。

| 題目 | 現譯 | 評語 |
|---|---|---|
| "What doth trolls lack?" | 山怪缺何物？ | ⚠️ **P1**：Troll 在 glossary 譯「山怪」，但聖者之書 p52 和遊戲手冊 p43 稱「巨人」。建議統一為「山怪」（本專案定義）並確認 quiz 題目顯示正確 |
| "What creature art wisps oft mistaken for?" | 幽影常被人誤認為何種生靈？ | ✅ |
| "How canst one fend off rotworms?" | 如何方能驅退腐蟲？ | ✅ |
| "What art reapers remnants of?" | 死神乃何物之遺存？ | ⚠️ **P1**：Reaper 聖者之書 p76 + p80 圖說「樹妖」，非「死神」。應改「樹妖乃何物之遺存？」 |
| "How doth giant squids crush their prey?" | 巨烏賊以何物壓碎其獵物？ | ⚠️ **P1**：遊戲手冊 p29 稱 Squid 為「大烏賊」，聖者之書 p56 圖說「大烏賊」，本專案現譯「巨烏賊」。建議統一為「大烏賊」 |

---

### B12. 美德聖壇（192_Honesty / 194_Valor）★★★☆☆ 中等

**問題**：`194_Valor.json` 將 Valor 譯為「英勇」，但第一輪 cross-ref 建議改「勇敢」（避免與 Courage 撞名）。此修正尚未落實到 `194_Valor.json`！

| 當前狀態 | 問題 |
|---|---|
| 192_Honesty.json：NPC name「誠實祭壇」，描述「誠實之祭壇」 | ✅ |
| 194_Valor.json：NPC name「英勇祭壇」，「汝對英勇仍有許多須學習之處」 | ⚠️ **P1**：cross-ref 已決議 Valor→勇敢，但 Valor 相關 JSON 未更新 |

---

## C. 對話分支 / Compendium Quiz 校對

### C1. LB Quiz 答案 keyword 一致性

LB batch3 共 9 題 quiz，答案 keyword 全部保留英文（copy protection 設計正確）。
對照遊戲手冊 p44-50 的怪物描述，答案對應檢查：

| 題目 | 答案 keyword | 遊戲手冊 | 狀態 |
|---|---|---|---|
| trolls lack? | `end` | 手冊 p43「巨人……任何工具也碰不了的效果」（即「耐力」endurance？）| ⚠️ 無法直接確認，保留英文合理 |
| tangle vine sleep? | `cent,pod,frag` | 手冊 p56「纏藤……噴出催眠毒霧」（fragment/pod）| ✅ |
| headlesses produced? | `wiza,expe` | 手冊 p48「巫師實驗」→ wizard + experiment | ✅ |
| hydras near? | `nigh,mush` | 手冊 p55「nightshade mushroom」 | ✅ |
| fend off rotworms? | `torc,fire,flam,burn,pass` | 手冊 p50「用火就能把它們趕走」 | ✅ |
| sea serpents attack? | `fire,ball,swip,tail` | 手冊 p50「魔火球或揮掃有力的尾部」 | ✅ |
| wisps mistaken for? | `fire,fly` | 手冊 p57「幻靈」——螢火蟲（firefly）| ✅ |
| squids crush? | `beak` | 手冊 p56「大鳥賊……一嘴就咬成粉碎」| ✅ 鳥嘴=beak |
| silver serpent images? | `tomb,wall,anci,monu` | 手冊 p51「銀蛇……古遺跡牆壁」 | ✅ |

**結論**：Quiz answers 設計合理，keyword 與手冊描述吻合。全數 ✅（除 trolls 1 題無法確認）。

### C2. 魔法咒語構詞對照（遊戲手冊 p40 表格）

遊戲手冊 p40 給出 26 個魔法音節的中文意義，本專案 glossary 有部分收錄：

| 音節 | 遊戲手冊意義 | 本專案 glossary | 差異 |
|---|---|---|---|
| An | Negate/Dispel 反法/解除南 | 未列 | 需補 |
| Bet | Small 微小 | 未列 | 需補 |
| Corp | Death 死亡 | 未列 | 需補 |
| Des | Lower/Down 降低 | 未列 | 需補 |
| Ex | Freedom 釋放 | 未列 | 需補 |
| Flam | Fire 火 | 未列 | 需補 |
| Grav | Energy/Field 能量/力場 | 未列 | 需補 |
| Hur | Wind 風 | 風 (魔法音節) | ✅ |
| In | Make/Create/Cause 製造/產生/引起 | 未列 | 需補 |
| Jux | Danger/Trap/Harm 危險/陷阱/傷 | 危/陷阱/傷 (魔法音節) | ✅ 基本正確 |
| Kal | Summon/Invoke 召喚/傳喚 | 未列 | 需補 |
| Lor | Light 光 | 未列 | 需補 |
| Mani | Life/Healing 生命/治療 | 未列 | 需補 |
| Nox | Poison 毒 | 未列 | 需補 |
| Ort | Magic 魔法 | 法力 (魔法音節) | ⚠️ 遊戲手冊「魔法」，本專案「法力」，意思相近但不一致 |
| Por | Move/Move 移動 | 未列 | 需補 |
| Quas | Illusion 幻像 | 幻 (魔法音節) | ✅ |
| Rel | Change 改變 | 未列 | 需補 |
| Sanct | Protect/Protection 保護 | 未列 | 需補 |
| Tym | Time 時間 | 未列 | 需補 |
| Uus | Raise/Up 升起 | 未列 | 需補 |
| Vas | Great 偉大 | 未列 | 需補 |
| Wis | Know/Knowledge 知道/知識 | 知識 (魔法音節) | ✅ |
| Xen | Creature 怪物 | 怪物 (魔法音節) | ✅ |
| Ylem | Matter 物質 | 物質 (魔法音節) | ✅ |
| Zu | Sleep 睡眠 | 眠 (魔法音節) | ✅ |

**建議**：在 glossary 補齊全部 26 個音節及遊戲手冊對應中文義，方便未來 BOOK.DAT 魔法書文本校閱。

---

## D. P0/P1/P2 修正清單

### P0：必修（lookup miss、嚴重誤譯、會壞 quest）

| # | 檔案 | EN | 當前 zh | 建議 zh | 說明 |
|---|---|---|---|---|---|
| P0-1 | `008_Tholden.json` (offset 156) | "I am Tholden von Bazillius, Chancellor to Lord @British." | 老臣索登·馮·巴齊柳斯，乃@British（不列顛王）顛王之宰相。 | 老臣索登·馮·巴齊柳斯，乃@不列顛王之宰相。 | 「不列顛王顛王」重字 bug（keyword expand 導致） |
| P0-2 | `008_Tholden.json` (offset 217) | "'The @Werecat of the Wine Cellar'..." | 老臣人稱『@Werecat（酒窖之貓人）之貓人』 | 老臣人稱『@酒窖之貓人』 | 括號展開後「貓人之貓人」重字 |
| P0-3 | `009_Sherry.json` (offset 282) | "I am Lord @British's friend, @Sherry." | 俺乃@British（不列顛王）顛王的好友@Sherry（雪莉）是也。 | 俺乃@不列顛王的好友@雪莉是也。 | 「不列顛王顛王」重字 bug，全組同樣問題（offset 1431 同文） |
| P0-4 | `010_Chuckles.json` (offset 1630) | "Search the @chest in @Nystul's room." | 翻翻@chest（寶箱）托房裡那只@Nystul（寶箱）。 | 去翻@尼斯托房裡的@寶箱。 | Quest hint 嚴重混亂：兩個 keyword 的括號說明互相矛盾，且「托」字不知所從 |
| P0-5 | `194_Valor.json` 全組 | Valor (virtue) | 英勇 | **勇敢** | Cross-ref 第一輪已決議但未落實；Valor=勇敢 以與 Courage=勇氣 區分，避免玩家混淆 |
| P0-6 | `005_Lord British_batch3of3.json` (offset 7041) | "What art reapers remnants of?" | 死神乃何物之遺存？ | 樹妖乃何物之遺存？ | Reaper 在本作圖說為「樹妖」非「死神」（聖者之書 p76 怪物誌確認） |

---

### P1：應修（譯名更權威、風格漂移）

| # | 檔案 | EN | 當前 zh | 建議 zh | 說明 |
|---|---|---|---|---|---|
| P1-1 | `002_Dupre.json` (offset 8) | "wearing a gleaming suit of armor." | 身披一襲閃亮的甲甲。 | 身披一襲閃亮甲冑。 | 「甲甲」重字錯誤 |
| P1-2 | `003_Shamino.json` (offset 138) | "I help my @friends when they need it." | @friends（朋友）有難時，我便相助。 | @朋友有難時，我便相助。 | 括號注釋混在正文中，顯示為「@friends（朋友）有難」，語感差 |
| P1-3 | `010_Chuckles.json` (offset 55) | "I've got a @clue!" | 俺有@clue（線索）特意俏！ | 俺有@線索最緊要！ | 括號打斷韻律，且 keyword 應直接譯 |
| P1-4 | `010_Chuckles.json` (offset 2337) | "It said 'ankh ankh!'" | 牠說『鵝是聖者！』 | 牠說『安克！安克！』 | 應與 riddles 記錄一致（honk/ankh 雙關，保音譯） |
| P1-5 | `016_Gwenneth.json` (offset 349) | "what with the @gargoyles!" | @gargoyles（魔像族）族肆虐 | @魔像族肆虐 | 「魔像族族」重字 |
| P1-6 | `016_Gwenneth.json` (offset 1837) | "@gargoyle war" | @gargoyle（魔像）族戰事 | @魔像族戰事 | 同上 |
| P1-7 | `183_Captain John.json` (offset 412) | "@studying the @gargoyles" | @studying研究@gargoyles魔像 | @研究@魔像 | 英文 keyword 直接接中文正文，視覺混亂 |
| P1-8 | `005_Lord British_batch3of3.json` (offset 6709) | "giant squids crush their prey?" | 巨烏賊以何物壓碎其獵物？ | 大烏賊以何物壓碎其獵物？ | 遊戲手冊 + 聖者之書均作「大烏賊」 |
| P1-9 | glossary.json | Control（魔像德目） | 操控 | **控制** | 遊戲手冊 p16 及官方說明書一致用「控制」；Captain John 163 的「操控」宜同步更新 |
| P1-10 | glossary.json monsters | Mongbat | 魔蝠 | 蝙猴 | 聖者之書 p79 + U6 怪物誌圖說明確「蝙猴」 |

---

### P2：可選（語氣優化）

| # | 檔案 | EN | 當前 zh | 建議 zh | 說明 |
|---|---|---|---|---|---|
| P2-1 | `005_Lord British_batch1of3.json` (offset 2103) | "'tis a heavy burden" | 此乃沉重之@擔 | 此@重擔甚沉 | 「之擔」文言略彆扭；@keyword 形式更自然 |
| P2-2 | `003_Shamino.json` (offset 99) | "Shamino Salle' Dacil." | 夏米諾薩列。 | 夏米諾薩列達席。 | 縮短全名但加點尾部以示完整感（如 byte 允許） |
| P2-3 | `009_Sherry.json` (offset 43) | "@squeak!" | @squeak（吱吱）! | @吱吱! | 括號注釋在擬聲詞中更不必要 |
| P2-4 | `004_Iolo.json` (offset 227) | "@gather all our gold" | @gather（匯集）眾人之金幣 | @匯集眾人之金幣 | 括號注釋風格統一，應消除 EN keyword 夾中文正文 |
| P2-5 | `005_Lord British_batch2of3.json` (offset 3881) | "so I can tell her @stories" | 朕便講@故事與她聽 | 朕便說@故事給她聽 | 「講與她聽」文言中「與」字語順稍彆，「說給她聽」更順 |

---

## E. 最終 Ship-Ready 判定

### 整體分數：**40 / 50**

| 項目 | 分數 | 說明 |
|---|---|---|
| 譯名一致性 | 7/10 | Valor 未落實、Mongbat 不一致、重字 bug 4 處 |
| 文學品質 / 語感 | 9/10 | Lord British、Nystul、Captain John 組優秀；Dupre「甲甲」等失誤小 |
| 角色聲音 | 10/10 | 朕/老朽/俺/在下/老臣 分工清晰，無風格漂移 |
| 格式正確性 | 7/10 | @keyword 括號夾中文正文問題系統性存在（P1-2、P1-3、P1-7 等） |
| quest-critical 資訊 | 7/10 | Chuckles quest hint (P0-4) 嚴重混亂需立即修 |

---

### 上線前必做（N = 6 項 P0）

1. **P0-1 + P0-2**：Tholden — 「不列顛王顛王」/「貓人之貓人」重字 bug（影響可讀性）
2. **P0-3**：Sherry（offset 282 + 1431）— 同上 @British expand 重字
3. **P0-4**：Chuckles quest hint — 混亂的 @Nystul + @chest keyword，玩家看到會困惑，quest 關鍵
4. **P0-5**：Valor 全組改「勇敢」— cross-ref 決議未落實，Valor/Courage 混淆傷遊戲完整性
5. **P0-6**：Reaper quiz 題目改「樹妖」— 怪物名不一致傷玩家理解

### 上線後可繼續優化（M = 10+ 項 P1/P2）

- P1 組：Dupre「甲甲」、Gwenneth 重字族、Captain John @keyword 格式、大烏賊統一、Control→控制
- P2 組：Shamino 全名截斷、Sherry 擬聲括號、Iolo @gather 格式、LB「之擔」語順
- glossary 補齊：施法材料、咒語名、職業名、怪物名（建議整批補入，不影響現有 JSON）

### 一句話總結

本專案譯文整體品質扎實、角色聲音分明，核心問題集中在 **@keyword expand 導致的重字 bug**（P0-1 至 P0-3）以及 **Chuckles quest hint 格式混亂**（P0-4），這兩類問題修完即具備上線水準；Valor→勇敢的決議落實後，八德譯名系統完整無缺。

---

*報告由總編輯審稿完成。引用文本均為比對用短片段（≤50字），遵守 IP-safe 原則。*
