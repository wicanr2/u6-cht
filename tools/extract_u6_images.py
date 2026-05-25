#!/usr/bin/env python3
"""Extract U6 world map (WORLDMAP.BMP) and NPC portraits (PORTRAIT.A/B/Z) to PNG.

Pure-Python port of Nuvie's U6Lzw + U6Lib_n + GamePalette.  No game code linked.
Used to generate README art (Britannia map + NPC icons).
"""
import os
import struct
import sys
from PIL import Image

GAME = os.path.join(os.path.dirname(__file__), "..", "working", "game")


# ---------------------------------------------------------------- U6 LZW
def lzw_decompress(src: bytes) -> bytes:
    """Port of U6Lzw::decompress_buffer."""
    out = bytearray()
    # dict entries: codeword -> (root_byte, parent_codeword)
    dict_root = [0] * 0x1000
    dict_cw = [0] * 0x1000

    bits_read = 0
    codeword_size = 9
    next_free = 0x102
    dict_size = 0x200
    contains = 0x102  # not strictly needed; we track next_free

    data = src[4:]  # skip 4-byte uncompressed-size header

    def get_codeword(bits_read, size):
        byte_i = bits_read // 8
        b0 = data[byte_i]
        b1 = data[byte_i + 1] if byte_i + 1 < len(data) else 0
        if size + (bits_read % 8) > 16:
            b2 = data[byte_i + 2] if byte_i + 2 < len(data) else 0
        else:
            b2 = 0
        cw = (b2 << 16) + (b1 << 8) + b0
        cw >>= (bits_read % 8)
        cw &= (1 << size) - 1
        return cw

    def get_string(codeword):
        stack = []
        cur = codeword
        while cur > 0xff:
            stack.append(dict_root[cur])
            cur = dict_cw[cur]
        stack.append(cur & 0xff)
        return stack  # leaf-last: stack[-1] is the root (top)

    pW = 0
    while True:
        cW = get_codeword(bits_read, codeword_size)
        bits_read += codeword_size

        if cW == 0x100:
            codeword_size = 9
            next_free = 0x102
            dict_size = 0x200
            cW = get_codeword(bits_read, codeword_size)
            bits_read += codeword_size
            out.append(cW & 0xff)
        elif cW == 0x101:
            break
        else:
            if cW < next_free:
                s = get_string(cW)
                C = s[-1]
                # output string (stack pops top..bottom => reversed)
                for ch in reversed(s):
                    out.append(ch)
                dict_root[next_free] = C
                dict_cw[next_free] = pW
                next_free += 1
                if next_free >= dict_size and codeword_size < 12:
                    codeword_size += 1
                    dict_size *= 2
            else:
                s = get_string(pW)
                C = s[-1]
                for ch in reversed(s):
                    out.append(ch)
                out.append(C)
                if cW != next_free:
                    raise ValueError("cW != next_free_codeword")
                dict_root[next_free] = C
                dict_cw[next_free] = pW
                next_free += 1
                if next_free >= dict_size and codeword_size < 12:
                    codeword_size += 1
                    dict_size *= 2
        pW = cW
    return bytes(out)


# ---------------------------------------------------------------- U6Lib_n (U6 type)
class U6Lib:
    def __init__(self, path, lib_size=4):
        self.data = open(path, "rb").read()
        self.lib_size = lib_size
        self.filesize = len(self.data)
        self.offsets = []
        self.flags = []
        self._parse()

    def _read4(self, off):
        return struct.unpack_from("<I", self.data, off)[0]

    def _parse(self):
        # determine num_offsets: scan until we hit first data block
        max_count = 0xffffffff
        i = 0
        while (i + 1) * self.lib_size <= len(self.data):
            raw = self._read4(i * self.lib_size)
            offset = raw & 0xffffff
            if offset != 0 and offset // self.lib_size < max_count:
                max_count = offset // self.lib_size
            i += 1
            if i >= max_count:
                break
        num = max_count
        for k in range(num):
            raw = self._read4(k * self.lib_size)
            self.offsets.append(raw & 0xffffff)
            self.flags.append((raw & 0xff000000) >> 24)
        self.offsets.append(self.filesize)  # sentinel for last size
        self.num = num

    def item_size(self, n):
        off = self.offsets[n]
        if off == 0:
            return 0
        nxt = 0
        for o in range(n + 1, self.num + 1):
            if self.offsets[o]:
                nxt = self.offsets[o]
                break
        return nxt - off if nxt > off else 0

    def is_compressed(self, n):
        return self.flags[n] in (0x1, 0x20)

    def get_item(self, n):
        off = self.offsets[n]
        size = self.item_size(n)
        if off == 0 or size == 0:
            return None
        raw = self.data[off:off + size]
        if self.is_compressed(n):
            return lzw_decompress(raw)
        return raw


# ---------------------------------------------------------------- palette
def load_palette(path):
    buf = open(path, "rb").read()
    pal = []
    for i in range(256):
        r = buf[i * 3] << 2
        g = buf[i * 3 + 1] << 2
        b = buf[i * 3 + 2] << 2
        pal.extend((r, g, b))
    return pal


def indexed_to_image(data, w, h, pal):
    img = Image.frombytes("P", (w, h), bytes(data[:w * h]))
    img.putpalette(pal)
    return img.convert("RGB")


# ---------------------------------------------------------------- main ops
def extract_worldmap(outdir, pal):
    raw = open(os.path.join(GAME, "WORLDMAP.BMP"), "rb").read()
    decomp = lzw_decompress(raw)
    print(f"worldmap decompressed: {len(decomp)} bytes")
    side = 128  # 128x128 overview
    img = indexed_to_image(decomp, side, side, pal)
    out = os.path.join(outdir, "worldmap_raw.png")
    img.save(out)
    print("wrote", out, img.size)
    return img


def extract_portrait(num, pal):
    """num = portrait index (actor_num - 1). Returns RGB image 56x64."""
    if num < 98:
        lib = U6Lib(os.path.join(GAME, "PORTRAIT.A"))
        idx = num
    else:
        lib = U6Lib(os.path.join(GAME, "PORTRAIT.B"))
        idx = num - 98
    item = lib.get_item(idx)
    if not item:
        return None
    # portrait items are themselves standalone LZW streams (Nuvie always
    # lzw-decompresses portrait data regardless of the lib flag)
    data = lzw_decompress(item)
    return indexed_to_image(data, 56, 64, pal)


if __name__ == "__main__":
    outdir = os.path.join(os.path.dirname(__file__), "..", "dumps", "u6_images")
    os.makedirs(outdir, exist_ok=True)
    pal = load_palette(os.path.join(GAME, "U6PAL"))

    extract_worldmap(outdir, pal)

    # sample portraits: Iolo(4), LB(5), Geoffrey(7)
    for name, actor in [("Iolo", 4), ("LordBritish", 5), ("Geoffrey", 7)]:
        img = extract_portrait(actor - 1, pal)
        if img:
            p = os.path.join(outdir, f"portrait_{actor:03d}_{name}.png")
            img.save(p)
            print("wrote", p)
        else:
            print("no portrait for", name)
