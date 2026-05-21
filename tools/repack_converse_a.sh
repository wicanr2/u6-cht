#!/bin/bash
# Repack all .conv files in dumps/converse into converse.a.
# Uses Nuvie unpack_conv -r (uncompressed mode).
#
# Inputs: any .conv file with .zh sibling will be used as the translated version.
# All originals are preserved; we just symlink/copy .zh over for the duration of pack.

set -e
CONV_DIR=/home/anr2/u6-cht/dumps/converse
TOOL=/home/anr2/u6-cht/tools/unpack_conv

cd "$CONV_DIR"

# Backup current .conv files, swap in .zh versions where present
backed_up=0
swapped=0
for zh in *.conv.zh; do
    [[ -f "$zh" ]] || continue
    base="${zh%.zh}"
    if [[ -f "$base" ]]; then
        cp -f "$base" "$base.bak"
        cp -f "$zh" "$base"
        backed_up=$((backed_up + 1))
        swapped=$((swapped + 1))
    fi
done
echo "swapped $swapped .conv files (originals kept as .bak)"

# Repack
"$TOOL" -r

# Restore backups
for bak in *.conv.bak; do
    [[ -f "$bak" ]] || continue
    base="${bak%.bak}"
    mv -f "$bak" "$base"
done
echo "restored $backed_up originals"
echo ""
echo "Output: $CONV_DIR/converse.a ($(stat -c%s converse.a) bytes)"
