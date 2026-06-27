#!/usr/bin/env bash
# v2.x patch: 把 patched intro.lua (Lua chunk multi-frame split) 寫入 ultima.dat
# Run after `git pull` to make ScummVM 用新版 Lua intro。
#
# 兩個 ultima.dat 都要 patch:
#   working/game/ultima.dat — 玩家 launch 用的 game dir 端 (priority 高)
#   scummvm-src/dists/engine-data/ultima.dat — dev binary 從 extrapath 端
#
# 修 source of truth: nuvie/data/scripts/u6/intro.lua (gitignored, 從 patches/
# intro-lua-multi-frame.patch 還原)。

set -euo pipefail
HERE="$(cd "$(dirname "$0")/.." && pwd)"

INTRO_LUA="$HERE/nuvie/data/scripts/u6/intro.lua"
if [ ! -f "$INTRO_LUA" ]; then
  echo "ERROR: $INTRO_LUA 不存在。先 clone Nuvie / 從 patches/intro-lua-multi-frame.patch 還原。" >&2
  exit 1
fi

# 暫存到正確 zip-internal path
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
mkdir -p "$TMP/ultima6/scripts/u6"
cp "$INTRO_LUA" "$TMP/ultima6/scripts/u6/intro.lua"

for DAT in \
  "$HERE/working/game/ultima.dat" \
  "$HERE/scummvm-src/dists/engine-data/ultima.dat"
do
  if [ ! -f "$DAT" ]; then
    echo "skip: $DAT 不存在"
    continue
  fi
  (cd "$TMP" && zip -u "$DAT" ultima6/scripts/u6/intro.lua) > /dev/null
  echo "patched: $DAT"
done

echo "done."
