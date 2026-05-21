---
name: u6-game-tester
description: Ultima VI 繁中化專案 in-game tester 接手 skill。文件描述如何在 Xephyr 無頭環境下啟動 ScummVM Nuvie + 我們的 patched build，逐路徑驗證 Big5 渲染、conv VM 對話、戰鬥訊息、Look 路徑、BOOK.DAT、Compendium quiz 等。參考遊戲手冊 DDSC-J-00124。
metadata:
  type: feedback
---

# Ultima VI 繁中化 — In-Game Tester Skill

**Why**：本專案翻譯實機驗證流程經過 3 次 tester agent 迭代（pass 1 → 3）累積教訓。新 session / agent 接手時讀此檔即可避開所有踩過的坑。

**How to apply**：當被指派 in-game test 任務時讀完本檔；按章節步驟執行。

---

## 1. 環境快速啟動

```bash
# (a) 啟 Xephyr 無頭 X server（若已啟可跳過）
DISPLAY=:2 xdpyinfo > /dev/null 2>&1 || Xephyr -screen 800x600 :2 &
sleep 1

# (b) 啟 ScummVM with 我們的 build
DISPLAY=:2 /home/anr2/u6-cht/scummvm-src/scummvm \
  --extrapath=/home/anr2/u6-cht/scummvm-src/dists/engine-data \
  --debuglevel=1 ultima6 > /tmp/scummvm_test.log 2>&1 &

# (c) 跳過 intro cinematic
sleep 6
DISPLAY=:2 xdotool key Escape; sleep 1
DISPLAY=:2 xdotool key Escape; sleep 1

# (d) Title menu → Journey Onward
DISPLAY=:2 xdotool mousemove 400 500 click 1
sleep 8

# (e) 驗證 CHT loaded
grep "CHT" /tmp/scummvm_test.log
# 應出現：CHT: loaded 7298 entries + 40 fragments from cht_strings.tab (v3, hashed)
```

**檢查清單啟動 PASS 條件**：
- ✅ `CHT: loaded N entries + M fragments (v3, hashed)` log line
- ✅ `WOUFont(cutscene): loaded big5_u6_12x12.fnt — intro CJK enabled`
- ✅ `ConvFont: loaded big5_u6_12x12.fnt — ConverseGump CJK enabled`
- ✅ `U6Font: loaded big5_u6_12x12.fnt — CJK enabled`
- ✅ Screen shows party panel right side（anr2 / Dupre / Shamino / Iolo with 90 HP）

**FAIL 處理**：
- 黑屏 → scummvm 未啟動完成，多 `sleep` 等
- "Could not locate engine data ultima.dat" → 加 `--extrapath=` 指 `dists/engine-data`
- "Game not found" → 確認 scummvm.ini 有 `[ultima6]` section + 正確 `path=`

---

## 2. 截圖與輸入工具

```bash
# 截圖到 /tmp
DISPLAY=:2 ffmpeg -y -f x11grab -video_size 800x600 -i :2 -frames:v 1 /tmp/u6_<num>_<desc>.png

# 用 Claude Read tool 看
Read /tmp/u6_<num>_<desc>.png

# 按鍵 / click
DISPLAY=:2 xdotool key X         # 單一鍵
DISPLAY=:2 xdotool key Up        # 方向鍵
DISPLAY=:2 xdotool key Escape    # esc
DISPLAY=:2 xdotool mousemove X Y click 1
```

**地圖座標 → 像素轉換**：800×600 視窗，map view 約佔左半 (10..380, 10..430)。每 game tile 約 32 px（雙倍縮放 from 16 px）。Click 不一定精準，可能命中 wall / floor，重試幾次。

---

## 3. Game commands（從遊戲手冊 DDSC-J-00124）

| 鍵 | 動作 | 中文 |
|---|---|---|
| A | Attack | 攻擊 |
| B | Combat mode | 戰備 |
| C | Cast | 施法 |
| D | Drop | 放置 |
| G | Get | 拾取 |
| L | Look | 察看 |
| M | Move | 移動 |
| P | Push | 推 |
| R | Rest | 休息 |
| T | Talk | 對話 |
| U | Use | 使用 |
| Y | Yell | 呼喊 |
| F1-F8 | check party member | 查看隊員 |
| F10 | display position | 顯示座標 |
| Ctrl+S | save game | 存檔 |
| Esc | game menu | 遊戲選單 |
| Tab | switch map view | 切換地圖 |
| Space | end turn (combat) | 結束回合 |

戰鬥模式下隊員指令：
- FRONT / REAR / FLANK / BERSERK / RETREAT / ASSAULT / COMMAND

---

## 4. 測試 checklist（依優先級）

### P0 — 必驗，影響 ship-ready
1. **Look 地板** → 「汝見地板」  
   `L` + click empty tile
2. **Look 牆** → 「汝見一面牆」  
   `L` + click wall  
3. **Look party 成員** → portrait + 中文姓名（如 Iolo → 尤洛）  
   `L` + click 黨員頭像（右側 panel）
4. **Talk-nothing!** → 「對話-無對象！」  
   `T` + click empty tile
5. **Game Loaded** → 「存檔已載入」（在 Journey Onward 後自動出現）

### P1 — 應驗，影響大量字串
6. **戰鬥訊息 fragment**：
   - 「Iolo 擦傷」「杜普雷 重度受傷」「夠不著！」  
   - 觸發：戰鬥中（autosave 進入就在戰鬥）
7. **Attack with sword-X**：
   - `A` + click → 「以劍攻擊-地板」「以劍攻擊-階梯」  
8. **多行對話無重疊**：  
   - 兩行中文間應有 2 px gap（不重疊也不過大）
9. **CJK wrap**：  
   - 長中文句應自然換行（每字獨立 token）

### P2 — 進階，需特殊操作
10. **Talk NPC 完整對話**：
    - 需相鄰；可用 hackmove 或 walk
    - LB 對話：觸發 Compendium quiz → 看「(答案: cent / pod / frag)」括號註記
    - 答對 / 答錯 → 中文 反應
11. **Talk party member**：
    - `T` + click party sprite → 「Friends of Nuvie?」中文化  
    - 注意：黨員可能與 Avatar 重疊，click 不易瞄準
12. **Read book / scroll** (BOOK.DAT)：
    - `L` + click 書本 → 中文內文
13. **Compendium quiz 完整 flow**：
    - 8 題 + 答錯 / 答對 都覆蓋

---

## 5. 已知 blocker 與 workaround

### Blocker 1：Avatar 走不到 LB（戰鬥卡住）
**症狀**：autosave 在 throne room 進戰鬥；gargoyle 擋路；走不到 LB。  
**Workaround**：
- A. 攻擊 6-10 輪清完戰鬥
- B. ScummVM cheats menu → Enable hackmove → Shift+drag avatar 至 LB 旁
- C. 用 `tools/teleport.py to-npc 5` 編 OBJLIST（但 ScummVM autosave 會覆蓋 → 須先 quit 再 load）
- D. 不測 Talk LB，改測 party member talk（永遠相鄰）

### Blocker 2：點 NPC 不準（Talk-nothing）
**症狀**：`T` + click 抓不到目標。  
**Workaround**：  
- 多試幾個座標：(145,200), (165,165), (175,140)
- 確認 Avatar 與目標相鄰（隔一格也不行）
- 用 portrait click 代替 map click

### Blocker 3：scummvm crash
**症狀**：某些 OBJ click 觸發 select_obj assertion。  
**Workaround**：自動恢復；重啟即可。重複 crash 才停手。

### Blocker 4：xdotool Shift+drag 被當 Esc
**症狀**：Shift key 開了 game menu。  
**Workaround**：先 `xdotool keydown shift` 再 `mousedown 1` → `mousemove` → `mouseup 1` → `keyup shift`，分別呼叫。

---

## 6. v1.0 已驗證路徑（基準）

每次測試應重新確認以下 baseline 通過：

| Path | Test | 期望 |
|---|---|---|
| `Events::lookAtCursor` ground | `L` + click empty | 「汝見地板」/「一面牆」/「一張地毯」|
| `Events::look(Actor*)` | `L` + click NPC | 「汝見」+ actor 名（黨員=中文）|
| `nscript_print` prefix | `L` + click obj | 「汝見階梯」/「一個寶箱」|
| `MsgScroll::display_string` 中央 hook | 各種 system msg | 「存檔已載入」「對話-無對象！」|
| Verb-Object combo | `A` + click obj | 「以劍攻擊-地板」|
| Combat fragment | 戰鬥 | 「Iolo 擦傷」「夠不著！」|
| ConverseInterpret::do_text | Talk NPC | NPC 中文對話 + 0 `[ctl byte]` 錯誤 |
| Big5 wrap | 長中文 | 每字獨立 token，自然換行 |
| Line height | 多行中文 | 10 px stride，無重疊 |
| 0x5C trail | 含「閱」等字 | 不被誤判 plural marker |

---

## 7. 報告格式

寫到 `/home/anr2/u6-cht/dumps/tester_passN_report.md`：

```markdown
# In-Game Tester Pass N Report

日期：YYYY-MM-DD
版本：scummvm 7298 entries (v3, hashed) / cht_strings.tab MD5: xxx
測試人員：<agent name>

## 環境啟動
- [ ] / [x] CHT loaded
- [ ] / [x] 3 font CJK enabled
- [ ] / [x] Journey Onward 進 game

## P0 路徑（10 項）
| # | Test | Result | Screenshot | Notes |
| 1 | Look ground | PASS | /tmp/u6_p1_01.png | ✓ 汝見地板 |
| ... |

## P1 / P2 路徑

## 發現的 bug
- [bug 1] 描述 + 截圖

## ship-ready 判定
是 / 否 / 條件

## 關鍵 screenshot 列表（≥ 5 張）
- /tmp/u6_pN_XX.png — 描述
```

---

## 8. Ultima VI 知識速查（從遊戲手冊）

### 八德對應城市（quest 必去）
- Honesty 月光城 / Moonglow
- Compassion 不列顛城 / Britain
- Valor 哲倫 / Jhelom
- Justice 紫衫城 / Yew
- Sacrifice 米諾克 / Minoc
- Honor 川辛 / Trinsic
- Spirituality 史卡拉布雷 / Skara Brae
- Humility 新馬精西亞 / New Magincia

### 主要 NPC（測 Talk path 候選）
- Lord British (5) — 不列顛王城堡
- Iolo (4) — 黨員，已加入  
- Dupre (2) — 黨員
- Shamino (3) — 黨員
- Mariah (33) — Lycaeum 學苑法師
- Nystul (6) — 城堡法師
- Geoffrey (7) — 戰士領隊
- Sherry (9) — 會說話的老鼠
- Chuckles (10) — 弄臣

### 魔法八環 + 法力字根（Lingua Magica）
構詞語法：詞根組合成咒語。An = 反義, In = 製造, Mani = 生命, Por = 移動, Vas = 大, Lor = 光 等。
例：In Mani Ylem = Create Food, In Lor = Light, In Mani = Heal

### Compendium quiz 答案（copy protection）

| Q | Acceptable prefix |
|---|---|
| tangle vine doth put one to sleep | `cent / pod / frag` |
| trolls lack | `end` |
| giant squids crush prey | `beak` |
| silver serpent images seen | `tomb / wall / anci / monu` |
| reapers remnants of | `anci / ench / fore` |
| wisps oft mistaken for | `fire / fly` |
| headlesses produced | `wiza / expe` |
| spawning grounds of Hydras | `nigh / mush` |
| fend off rotworms | `torc / fire / flam / burn / pass` |
| sea serpents attack | `fire / ball / swip / tail` |

完整 cheatsheet：`/home/anr2/u6-cht/docs/npc_keywords.md`

---

## 9. 教訓清單（給後人）

1. **Autosave 是 mid-combat 狀態** — 別期待乾淨進場
2. **戰鬥訊息走 Lua actor.lua path** — fragment substitution 已 cover
3. **Look-Actor 與 Look-Obj 是不同 codepath** — 兩條都要測
4. **中文 wrap 從 v1.0 起每字獨立 token** — 不會像 token 過寬溢出
5. **0x5C trail 字（「閱」「許」等）** — get_formatted_text 已跳過 Big5 pair，但翻譯仍盡量避用
6. **`Talk-nothing!` 在戰鬥模式特別容易觸發** — Avatar 一動位置就可能離開 NPC
7. **`?` / `help` magic command 還沒做** — task #未完
8. **可參考前次報告** — `dumps/tester_pass2_report.md`、`dumps/tester_pass3_report.md`

---

## 10. 完工標誌

報告交付後：
- [ ] 截圖 ≥ 5 張，含 1 張 Big5 對話清晰範例
- [ ] tester_passN_report.md 寫好
- [ ] 列出所有 blocker（即使沒 workaround）
- [ ] 一句話 ship-ready 結論
- [ ] 不修改任何 JSON / engine code（純驗證）

不需做（這些是 dev 工作不是 tester）：
- 編譯 engine
- 修譯文
- push 到 GitHub
