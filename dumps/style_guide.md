# Ultima VI 繁中化譯者風格指南

## 主題基調
Ultima VI 設定為英美中古高度奇幻 (high fantasy) + Lord British 古英文 (Early Modern English: thee/thou/hath/dost/'tis)。
譯文目標：**文白並用**，避免兩種失敗模式：

1. **過度白話**：失去莊重感（"What ho!" 譯成「嗨」會掉風格）
2. **過度文言**：玩家讀不懂（"汝胡能至此" 太古怪，"汝為何在此" 較剛好）

範例對照：
| 原文 | ❌ 太白 | ❌ 太古 | ✅ 採用 |
|---|---|---|---|
| "Welcome, friend." | 嗨，朋友 | 汝來此哉 | 朋友，歡迎你 |
| "Thou art the Avatar?" | 你是阿瓦塔？ | 汝即聖者乎？ | 汝便是聖者？ |
| "I noticed thou didst arrive through a red gateway." | 我看到你從紅色傳送門過來 | 余見汝自赤色幽門入境 | 我注意到汝自紅色之門而來 |

## 人稱代詞
- **NPC 對玩家**：用「汝」（莊重）或「你」（隨意 NPC，例如笑笑、Sherry 等孩童/弄臣）
- **玩家對 NPC**：用「我」
- **Lord British 等高位**：被稱「陛下」「不列顛王」
- **指自身**：「我」（NPC 自我介紹）

## 句尾語氣詞
古英文常用 "thee/thou/'tis"，譯文可加少量「也、哉、乎、矣」點綴：
- "Thanks to thee" → 「賴汝之力也」「全靠了汝」
- "Tis good to see thee" → 「見汝甚悅」（不要「真高興看到你」太現代）

## 名詞統一
所有專有名詞**必須**對照 `glossary.json`。新詞要回寫。

### Lord British 譯名規則（2026-05-21 確立）
- **第一次出現**：用「不列顛王」全稱
- **同一段對話後續**：可用「陛下」做代詞
- **Lord British 自稱**：「朕」（國王語氣）
- **對玩家稱呼**：「卿」「聖者」
- **Iolo/Chuckles 私下戲稱**：「Mr. Nose / 大鼻先生」「His nibs / 那位大人」（弄臣段，幽默感保留）

### 跨 NPC 名詞統一檢核
| 詞 | 標準譯 | 注意 |
|---|---|---|
| Lord British | 不列顛王 / 陛下 | 上述規則 |
| Avatar | 聖者 | 主角 |
| gargoyle | 魔像族（內文）/ 魔像（keyword 短碼）| 玩家輸入「魔像」可 prefix match |
| Britannia | 不列顛尼亞 | |
| Britain | 不列顛城 | |
| Cove | 海灣鎮 | |
| Magincia / New Magincia | 馬精西亞 / 新馬精西亞 | |
| Yew | 尤伊 | 城名，無 you 雙關 |
| Minoc | 米諾克 | 工匠公會所在 |
| Spiritwood | 靈魂林 | |
| Deep Forest | 深林 | Shamino 之家 |
| Lycaeum | 學苑 | Mariah 所在 |

## 保留不譯
| 原始 | 處理 |
|---|---|
| `@keyword` | 不譯字母部分，但譯後也要對應的 keyword section 改成「@中文詞」（如 @virtue → @美德）|
| `$P / $T / $N` | 完全保留 |
| `\nnn` 八進位 escape | 保留（在重編譯時還原）|
| `0xF1 / 0xF3 / 0xF6 / 0xF7 / 0xF8` 控制 byte | 保留（不是 ASCII 文字）|

## 謎語、占卜、雙關語
**必須**寫入 `glossary.json` 的 `riddles` 段，記錄：
- NPC 來源
- 原文
- 譯文
- 解答（如有）
- 翻譯策略（直譯 / 意譯 / 重寫）

雙關語常見：
- The King → 「貓王」（Elvis Presley 致敬，Ultima 系列固定譯法）
- Yew (城名) vs you (人稱)：保留城名「尤伊」，玩家可能會錯失雙關但無妨

## 對話框長度
- **MsgScroll** (8-pixel 行): 寬 17 chars/line, 高 10 lines/page → 中文 12px 約佔 1.5 行高 → 實際可放 ~6-7 行 / 17÷2 ≈ 8 個 CJK 字/行
- **ConverseGump** (NewUI): 寬約 ~25 字元，高約 5 行
- 一段「句子」原則：不超過 30 個 CJK 字。長段拆兩句。

## NPC 個性差異
- **Lord British**：莊重、長者語氣，多用「卿」「諸君」
- **Dupre**：豪邁、軍人腔
- **Iolo**：詩人、藝術家，用詞優雅
- **Shamino**：簡潔、實用
- **Sherry**（會說話的老鼠）：童趣 + 第一人稱「奴家」或乾脆「小弟」
- **Chuckles** (Court Jester)：諧音/順口溜 → 譯時找中文諧音替代
- **Gargoyles**：自稱"we"複數，用「吾族」「我等」
