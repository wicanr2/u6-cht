#!/bin/bash
# Launch patched ScummVM with the U6 CHT working dir.
#
# Strategy: run scummvm pointed directly at the game data folder.
# ScummVM will detect U6 via files (e.g. game.exe, lzdngblk, schedule).
SCUMMVM=/home/anr2/u6-cht/scummvm-src/scummvm
GAMEDIR=/home/anr2/u6-cht/working/game

if [[ ! -x "$SCUMMVM" ]]; then
    echo "scummvm binary not built yet: $SCUMMVM"
    exit 1
fi

# Run directly with the game path. ScummVM tries to detect; --auto-detect picks
# the first detected game from the dir.
exec "$SCUMMVM" --auto-detect --path="$GAMEDIR" --no-fullscreen "$@"
