#!/usr/bin/env bash
# Re-pack u6cht windows release 7z with CRLF run.bat (issue #2).
# Usage: ./repack.sh <input.7z> <variant: free|full> <out.7z>
# Source of truth for run.bat is in this dir (CRLF, verified by `file`).
set -euo pipefail
IN="${1:?input .7z}"
VAR="${2:?free|full}"
OUT="${3:?output .7z}"
HERE="$(cd "$(dirname "$0")" && pwd)"
case "$VAR" in
  free) SRC_BAT="$HERE/run-free.bat";;
  full) SRC_BAT="$HERE/run-full.bat";;
  *) echo "variant must be free or full" >&2; exit 1;;
esac
# verify source is CRLF
file "$SRC_BAT" | grep -q CRLF || { echo "source $SRC_BAT not CRLF"; exit 1; }
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
7z x -y -o"$WORK" "$IN" >/dev/null
ROOT="$(ls "$WORK")"
[ -d "$WORK/$ROOT" ] || { echo "expected single root dir, got: $ROOT"; exit 1; }
cp "$SRC_BAT" "$WORK/$ROOT/run.bat"
file "$WORK/$ROOT/run.bat" | grep -q CRLF || { echo "post-copy not CRLF"; exit 1; }
(cd "$WORK" && 7z a -t7z -mx=9 "$OUT" "$ROOT" >/dev/null)
echo "OK: $OUT"
file "$WORK/$ROOT/run.bat"
