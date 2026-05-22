# Credits / 致敬

> 本專案站在前人的肩膀上。沒有以下這些 1990 年代的中文化工作者 + 數位保存者，u6-cht 不可能成立。

---

## 一、《創世紀聖者之書 特別版》(1992)

電腦玩家雜誌 (PC Magazine) 出版的 Ultima VI 中文攻略 + 設定集，
83 頁，是台灣最早的 Ultima 系列中文研究著作。本專案的譯名校對與
文白體例多處參考此書。

| 角色 | 貢獻 |
|---|---|
| **蘇炫榮** | 前言 + 第一章「在創世紀之前」… 各章節撰寫（含 U1-U6 史、製作過程、走訪、Britannia 全境介紹） |
| **高文麟** | 「序」(1992/5/19)，回顧從 Apple II 創世紀III 入坑經驗 |
| **泉英大、施美工** | 恐文字編輯（雜誌打字 / 排版） |
| **黃文鵬** | 美工編輯 |

書版部分被本專案採納的權威譯名：

- **Codex of Ultimate Wisdom** → 知識寶典（取代我們最初的「守則之書」）
- **Reaper** → 樹妖（U6 怪物誌 p76 確認；早於我們最初的「死神」）
- **Squid (giant)** → 大烏賊（取代我們最初的「巨烏賊」）
- 八德 + 三原則架構（Truth/Love/Courage + 8 derived virtues）

文件：DDSC-J-00007-創世紀聖者之書特別版.pdf（83 頁）

---

## 二、《創世紀６ 遊戲手冊》

軟體世界 出版的 Ultima VI 中文版說明書 (13 頁)，包含官方譯法：
- 8 種職業（Fighter 戰士 / Bard 吟遊詩人 / Mage 法師 / 武士 / 流浪者 / 牧羊人 等）
- 26 個魔法音節 (Lingua Magica) 完整對照
- 8 種施法材料 (硫磺灰 / 大蒜 / 人蔘 / 曼陀羅根 / 血苔 / 龍葵 / 黑珍珠 / 蜘蛛絲)
- 8 環咒語完整列表 (從 Create Food 到 Tremor)
- 戰鬥指令 (COMMAND / FRONT / REAR / FLANK / BERSERK / RETREAT / ASSAULT)
- Britannia 8 大美德城市 + 4 個中央區域

文件：DDSC-J-00124-遊戲手冊：創世紀６.pdf (13 頁)

---

## 三、PDF 掃描提供者（匿名）

> *「If I have seen further it is by standing on the shoulders of Giants.」*  
> — Isaac Newton, 1675

某位無名英雄將上述兩份書面文獻**掃描為 PDF**，使得 2026 年的我們得以重訪
1992 年的中文化成果。沒有這次掃描，無論譯名考據、體例研究、書面風格參考都無從談起。

身分目前未考（檔名 DDSC-J 編碼推測為某數位典藏專案；如有讀者知悉，請開 PR 補上）。

**致無名掃描者：感謝您的勞動讓中文化研究得以延續。**

---

## 四、Original Game Authors

Ultima VI: The False Prophet  
© 1990 Origin Systems, Inc.  
Created by **Richard Garriott** (Lord British) and the Origin team.

引擎相容性: ScummVM Nuvie engine (https://www.scummvm.org/) — GPL v3+

---

## 五、字型 Fonts

- **WenQuanYi Zen Hei Sharp** — Apache 2.0, 12px embedded bitmap, v1.0 預設
- **AR PL UMing CN** — Apache 2.0, 11px embedded bitmap, v1.1+ 預設

兩款開源中文字型，使中文化 Big5 渲染成為可能。

---

## 六、Tools & Libraries

- **ScummVM Nuvie engine** — 引擎 + Lua bindings + cutscene framework
- **FreeType** — bitmap font rendering
- **Python + freetype-py** — 字型生成 pipeline
- **Anthropic Claude** — 翻譯 / 審稿 / 工程協同（200+ NPC × 7298 entries）

---

## 七、Project Owner

- **王俊又** (Chun-Yu Wang / wicanr2) <wicanr2@gmail.com> — 小小貢獻者
- GitHub: https://github.com/wicanr2/u6-cht
- 角色：發起本專案、整體架構、Plan B 路線決策、譯文監修、coordinate 多輪 AI 翻譯協同

---

## 引用 / Citation

若您引用本專案，建議格式：

> u6-cht: Ultima VI 繁體中文化 (2026)
> https://github.com/wicanr2/u6-cht
> Based on translation references from 蘇炫榮 et al.,《創世紀聖者之書特別版》(1992) 電腦玩家雜誌
> and《創世紀６ 遊戲手冊》軟體世界.

---

## License

- **Engine patches**: GPL v3+ (繼承 ScummVM)
- **Translation data (translations/, translations_public/)**: CC BY-SA 4.0
- **Font (fonts/big5_u6_12x12.fnt)**: Apache 2.0 (繼承 AR PL UMing)
- **Tools (tools/)**: MIT
- **Documentation (docs/, dumps/, skills/)**: CC BY 4.0
- **Reference PDFs**: 著作權歸原出版社/作者所有，本專案僅作研究比對用
