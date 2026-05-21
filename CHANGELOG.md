# Changelog

## v1.2.1 (2026-05-22)

### Fixed
- Intro cinematic captions 2-5 (storm/lightning/stones sequence) — added 11 missing fragments matching Lua's actual `image_print` chunk splits
  - "You have traded the Avatar's life of peril and adventure" 等 (split per-line)
  - "Tongues of lightning lash the sky..." / "crescendo of thunder...." / "...and in moments, the storm is upon you."
- Tester pass 4 PASS（含條件，11/15 captions verified Chinese）

### Build
- `releases/u6cht-1.2.1-linux-x86_64.AppImage` (123 MB)
- `releases/u6cht-1.2.1-windows-x86.7z` (91 MB)

---

## v1.2 (2026-05-22)

### Added
- **Cinematic intro Chinese translation** — `ScriptCutscene::ScriptCutscene` ctor now calls `CHTranslate::load(cfg)` before cinematic plays, fixing the issue where intro ran before `Game::init()` (where CHT was loaded)
- Print hooks in `print_text` + `print_text_raw` for cinematic CHT
- 13+ intro caption fragments

### Fixed (editor3 round)
- 066 Gwenno keyword brackets shifted by 1 (songs/notation/guild) → re-aligned
- 066 Gwenno @number (音符) → @number (數字)
- Valor 勇氣 → 勇敢 in 044/049/127/160 (4 NPCs, 5 occurrences) — unified with 194 + editor1
- Honor 榮耀 → 榮譽 in 197 — majority usage (25:12)
- Captain John 操控 → 克制 — matches 033/164/174 + BOOK_DAT
- 180 Mandrake virtue list: 英勇/榮耀 → 勇敢/榮譽
- 6 minor name bracket fixes (Thindle / Britain / 小麵包 etc)

### Stats
- 7298 hashed entries + 77 plain fragments (was 7298 + 40 in v1.1)
- Editor3 score 44/50

---

## v1.1 (2026-05-21)

### Engine
- **Cursor Y stride bug fix** (designer agent finding) — `cursor_y * 8` → `cursor_y * 10` to match `drawLine` stride. Cursor & ↓ prompt no longer block last line
- **Portrait header 中文化** — 4 codepath hooks (portrait_view, portrait_view_gump, party_view, container_view_gump, doll_view_gump)
- **Look/Search 路徑 fragment substitution** — `Thou dost see <tile>` now Chinese
- **「夠不著」→「搆不著」** typo fix in cht_translate.cpp hardcoded Big5 bytes
- **Multi-paragraph split** — NPC 多段對話分段 lookup

### Translations
- **Codex 守則之書 → 知識寶典** (聖者之書 1992 canonical, 39 occurrences / 15 files)
- **25+ `@EN（ZH）ZH` 重字 bug cleared** (editor2 round)
- **6 P0 fixes** (editor1 round): Tholden/Sherry/Chuckles/Reaper/大烏賊/Dupre 甲冑
- Valor 勇氣 → 勇敢, Singularity 200 quest hint brackets re-aligned
- Reaper 死神 → 樹妖 (聖者之書 p76 canonical)
- 大烏賊 統一 (遊戲手冊 + 聖者之書 一致)

### Tooling
- `tools/fix_at_duplicates.py` — auto-strip @EN（ZH）ZH duplicate-suffix
- `tools/fix_p0_editor_round1.py` + `tools/fix_p0_editor3.py`
- `tools/fix_bilingual_brackets.py` — canonical map post-fix
- `tools/bilingual_keywords.py` — @中文 → @english（中文）
- `tools/extract_npc_keywords.py` — 198 NPC × 407 keyword cheatsheet

### Documentation
- `skills/u6-cht.md` — main project skill
- `skills/u6-game-tester.md` — in-game testing playbook
- `dumps/editor_in_chief_report.md` — round 1
- `dumps/editor2_report.md` — round 2
- `dumps/editor3_report.md` — round 3 (44/50)
- `dumps/dialog_redesign.md` — UX designer proposal
- `dumps/distilled_sage_book.md` — 聖者之書 P1-50 精華
- `dumps/distilled_manual.md` — 遊戲手冊 13 頁精華
- `dumps/sage_book_cross_ref.md` — cross-ref 決策
- `dumps/tester_pass3_report.md` — pass 3 (7/9 PASS)
- `dumps/tester_pass4_report.md` — pass 4 (PASS with conditions)

### Build
- `releases/u6cht-1.1-linux-x86_64.AppImage` (123 MB)
- `releases/u6cht-1.1-windows-x86.7z` (91 MB)

---

## v1.0 (2026-05-21)

### Initial release
- Plan B (load-time string substitution) architecture
- 199 NPC + BOOK.DAT translated (7298 entries)
- 8 engine hook points (NPC dialog, Look, Search, Lua print, Book, MsgScroll central, $G honorific, Avatar SLOOK)
- Big5 12px font (WenQuanYi Zen Hei Sharp)
- v3 binary lookup with FNV-1a 64-bit hash keys
- 40 plain fragments for dynamic combat / actor name strings

### Repo published
- https://github.com/wicanr2/u6-cht @ `f114473`

### License
- Engine patches: GPL v3+ (ScummVM upstream)
- Translation data: CC BY-SA 4.0
- Font: Apache 2.0 (AR PL UMing → WQY Sharp)
- Tools: MIT
- Documentation: CC BY 4.0

---

## Roadmap v1.3

- (a) `?` / `help` magic command — display current NPC keyword list in-game
- (b) Dialog redesign Plan 2 (stride 12px + panel 128px) per designer agent
- Cinematic caption 2 visual layout (currently cramped — needs newline handling)
- Multi-PR sync to ScummVM upstream (offer engine patches)
- 8 professions + 26 mantras + 8 reagents glossary entries
- 9px font experimentation (designer Plan 3) — if quality acceptable
