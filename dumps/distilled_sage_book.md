# 聖者之書 1992 — Distilled Reference

**來源**：DDSC-J-00007 創世紀聖者之書特別版（電腦玩家雜誌出版，蘇炫榮、高文麟編）
**Total**：83 pages
**Distillation purpose**：給 editor agent 快速查譯名用，省去重讀 PDF 時間
**IP-safe**：均為 ≤ 20 字短譯名表，無長段引用

---

## 1. 整體風格

書版採「**英文專有名詞保留 + 概念詞中譯**」路線：
- Lord British 不譯（我們：不列顛王）
- Iolo / Dupre / Shamino / Mondain 等保英文
- 城市名 Britain / Britannia / Trinsic / Yew 等用英文，內文偶有中譯
- 八德、概念詞、怪物名、咒語、職業全中譯

---

## 2. 八德對照（書版 vs 我們）

| EN | 書版 | 我們 v1.0 | 決議 |
|---|---|---|---|
| Honesty | 誠實 | 誠實 | ✅ 一致 |
| Compassion | 同情 | 慈悲 | 維持慈悲 |
| Valor | 勇敢 | 勇氣 → **勇敢** | ⚠️ 第一輪 cross-ref 已決議改、未落實到 194_Valor.json |
| Justice | 正義 | 正義 | ✅ |
| Sacrifice | 犧牲 | 犧牲 | ✅ |
| Honor | 榮譽 | 榮譽 | ✅ |
| Spirituality | 心靈 / 心靈力量 | 靈性 | 維持靈性 |
| Humility | 謙虛 | 謙卑 | 維持謙卑 |
| Pride (anti-virtue) | 驕傲 | 驕傲 | ✅ |

**三原則**：Truth → 真理、Love → 愛、Courage → 勇氣

---

## 3. 概念詞

| EN | 書版 | 我們 | 決議 |
|---|---|---|---|
| Codex of Ultimate Wisdom | **知識寶典** | 守則之書 → **知識寶典** | ✅ 已採納（commit 6db84ca）|
| Avatar | 聖者 | 聖者 | ✅ |
| Gargoyle | 翼魔 | 魔像族 | 維持魔像族（U6 揭露為種族）|
| False Prophet | 錯誤的預言（書註虛偽先知）| 假先知 | 維持 |
| Underworld | 地底世界 | 地底世界 | ✅ |
| Stygian Abyss | 冥河深淵 | 冥河深淵 | ✅ |
| Ankh | Ankh（或 護身符）| 安卡 | 我們更明確 |
| Way of the Avatar | 聖者之道 | 聖者之道 | ✅ |
| Shrine | 神壇 | 聖壇 | 維持聖壇 |
| Rune | 標記 | 符文 | 維持符文 |
| Mantra | 真言 / 祈禱詞 | 真言 | ✅ |
| Tower of Knowledge | 知識之塔 | 知識之塔 | ✅ |

---

## 4. 八大城市 + 對應美德

| EN | 中譯 | 美德 | 真言 |
|---|---|---|---|
| Moonglow | 月光城 | Honesty | ahm |
| Britain | 不列顛 / 不列顛城 | Compassion | mu |
| Jhelom | 哲倫 / 捷倫城 | Valor | ra |
| Yew | 紫衫 / 紫衫城 | Justice | beh |
| Minoc | 米諾克 | Sacrifice | cah |
| Trinsic | 川辛 / 特林西 | Honor | summ |
| Skara Brae | 史卡拉布雷 / 史卡拉雷 | Spirituality | om |
| New Magincia | 新馬精西亞 / 新美吉西亞 | Humility | lum |

---

## 5. U6 怪物誌（聖者之書 p46-57 + 75-80）

| EN | 書版 | 我們 |
|---|---|---|
| Acid Slug | 酸液蛞蝓 | （未列）|
| Alligator | 短吻鱷 | （未列）|
| Ant, giant | 巨蟻 | （未列）|
| Bat, giant | 大蝙蝠 | （未列）|
| Corpser | 拖屍怪 | （未列）|
| Mongbat | **蝙猴** | 魔蝠 ⚠️ |
| Gazer | 多眼妖 | （未列）|
| Headless | 無頭怪 | 無頭怪 ✅ |
| Reaper | **樹妖** | 收割者樹妖 ⚠️（quiz 題目用「死神」需改）|
| Cyclops | 獨眼巨人 | （未列）|
| Slime | 黏怪 | 黏液怪 |
| Wisp | 幻靈 | 幽影（維持）|
| Silver Serpent | 銀蛇 | 銀蛇 |
| Tangle Vine | 纏人藤 | 纏人藤 |
| Daemon | 惡魔 | 惡魔 ✅ |
| Drake | 小龍 | 小龍 |
| Dragon | 龍 / 巨龍 | 巨龍 |
| Hydra | 九頭龍 | 九頭龍 |
| Rotworm | 腐蟲 | 腐蟲 |
| Troll | 巨人 | 山怪 |
| Squid (giant) | 大烏賊 | 巨烏賊 ⚠️ |
| Sea Serpent | 海蛇 | 海蛇 |
| Cat | 貓 | 貓 |
| Cow | 牛 | 牛 |
| Sheep | 綿羊 | 綿羊 |

---

## 6. 主要 NPC（書版保英文，這裡列我們中譯）

| EN | 我們 |
|---|---|
| Lord British | 不列顛王 |
| Iolo | 尤洛 |
| Dupre | 杜普雷 |
| Shamino | 夏米諾 |
| Mariah | 瑪萊雅 |
| Nystul | 尼斯托 |
| Geoffrey | 傑佛瑞 |
| Sherry | 雪莉 |
| Chuckles | 笑笑 |
| Linda | 琳達 |
| Lord Blackthorn | 布雷克松領主 |
| Mondain (Ultima I villain) | 蒙丹 |
| Minax (Ultima II villain) | 米娜克斯 |
| Exodus (Ultima III villain) | 米索 |

---

## 7. 魔像族三原則（U6 反向虛擬美德）

| EN | 我們 | 注 |
|---|---|---|
| Control | **控制** | 遊戲手冊 p16 也用控制；我們 v1.0 用「操控」⚠️ |
| Passion | 熱情 | ✅ |
| Diligence | 勤勉 | ✅ |
| Singularity | 獨一 / 一體性 | ✅（NPC 200）|

---

## 8. P51-83 章節骨架（攻略地圖 + 怪物誌）

- p51-58 各種生物簡介（U6 怪物誌）
- p59-75 八環魔法咒語完整列表
- p76-83 U4/U5 attack 攻略地圖

→ 對譯文校正幫助主要在 monster names + spell names。
