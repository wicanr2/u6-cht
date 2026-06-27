# U6-CHT 實機 game-tester onboarding

任何 sub-agent 接到「實機驗證 u6-cht 中文化」任務前，先讀這一份。
萃取自 `dumps/tester_pass{2,3,4,5,6}_report.md` 五輪實機紀錄 + `skills/u6-cht.md` engine hook 知識。

> 配套：`skills/u6-cht.md` (技術全景)、global skill `retro-game-playtest` (老遊戲實機驗證方法論)。

---

## 30 秒摘要 (BLUF)

驗 u6-cht 中文化 = 啟動 patched ScummVM **配 `--save-slot=2`** → 直接進 throne room → 截圖 + 看 stderr `CHT-LOOK *` debug。

**最小一行 launch**（已實機驗 2026-06-27）：

```bash
DISPLAY=:99 /home/anr2/u6-cht/scummvm-src/scummvm \
  --auto-detect --path=/home/anr2/u6-cht/working/game \
  --no-fullscreen -d 1 --save-slot=2 ultima6 \
  > /tmp/u6_run.log 2>&1 &
```

**`--save-slot=2` 才跳過 intro cinematic**。沒帶 `--save-slot` 雖然 `scummvm.ini` 有 `loadgame=ultima6, latest_save=2`，ScummVM 仍會先 play intro。

13 秒後視窗顯示 throne room（Avatar 跟 LB / Dupre / Shamino / Iolo 圍王座），可直接驗 LB 對話與旁邊物件 Look/Use。
要驗第一場戰役有三條路：(A) intro 最後段 gargoyle ambush（不帶 `--save-slot` 跑 intro，按 SPACE 推進到底會觸發），(B) 走出王宮去野外 spawn 怪，(C) 純驗 combat mode 切換鍵（`B` 切 `>進入戰鬥！`，不必真打）。

---

## 1. 環境準備

### 1.1 binary 與資料

| 項 | 路徑 |
|---|---|
| ScummVM binary | `/home/anr2/u6-cht/scummvm-src/scummvm`（已 patched，137 MB） |
| Game dir | `/home/anr2/u6-cht/working/game/`（含 cht_strings.tab + big5_u6_12x12.fnt + SAVEGAME/）|
| autosave | `working/game/SAVEGAME/`（已存在，throne room 狀態） |
| ScummVM config | `~/.config/scummvm/scummvm.ini`（target = `ultima6`，cheats/enabled=yes、hackmove=yes、loadgame=ultima6）|

### 1.2 工具鏈

`Xvfb`、`Xephyr`、`xdotool`、`ffmpeg`、`import`（ImageMagick）都已裝。`wmctrl` 也可用。

### 1.3 兩種 headless display 選一

| 選項 | 命令 | 適用 |
|---|---|---|
| Xvfb | `Xvfb :99 -screen 0 800x600x24 &; DISPLAY=:99 ...` | 全自動截圖（pass4+ 用） |
| Xephyr | `Xephyr -screen 800x600 :2 &; DISPLAY=:2 ...` | 需要人眼看的 debug（pass2/3 用） |
| dummy | `SDL_VIDEODRIVER=dummy` | **無法**走 GUI（會卡在主選單）、僅可驗 log line |

**雷**：`SDL_VIDEODRIVER=dummy` 不會 paint 視窗，沒有 cursor / mouse click → 進不了主選單以後的任何畫面。只用於 5 秒 sanity「看 CHT loaded log」。要實機操作必須 Xvfb / Xephyr。

### 1.4 ScummVM 啟動 flag 清單

| flag | 用途 |
|---|---|
| `--auto-detect --path=<dir>` | 自動偵測 u6 |
| `--no-fullscreen` | 窗化（Xvfb 比較好截）|
| `-d 1` 或 `--debuglevel=1` | 開 debug level 1（**會印 `CHT-LOOK actor-look:` / `CHT-LOOK ground:` / `CHT-MISS:`**）|
| `--save-slot=0` | 直接從 slot 0 載入 autosave（跳過主選單）|
| `ultima6` | game target（也可用 `--auto-detect` 不指定）|

**注意**：`-d 1` 觸發 ScummVM 自己的 verbose log 很吵，但 `CHT-LOOK` / `CHT-MISS` / `CHT: loaded` 等專案 debug 都在 `-d 1` 才會印。

---

## 2. 進到遊戲的正確序列

### 2.1 「跳 intro 直接進 throne room」最快路徑

**`--save-slot=2`** — 唯一可靠跳 intro 直接 load slot 2 (throne room autosave) 的方式。
不帶這 flag 即使 `scummvm.ini` 有 `loadgame=ultima6, latest_save=2`，scummvm 仍會先跑 intro cinematic。

**實機驗證**（2026-06-27 P3）：
- 不帶 `--save-slot`：13s 截圖是 intro 第一段「汝之世界已歷五載春秋」（Avatar 在地球家）
- 帶 `--save-slot=2`：13s 截圖直接是 throne room（黨員列表「anr2 / 杜普雷 / 夏米諾 / 尤洛」+ 「存檔已載入」）

### 2.2 主選單按鍵

| 動作 | 鍵 |
|---|---|
| Journey Onward（載 autosave）| Return（預設選項）|
| Begin a New Game | ↓ × N 後 Return |
| Cinematic Intro | ↓ × N 後 Return |

### 2.3 intro 推進（**重要雷**）

intro caption 採 **按鍵推進**（`intro.lua` 內 `while input == nil do ... end`），**不是 timer**。
pass4 早期誤以為時間驅動，等候 > 8 分鐘第一字幕仍卡 — 按 Space 才推進。

每段 caption 出來後按 **Space**（或 Return）切下一段。**ESC 可整段 skip**。

完整 intro caption 序列（驗 #4 用）：
1. Upon your world, five seasons... → 汝之世界已歷五載春秋
2. You have traded the Avatar's life... → 汝以聖者之凶險...螢光中之超人...
3. Outside, a chill wind rises... → 屋外，寒風漸起……
4. Tongues of lightning lash the sky... → 閃電之舌鞭笞長空…
5. ...and in moments, the storm is upon you. → ……片刻間，風暴已臨。
6. In a cataclysm of sound and light, a bolt of searing blue fire... → 一聲雷光交響之間，一道熾烈藍火擊中大地！
7. Lightning among the stones! → 石陣之中閃電起！
8. Near the stones, the smell of damp... → 近石陣處，潮濕焦土之氣息瀰漫…
9. ...and from the heart of the stones, a softly glowing door ascends... → ……自石陣之心，一道微光柔現之門悄然升起！
10. by Lord British to banish the tyrant Blackthorn! → 不列顛王擲下以放逐暴君布雷克松！
11. Gargoyles surround you! → 魔像族將汝團團圍住！（**最後段帶 Gargoyle ambush，會直接進到戰鬥**）

---

## 3. 鍵盤操作完整對照

**U6 設計上「全鍵盤可玩」**（1990 DOS 原版），鍵盤 + numpad 八方向 + 命令鍵 + F1-F10 + Ctrl-* 涵蓋所有操作。
ScummVM Nuvie 完整繼承這套 binding。

> 來源：① 1992 軟體世界《創世紀６ 遊戲手冊》p8-11「遊戲控制」（**權威**）；
> ② `scummvm-src/devtools/create_ultima/files/ultima6/defaultkeys.txt`（**Nuvie 實裝**）；
> ③ 本專案實機驗證（2026-06-27）。

### 3.1 命令指令（Command Bar）

對應原版手冊 p8「圖形指令」順序：A T C L G M U B R（attack / talk / cast / look / get / move / use / combat / rest）

| 鍵 | 命令 | 中文化後 prompt | 後續動作 |
|---|---|---|---|
| **A** | Attack | `以劍攻擊-什麼？` | combat mode 內、選 target |
| **T** | Talk | `對話-無對象！` / `對話-...` | 滑鼠點 NPC 或 8 方向鍵選相鄰 |
| **C** | Cast spell | `施法-...` | 拼 Lingua Magica 音節（如 `In Mani`）|
| **L** | Look | `察看-...` | 滑鼠 click target / 8 方向鍵選相鄰 / 直接 Return 看 Avatar 自己 |
| **G** | Get | `取得-...` | 8 方向鍵選相鄰地上物 |
| **M** | Move | `移動-...` | （cheat hackmove）拖 NPC / 推物件 |
| **U** | Use | `使用-...` | 滑鼠 click 物件 |
| **B** | Toggle Combat | `>進入戰鬥！` / `>脫離戰鬥！` | 切換隊伍 combat mode |
| **R** | Rest | （野外露營，9 小時補血）| 需在野外 |

> ⚠️ **手冊 vs Nuvie 差異**：原版手冊寫 `B` 是切戰鬥（Battle），但 Nuvie defaultkeys.txt 把 `b` 也綁 `toggle_combat`（相同效果），多了 `Alt-b` 走 command bar 第 9 格。

### 3.2 移動（八方向）— 手冊 p11「移動方法」

```
  KP_7  KP_8  KP_9       ↖   ↑   ↗
  KP_4   ·   KP_6        ←   ·   →
  KP_1  KP_2  KP_3       ↙   ↓   ↘
```

| 鍵 | 方向 | Nuvie action |
|---|---|---|
| KP_8 / ↑ | 北 | walk_north |
| KP_2 / ↓ | 南 | walk_south |
| KP_4 / ← | 西 | walk_west |
| KP_6 / → | 東 | walk_east |
| KP_7 / KP_9 / KP_1 / KP_3 | 西北 / 東北 / 西南 / 東南 | walk_*diagonal* |

**滑鼠移動**：在 map view 上按住左鍵往欲移方向，Avatar 一直走到鬆手或撞牆。

### 3.3 角色 / 隊伍

| 鍵 | 動作 | 備註 |
|---|---|---|
| **F1-F8** | 看隊員 1-8 inventory（doll gump）| F1=Avatar、F2=#2…|
| **Alt-F1-F8** | 同上 doll gump（另一條 binding）| |
| **F10** / `/` / `KP/` | party_view（顯示隊伍位置 map）| |
| **1-9** | solo_mode #N（指定隊員獨自行動）| |
| **0** | party_mode（恢復隊伍一起走）| |
| **Ctrl-1..Ctrl-9** | show_stats #N（基本資料：力 / 敏 / 智 / 法 / 體 / 等 / 經）| 手冊 `*` 鍵 = 基本資料 |
| `=` / `Shift-=` / `KP+` | 切換下一個隊員 | |
| `-` / `KP-` | 上一個隊員 | |

### 3.4 系統 / 存檔

| 鍵 | 動作 | 中文化後 |
|---|---|---|
| **S** | save_menu | 存檔選單 |
| **Ctrl-S** | toggle_sfx（**注意**：不是手冊的「存進度」— Nuvie 改成切音效）| |
| **Ctrl-L** / **Ctrl-R** | load_latest_save | 載最近存檔 |
| **Ctrl-Q** / **Q** / **Alt-X** | quit | 出現「儲存後離開」對話框 |
| **Alt-Q** | quit_no_dialog | 直接退出（**危險，不存檔**）|
| **Esc** | game_menu_dialog | 取消當前指令 / 喚出主選單 |
| **Space** | cancel_action | intro / 對話框「下一頁」推進 |
| **Enter** / **KP_Enter** | do_action | 確認 / 「下一個」|
| **Tab** | toggle_cursor | 更換遊戲移動區域（手冊原意）|

> ⚠️ **手冊 vs Nuvie 重大差異**：
> - 原版 `Ctrl-S` 是「存進度」、`Ctrl-P` 是「叫進度」、`Ctrl-Q`/`Alt-E` 是「返回 DOS」。
> - Nuvie 把 `Ctrl-S` 改成「切音效」，存檔改 `S` 鍵 + save_menu UI。**若按 Ctrl-S 期望存檔會誤關音效**。

### 3.5 訊息 / 視圖

| 鍵 | 動作 |
|---|---|
| **Z** | close_gumps（關所有開著的視窗）|
| **I** | doll_gump（循環切換隊員 doll 視圖）|
| **H** | show_keys（**叫出 in-game 完整 keymap help**，最權威）|
| **PageUp** / **PageDown** | msg_scroll_up / msg_scroll_down |
| **Home** / **End** | （特殊行為，主要用於 dialog input）|
| `;` | multi_use（連續使用同物件）|
| `,` | new_command_bar |
| `.` | toggle_original_style_command_bar |
| `` ` `` | toggle_combat_strategy（COMMAND / FRONT / REAR / FLANK / BERSERK / RETREAT / ASSAULT）|

### 3.6 Cheat / Debug（scummvm.ini cheats/enabled=yes 才有效）

| 鍵 | 動作 |
|---|---|
| **Ctrl-C** | toggle_cheats（總開關，已預設 on）|
| **Alt-Ctrl-G** | toggle_god_mode |
| **Alt-H** | toggle_hackmove（移動可穿牆，已預設 on）|
| **Alt-Ctrl-H** | heal_party |
| **E** | show_eggs（顯示 spawn egg 位置）|
| **Alt-E** | toggle_ethereal |
| **Alt-Ctrl-E** | toggle_egg_spawn |
| **Alt-I** | toggle_no_darkness |
| **Alt-Ctrl-P** | toggle_pickpocket_mode |
| **Ctrl-T** | **teleport_to_cursor**（**重要 game-tester 工具**：移 cursor 到目標位置 + Ctrl-T，Avatar 瞬移過去；解 OBJLIST teleport 跟 autosave 衝突的痛點）|
| **X** | toggle_x_ray |
| **Ctrl-A / Ctrl-M / Ctrl-S** | toggle_audio / music / sfx |
| **Ctrl-D / Ctrl-I** | decrease_debug / increase_debug（執行時調 ScummVM debug level）|
| **Ctrl-F** | toggle_fps_display |

### 3.7 game-tester 端 xdotool 整理

| 期望動作 | xdotool 寫法 | 已驗 work? |
|---|---|---|
| 找 ScummVM 視窗 id | `WID=$(DISPLAY=:99 xdotool search 'scummvm' \| head -1)` | ✅ (case-insensitive class match) |
| 送單一鍵 | `DISPLAY=:99 xdotool key --window $WID l` | ✅ (L+Return 印 `CHT-LOOK party-name: anr2`) |
| 送方向鍵 | `xdotool key --window $WID KP_6` | ✅（手冊 p11 numpad 八方向） |
| Look + 確認看自己 | `xdotool key l; xdotool key Return` | ✅ |
| 滑鼠 click target | `xdotool mousemove $x $y; xdotool click --window $WID 1` | ✅（scummvm.ini `look_on_left_click=yes` 直接 click 就 Look，不必先按 L）|
| 截圖 | `DISPLAY=:99 import -window $WID /tmp/XX.png` | ✅ |

**⚠️ xdotool `--sync` 雷**：`xdotool search --sync --name 'X'` 找不到視窗會**無限等**，2 分鐘 timeout 才回。
**永遠用沒 `--sync` 的版本**，找不到立刻 fail 比較好 debug。

**⚠️ wine 不 work**：xdotool 對 Wine 下 SDL app 的 event injection 不穩，**game-tester 一律用 native Linux scummvm binary + Xvfb**。

---

## 4. 跟 LB 對話（issue #1.3 debug 路徑）

### 4.1 從 autosave 走過去

autosave (slot 2) 已在 throne room，OBJLIST 顯示 Avatar=(306,348)、LB=(307,348) — **LB 在 Avatar 東邊 1 格**（不是北邊）。

**最簡單**：用 cheat `Ctrl-T` (teleport_to_cursor) — 移 mouse cursor 到 LB sprite + Ctrl-T，Avatar 瞬移到 cursor 位置。**這條繞過 OBJLIST/autosave 衝突的痛點**，不必動 SAVEGAME 檔。

如果 cheat 沒開或 `Ctrl-T` 失靈，退而求其次：

```bash
# LB = NPC id 5 (見 tools/teleport.py NPC_NAMES)
python3 tools/teleport.py to-npc 5
# 然後重啟 scummvm → 帶 --save-slot=2 載入
```

⚠️ 雷（README task #21）：autosave 跟 OBJLIST 衝突 — teleport 寫 OBJLIST、但 ScummVM autosave 有自己座標記錄，可能用 autosave 蓋過 teleport。**做完 teleport 後可能要刪 autosave 才生效**。

### 4.2 觸發對話

1. 按 `T`
2. 滑鼠 click LB sprite（或 KP_8 把 cursor 移到 LB 方向）
3. 觸發 LB 對話框，**stderr 同時印 `CHT-LOOK actor-look: <真實 aname>`**（events.cpp:1104）

### 4.3 抓 issue #1.3 真實字串

```bash
grep -E 'CHT-LOOK actor-look|CHT-MISS' /tmp/u6_run.log
```

期待輸出（pass5/6 觀察）類似：
```
CHT-LOOK actor-look: the noble ruler of Britannia
CHT-LOOK actor-look: the noble ruler of the British
```
（**真實字串需要自己抓**，issue 報的 5 個變體都已在表內但 leak — 應該有第 6 個變體沒被收）

---

## 5. 第一場戰役

三條路，按成本由低到高：

### 5.1 路 A：intro 最後 Gargoyle Ambush（**最便宜**）

按 SPACE 推進 intro 整段、看到 `Gargoyles surround you!` / `魔像族將汝團團圍住！`，自動進到 combat。
**已知 fragment 都中文化**（pass6 驗），戰鬥訊息 `杜普雷 擦傷。` `魔像 被擊殺！` 等全中文。

### 5.2 路 B：autosave 出 throne room 去野外

throne room 在 LB 城堡，往外走 → 進 Britain 城 → 出南門 → 草原 spawn 怪。需要 5-10 分鐘移動。

### 5.3 路 C：純驗 combat mode 切換（不必真打）

最快驗 combat fragment：
1. 進到 throne room
2. 按 `C` → 顯示 `>進入戰鬥！`
3. 按 `A` → 顯示 `以劍攻擊-什麼？`（無 target 就會問）
4. 按 `C` → 顯示 `>脫離戰鬥！`

不必真有怪也能驗 combat 命令列中文化。pass5/6 大多走這條。

---

## 6. 截圖

### 6.1 工具

```bash
# 全螢幕
DISPLAY=:99 import -window root /tmp/u6_NN.png

# 特定視窗（先 search window id）
WID=$(DISPLAY=:99 xdotool search --sync --name 'ScummVM' | head -1)
DISPLAY=:99 import -window $WID /tmp/u6_NN.png
```

### 6.2 時機（**雷**）

按下命令鍵後 **必須等 200-500ms** 才截圖，否則抓到「按下前」的畫面。
xdotool 送鍵後配 `sleep 0.5`，再截。`--dump-frame N` 不適用（ScummVM 沒此 flag）。

### 6.3 讀截圖

agent 用 `Read` tool 直接讀 PNG file，視覺判讀 caption 是否中文 / 是否亂碼 / wrap 是否重疊。

---

## 7. CHT debug log 訊號表

`-d 1` 啟動下，stderr 預期看到的 marker（2026-06-27 P1+P5 實機驗）：

| log 行 | 期待 | 已抓到範例 |
|---|---|---|
| `CHT: loaded NNNN entries + MMM fragments from cht_strings.tab (v3, hashed)` | 表 load 成功；v1.5.2 baseline = **7298 entries + 189 fragments** | ✅ 直接命中 |
| `WOUFont(cutscene): loaded big5_u6_12x12.fnt — intro CJK enabled` | intro 字型 OK | ✅ |
| `ConvFont: loaded big5_u6_12x12.fnt — ConverseGump CJK enabled` | 對話框字型 OK | ✅（要 `--save-slot=2` 進到 game 後才印）|
| `U6Font: loaded big5_u6_12x12.fnt — CJK enabled` | 主面板字型 OK | ✅（同上）|
| `CHT-LOOK party-name: <en>` | Look 黨員 | `CHT-LOOK party-name: anr2` |
| `CHT-LOOK actor-look: <en>` | 每次 Look 非黨員 NPC（issue #1.3 抓這個）| ⏳ 還沒抓到 LB 變體 |
| `CHT-LOOK ground: <en>` | 每次 Look 地形（issue #1.2 tile 抓這個）| `CHT-LOOK ground: the floor`、`CHT-LOOK ground: water`（throne room 樣本）|
| `CHT-MISS: <en>` | engine 試 lookup 但表內沒命中 | （未抓到）|

**任何 `ERROR` / `assert` / `ctl byte` / `page fault`** = 立刻停手回報。

### 7.1 已收 ground tile 字串 vs cht_strings.tab 對照

| `CHT-LOOK ground:` 真實字串 | exact 表內？ | 我們 #1.2 加的 fragment 涵蓋？ |
|---|---|---|
| `the floor` | ❓ 待 verify | ❌ 我加的 11 條只有 `the tile` 沒 `the floor` |
| `water` | ❓ 待 verify | ❌ 沒對應 fragment |

→ **issue #1.2 修法需要擴大範圍**：不只 `tile`，常見 ground (`the floor`、`water`、`grass`、`a wall`…) 都要補 exact 或 fragment entry。實機掃一輪 throne room + 街道收完整字串再加。

---

## 8. 已知雷（萃自 5 輪 pass）

1. **`SDL_VIDEODRIVER=dummy` 進不去主選單以後**（無 mouse）— 要 Xvfb / Xephyr 真窗。
2. **intro 不是 timer 驅動**，是按鍵推進 — 不按 Space 卡住到天荒地老。
3. **xdotool send key 在 wine SDL app 不可靠** — 不要用 wine 跑 scummvm.exe 做 tester。
4. **autosave 跟 OBJLIST 衝突** — teleport 可能被 autosave 蓋過，做大改動前刪 autosave。
5. **autosave 出生點在 Chuckles 旁戰鬥** (pass5 觀察) — 已知對話會 loop 鎖住，要先打完 Chuckles riddle 才能走。或刪 autosave 重新 New Game。
6. **截圖時機**：按下鍵後 sleep 0.5s 再截，否則抓到變化前的畫面。
7. **`Portrait header` 黨員肖像標題（F1-F4 開的 gump）某些 NPC 仍英文**（如 InventoryGump header）— 已知架構限制，**不在 v1.5.2 scope**，別誤報為 leak。
8. **「CHT loaded log 未輸出」**（pass5 觀察）：某些 build 即使 `-d 1` 也沒印該行，但 CJK 實際 work — log 缺失不代表 CHT 沒生效，看畫面為準。
9. **多個 ScummVM session 同時跑** 會搶 SDL audio / display 鎖 — 一次只跑一個。
10. **「杜」glyph 視覺易誤認 (2026-06-27 朋友 finding)**：12px WQY Sharp embedded bitmap 的「杜」row 3 = `█████··█`，跟「壯」「狀」「牡」的「丬」/「牜」結構像素化後接近，玩家會看成「壯普雷 / 狀普雷 / 牡普雷」。字型 atlas 確實是「杜」(Big5=A7F9) 沒翻錯，是 12px 解析度極限。對比 11px WQY Sharp 的「杜」row 4-8 有清楚分開的「木」橫+撇+捺三段，可能視覺較分明。修法 / 換字型尚未決定（task tracker）。

---

## 9. References

| 文件 | 看什麼 |
|---|---|
| **`DDSC-J-00124-遊戲手冊：創世紀６.pdf` p8-11** | **原版手冊「遊戲控制」權威鍵盤對照**（圖形指令 / 移動 / 其他 / 戰備指示 6 種）|
| `DDSC-J-00007-創世紀聖者之書特別版.pdf` p51-83 | 譯名權威、世界觀、角色背景 |
| `CONTEXT.md` | 專案總索引 + ubiquitous language（譯名 / 城市 / 系統用語）|
| `skills/u6-cht.md` | engine hook 點清單 / 二進位 lookup 格式 / 漏翻 SOP |
| `scummvm-src/devtools/create_ultima/files/ultima6/defaultkeys.txt` | Nuvie 鍵盤實裝完整 169 行（含 cheat / joy / KP / Alt-* 全 binding）|
| `dumps/tester_pass6_report.md` | 最新一輪（v1.3.1）完整截圖清單與 P0/P1 結果 |
| `dumps/tester_pass5_report.md` | autosave 在 Chuckles 旁這條雷的來源（**注意：那是 v1.3.1 期 user 自己改過的 save，2026-06-27 我驗 slot 2 是 throne room**）|
| `dumps/tester_pass4_report.md` | intro 按鍵推進雷的來源、cht_strings.tab Python 解碼範例 |
| `dumps/tester_pass3_report.md` | bilingual @keyword 驗證範例 |
| `dumps/tester_pass2_report.md` | 最早一輪、有完整 click LB 的 mouse 操作序列 |
| `tools/teleport.py` | NPC id 表（LB=5、Iolo=4、Linda=187…）、Avatar teleport-to-NPC |
| `~/.claude/skills/retro-game-playtest/` | 老遊戲實機驗證的方法論（headless ≠ 玩家可玩、按鍵後幀截圖、跨平台分歧）|

---

## 10. 一頁 sub-agent prompt 範本

把以下整段塞給 sub-agent，**不要再讓它重新摸索**：

```
你是 u6-cht 的實機 game-tester。先讀 /home/anr2/u6-cht/docs/PLAYTEST.md（5 分鐘）
再動手 — 該檔已 distill 5 輪 tester pass 的所有 know-how。

任務：<填具體任務，如「驗 LB 對話的 CHT-LOOK actor-look 真實字串」>

硬約束：
- 用 Xvfb（不用 wine、不用 dummy）
- 每次 scummvm launch 帶 timeout -s KILL 60，不放生
- 截圖前 sleep 0.5
- stderr 重導 file 再 grep（不直接 pipe）
- 卡 3 次同操作 → 誠實報告受阻，不無限重試
- 不進 plan mode、直接執行

完成後回報：
- 抓到的真實字串（如 CHT-LOOK actor-look: ...）
- 1-2 張關鍵 screenshot 路徑（讓我 Read 視覺判讀）
- 任何意外（如 autosave 位置變動、新 leak、xdotool 失靈）
```
