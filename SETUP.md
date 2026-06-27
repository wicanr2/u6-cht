# u6-cht dev-setup — 跨機接續 SOP

## 0. 解包

```bash
# 把 bundle 解到「跟原機相同的絕對路徑」最省事（claude session 接續直接 work）
mkdir -p /home/anr2
cd /home/anr2
tar --use-compress-program='zstd -T0 -d' -xf u6cht-dev-setup-YYYYMMDD.tar.zst
# 解出來會有：
#   u6-cht/                    主 repo
#   .claude/projects/-home-anr2-u6-cht/  Claude session 接續用
```

如果無法用相同路徑（不同 user / home），看 § 4 「Claude 接續」處理。

---

## 1. 系統依賴（Ubuntu / Debian 系）

```bash
sudo apt update
sudo apt install -y \
  build-essential git curl wget zip unzip 7zip-full p7zip-full zstd \
  libsdl2-dev libsdl2-net-dev \
  libfreetype-dev libpng-dev libjpeg-dev libfluidsynth-dev \
  liba52-0.7.4 libfaad2 libflac8 libmad0 libmpeg2-4 libogg0 libtheora0 libvorbis0a \
  pkg-config \
  python3 python3-pip python3-freetype \
  xvfb xdotool imagemagick ffmpeg \
  g++-mingw-w64-x86-64 binutils-mingw-w64-x86-64 \
  i686-w64-mingw32-g++ i686-w64-mingw32-binutils \
  wine \
  gh
```

Python pkgs：
```bash
pip3 install --user freetype-py Pillow
```

字型：
```bash
sudo apt install -y fonts-wqy-zenhei fonts-arphic-uming fonts-noto-cjk fonts-noto-cjk-extra
```

GitHub auth：
```bash
gh auth login   # 用 wicanr2 帳號
# 或 set GH SSH key (~/.ssh/id_github_wicanr2 自帶 in bundle 若有)
```

---

## 2. 重建 build（Linux native）

```bash
cd /home/anr2/u6-cht/scummvm-src
make -j$(nproc)
ls scummvm   # 應 137 MB ELF
```

第一次 build 慢（~10 分鐘）；後續 incremental 30 秒。

## 3. 重建 Linux AppImage

```bash
cd /home/anr2/u6-cht
# 用既有 AppDir（含 lib bundle）+ 換 v2.0 scummvm + 16x16 font
cp scummvm-src/scummvm dist/v2.0/AppDir/usr/bin/scummvm
cp working/game/big5_u6_16x16.fnt dist/v2.0/AppDir/u6cht-data/
cp working/game/cht_strings.tab    dist/v2.0/AppDir/u6cht-data/
cp working/game/ultima.dat         dist/v2.0/AppDir/usr/share/scummvm/ultima.dat
cd dist/v2.0
rm -f u6cht-2.0-linux-x86_64.AppImage
/home/anr2/zak-cht-build/appimagetool --appimage-extract-and-run AppDir u6cht-2.0-linux-x86_64.AppImage
```

appimagetool 需自備：https://github.com/AppImage/appimagetool/releases。

## 4. Claude `claude -r` 跨機接續 ★

新機跑：

```bash
cd /home/anr2/u6-cht
claude --resume 545a5e94-8f0d-4499-bee5-3cf51604932a
# 或最近: claude --continue
```

如果路徑不同（e.g. `/home/other/u6-cht`）：
1. 把 `.claude/projects/-home-anr2-u6-cht/` 改名成新路徑 encoding（`/`→`-`、開頭 `-`）：
   ```bash
   mv ~/.claude/projects/-home-anr2-u6-cht ~/.claude/projects/-home-other-u6-cht
   ```
2. 或者直接 `claude --resume 545a5e94-8f0d-4499-bee5-3cf51604932a`（用 UUID 不卡路徑）。

memory 在 `.claude/projects/-home-anr2-u6-cht/memory/` — 自動 load。

---

## 5. Windows mingw cross-compile（v2.x 還要重 build 時用）

```bash
# 同步 v2.0 patches 進 windows source（已 cross-compile 過一次）
cd /home/anr2/zak-cht-build/scummvm-win-src   # 如果 bundle 帶 zak-cht-build
# 或 fresh clone：
# git clone --depth 1 https://github.com/scummvm/scummvm.git
# cd scummvm
# git apply ~/u6-cht/patches/scummvm-u6cht.patch

# 複製 v2.0 改的 7 個 file 過去（最快）：
for f in screen.h screen.cpp; do
  cp /home/anr2/u6-cht/scummvm-src/engines/ultima/nuvie/screen/$f \
     engines/ultima/nuvie/screen/$f
done
for f in u6_font.cpp conv_font.cpp wou_font.cpp font_manager.cpp; do
  cp /home/anr2/u6-cht/scummvm-src/engines/ultima/nuvie/fonts/$f \
     engines/ultima/nuvie/fonts/$f
done
cp /home/anr2/u6-cht/scummvm-src/engines/ultima/nuvie/script/script_cutscene.cpp \
   engines/ultima/nuvie/script/script_cutscene.cpp

# build (本機 mingw toolchain native，不需 docker)
make -j$(nproc)
ls scummvm.exe   # 應 47 MB PE32 console
```

詳細 ship pipeline ref：`~/.claude/skills/retro-game-cht-package/SKILL.md`

## 6. Lua intro patch（v2.x caveat 1 真根治）

```bash
cd /home/anr2/u6-cht
./tools/patch-ultima-dat-intro-lua.sh
# 把 patched intro.lua zip 進 working/game/ultima.dat + scummvm-src/dists/engine-data/ultima.dat
```

詳見 `patches/intro-lua-multi-frame.patch`。

---

## 7. 跨機 verify smoke test

```bash
cd /home/anr2/u6-cht
DISPLAY=:99 nohup ./scummvm-src/scummvm \
  --auto-detect --path=./working/game \
  --no-fullscreen -d 1 --save-slot=2 ultima6 > /tmp/u6_smoke.log 2>&1 &
sleep 14
grep '16x16' /tmp/u6_smoke.log   # 應看到 4 條 native 16×16 CJK enabled 行
```

---

## ⚠️ IP / 隱私

bundle **含遊戲檔** (`working/game/CONVERSE.A` 等 Origin Systems 1990 © + PDF 1992 中文化雜誌)：
- 個人自留 OK
- **絕不公開散布**（gitignored、不 push）
- 上 GitHub Release 只能 ship slim（不含 game data）— v2.0 已照做

claude-session `*.jsonl` 含完整對話 — 別公開。
