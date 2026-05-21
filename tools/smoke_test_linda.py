#!/usr/bin/env python3
"""
Smoke test: replace Linda's "Welcome, friend." with Big5 中文 and repack.

Linda's .conv file structure (offset 0):
  FF BB              header
  "Linda"            actor name
  F1                 separator
  "a rugged looking lady farmer."  description
  0A 2A F2 22 ...   <newline + opcode + quoted greeting>
"""
import os, shutil, subprocess

WORK = '/home/anr2/u6-cht/dumps/converse'
TOOL = '/home/anr2/u6-cht/tools/unpack_conv'

# Re-extract fresh
os.chdir(WORK)
for ext in ('a', 'b'):
    src = f'/home/anr2/u6-cht/ultima6/CONVERSE.{ext.upper()}'
    dst = f'converse.{ext}'
    shutil.copy(src, dst)

# Wipe old .conv outputs so unpack regenerates
for f in os.listdir('.'):
    if f.endswith('.conv'):
        os.remove(f)
subprocess.run([TOOL], capture_output=True, check=True)

linda_path = '187_Linda.conv'
data = bytearray(open(linda_path, 'rb').read())

# Original line: 0x2C..0x3D = '"Welcome, friend."' (18 bytes incl quotes)
# Find it precisely:
old = b'"Welcome, friend."'
idx = bytes(data).find(old)
print(f'Found "Welcome..." at offset {idx} (len {len(old)})')

# Make a replacement of EXACTLY the same byte length (18 bytes).
# Big5: "「歡迎，朋友。」" — 8 chars × 2 = 16 bytes; pad with 2 spaces.
new = '「歡迎，朋友。」'.encode('big5')
print(f'Replacement (Big5): {len(new)} bytes : {new.hex(" ")}')
# Pad to 18 bytes with spaces.
new = new + b'  '
assert len(new) == len(old), f'len mismatch: {len(new)} vs {len(old)}'

# In-place replace (preserves all opcode bytes around it).
data[idx:idx+len(old)] = new
open(linda_path, 'wb').write(data)
print(f'Patched {linda_path}')

# Repack to converse.a (will use uncompressed mode).
r = subprocess.run([TOOL, '-r'], capture_output=True)
print(r.stdout.decode()[-200:] if r.stdout else '(no stdout)')
print(r.stderr.decode()[-200:] if r.stderr else '(no stderr)')
print('---')
import os
sz = os.path.getsize('converse.a')
print(f'converse.a size: {sz:,} bytes')
