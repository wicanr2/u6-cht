# u6-cht — previous-work snapshot (2026-06-27)

跨機接續用。下次在別台電腦 `claude --resume 545a5e94-8f0d-4499-bee5-3cf51604932a` 立刻上手。

---

## TL;DR

- **v2.0 SHIPPED**：漢字 16×16 真實解析度（仿 PC-98 1991 PonyCanyon）
- GitHub: https://github.com/wicanr2/u6-cht
- Release: https://github.com/wicanr2/u6-cht/releases/tag/v2.0
- main HEAD: `a922c70`、tag `v2.0` + `v2.0-rc1`
- Linux AppImage (123 MB) + Windows zip (93 MB) 已上 Release（slim、無遊戲檔）
- Issues #1 + #2 closed

朋友 finding（12×12「杜」字易誤認為「壯」）→ **v2.0 16×16 native 100% 解決**。

---

## 本次 session 做了什麼

### v1.5.2 first wave (commits `d80425d` → `f052061`)

- `dist/windows/run-free.bat` + `repack.sh` CRLF source of truth（issue #2 fix）
- `tools/build_lookup_table.py` source dir `dumps/translations/` → `translations/`（issue #1.1 opened!/closed! leak root cause）
- `_engine_fragments.json` longest-first sort（issue #1.4 intro 7 段退化）
- `tools/fix_term_drift.py` 加 `_engine_*.json` 排除（issue #1.5）
- 11 條 tile token 候選 fragment（issue #1.2）

### v2.0 ship（branch `v2-16x16` merged → main `702b44d`）

**Phase 0 source survey** (`docs/phase0-findings.md`):
- ScummVM Nuvie `Screen::init()` 從 config 讀 width/height，無上限
- 不需 fork OSystem、`RenderSurface` 可加 overlay layer
- 三條 font path (U6Font/ConvFont/WOUFont) drawString 都吃 `Screen *`

**Phase 1 字型 atlas** (`docs/phase1-font-survey.md`):
- WenQuanYi Zen Hei Sharp 16×16 embedded bitmap (face_idx=2)
- `tools/build-big5-font-16x16.py` 仿 12×12 build pipeline
- `big5_u6_16x16.fnt` 472,256 bytes、14,758 slots、13,707 字 cover (92.9%)
- `tools/dump_font_glyph.py` 對比 12×12 vs 16×16 — 朋友 finding 確認 16×16「杜」「木」結構分明

**Phase 2 Screen 雙 surface** (`docs/phase2-screen-dual-surface.md`):
- `_rawSurface 640×400 native` + `_gameSurface 320×200` + `_overlaySurface 640×400`
- `performUpdate`：2× nearest scale `_gameSurface` → `_rawSurface` + compose overlay (transparent key 0x0000)
- caller code 0 行改動

**Phase 3 三條 font path → overlay** (`docs/phase3-cjk-native-16x16.md`):
- BIG5_GLYPH_BYTES 24 → 32（16-row × 2 bytes）
- drawBig5Char 改 call `screen->queueCJKGlyph` 寫 `_overlaySurface` direct（不是 queue，persistent across frame）
- bug 演進：queue 模型失敗（msg_scroll dirty-only pattern → frame 1 後 CJK 消失）→ persistent overlay surface + transparent compose

**Phase 4 5 caveats fix** (`docs/phase4-caveats-fix.md`):
- 1 cursor coord：`get_mouse_location /= _displayScale` ✅ Iter 3 verified（cursor follow mouse）
- 2 cutscene shape 16-row：full 16-row iterate（line spacing dynamic 14/8）✅
- 3 overlay stale：`invalidateOverlayRegion` 在 `fill/clear/blit/blitbitmap` mirror clear ✅
- 4 font getCharWidth：Big5 byte (high bit) return 8 ✅ wrap 不再 miscount
- 5 conv_garg_font：加 `initBig5` ✅（gargoyle convo native 16×16）

**Phase 5 ship**:
- Linux AppImage 123 MB（reuse v1.5.1 squashfs base + 替換 scummvm + 16x16 font + ultima.dat）
- Windows mingw cross-compile（本機 toolchain 不需 docker）— 93 MB 7z
- macOS GitHub Actions workflow 寫 `.github/workflows/build-macos.yml`（user trigger）
- README v1.5 截圖全替換 v2.0 (10+ 張) + 圖文對位 (group C + D iter 2)
- RELEASE_NOTES_v2.0.md + CHANGELOG.md v2.0 entry

### v2.x caveat 1 真根治（commits `ea09a34` + `29a2e19`）

intro 字疊 root cause：Lua `intro.lua` 4-chunk `image_print` 累積 *y = 8 + 4×14 = 64 px > cinematic box ~40 px。

3 處 split done:
- line 381 (4 chunks「You have traded the Avatar's life...」) ✅ verified frame 1+2 clean
- line 745 (3 chunks「You bolt from your house...」) ✅
- line 923 (3 chunks「Exultant memories...by Lord British...」) ✅

build pipeline: `patches/intro-lua-multi-frame.patch` (git tracked) + `tools/patch-ultima-dat-intro-lua.sh` (zip update + working/game/ultima.dat + scummvm-src/dists/engine-data/ultima.dat 兩處)。

AppImage + Windows zip rebuild + `gh release upload v2.0 --clobber` re-uploaded。

---

## v2.x backlog（6 項，tasks #35-40）

跟 `docs/WORKLIST.md` 同步:

| # | 項目 | 風險 |
|---|---|---|
| #35 | intro Lua line 828「Near the stones」split | 高 — fade_in/stones_update animation 配對 |
| #36 | intro Lua line 953「But your joy」y 重排 | 中 — hardcoded absolute y |
| #37 | Look NPC 實機截圖 | 低 — hover cursor exact pixel |
| #38 | rm -rf dumps/translations/ | 低 |
| #39 | dumps/tester_pass{2..6}_report.md stale 清理 | 低 |
| #40 | macOS GitHub Actions trigger | 中 — runner queue |

---

## 鐵則 / 硬約束（必須遵守）

- **commit message 中文 + Co-Authored-By trailer**：
  ```
  Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
  ```
- **push 用** `GIT_SSH_COMMAND="ssh -i ~/.ssh/id_github_wicanr2 -o IdentitiesOnly=yes"` 前綴
- **FULL release 含遊戲檔 IP** 絕不上 GitHub — `releases/` gitignored、上 Release 只 slim
- **commit/push 只在 user 明確 ask** — 不主動 push
- **第一性原理 / 不退方案 A / 老遊戲重製不考慮成本** — feedback memory rule

---

## 工具鏈 / harness 速查

| 工具 | 用途 |
|---|---|
| `scummvm-src/scummvm` | Linux native 137 MB ELF（patched）|
| `working/game/ultima.dat` + scummvm-src/dists/engine-data/ultima.dat | 同步 patched intro.lua（v2.x caveat 1）|
| `tools/build-big5-font-16x16.py` | WQY Sharp 16×16 atlas build → `big5_u6_16x16.fnt` |
| `tools/dump_font_glyph.py` | glyph dump（12×12 vs 16×16 比對）|
| `tools/patch-ultima-dat-intro-lua.sh` | Lua intro patch 寫 ultima.dat |
| `tools/build_lookup_table.py` | rebuild `cht_strings.tab` v3 |
| `tools/fix_term_drift.py` | 譯名漂移修正（excludes `_engine_*.json`）|
| `dist/windows/repack.sh` | Windows zip CRLF hotfix |
| `dist/v2.0/AppDir` | Linux AppImage 打包 base（123 MB after pack）|
| Xvfb `:99` + xdotool + import | game-tester headless harness |

ScummVM launch:
```bash
DISPLAY=:99 nohup ./scummvm-src/scummvm \
  --auto-detect --path=./working/game \
  --no-fullscreen -d 1 --save-slot=2 ultima6 > /tmp/u6.log 2>&1 &
```

ScummVM log baseline (v2.0):
```
CHT: loaded 7298 entries + 189 fragments from cht_strings.tab (v3, hashed)
WOUFont(cutscene): loaded big5_u6_16x16.fnt — intro native 16×16 CJK enabled
ConvFont: loaded big5_u6_16x16.fnt — ConverseGump native 16×16 CJK enabled
ConvGargFont: loaded big5_u6_16x16.fnt — gargoyle convo native 16×16 CJK enabled
U6Font: loaded big5_u6_16x16.fnt — native 16×16 CJK enabled
```

---

## § 在別台電腦接續 Claude session ★

**最近 session UUID**: `545a5e94-8f0d-4499-bee5-3cf51604932a`

`~/.claude/projects/-home-anr2-u6-cht/` 整個帶過去（bundle 內 `claude-session/projects/`）。

新機解 bundle 到 `/home/anr2/u6-cht/`（相同絕對路徑）：
```bash
cd /home/anr2/u6-cht
claude --resume 545a5e94-8f0d-4499-bee5-3cf51604932a
```

如果路徑不同（不同 user / home）：
- 改 encoding dir name：`mv ~/.claude/projects/-home-anr2-u6-cht ~/.claude/projects/-home-NEW-u6-cht`
- 或直接 `claude --resume 545a5e94-8f0d-4499-bee5-3cf51604932a`（UUID 不卡路徑）

memory 在 session dir 內 `memory/`（含 6 條 feedback / project memory）— 自動 load。

---

## 記憶索引（自動 load on `claude -r`）

| memory | 用途 |
|---|---|
| `u6-cht-project` | Project state snapshot |
| `retro-game-cjk-rules` | 通用 retro RPG CJK 漢化規則 14 條 |
| `feedback-search-first-not-try` | 動手前 grep 現有 markdown |
| `feedback-first-principles-step-by-step` | 第一性原理鐵則 |
| `feedback-retro-remake-no-cost-ceiling` | 老遊戲重製不考慮成本 |

---

## 下一步建議

優先 v2.x backlog #40 (macOS Actions trigger) 完成三平台 ship。
然後 #38 (rm dumps/translations) + #39 (dumps/ stale 清理) 是收尾。
#35 / #36 / #37 是 intro / Look NPC 細節品質，不阻塞。
