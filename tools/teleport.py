#!/usr/bin/env python3
"""
Teleport the Avatar (actor #1) to be adjacent to a target NPC in U6 savegame.

OBJLIST format (offset 0x100): 256 actors × 3 bytes each
  byte0 = x[7:0]
  byte1 = ((y[5:0]) << 2) | x[9:8]
  byte2 = ((z[3:0]) << 4) | y[9:6]

Usage:
  teleport.py to-npc <npc_id> [--objlist PATH]
  teleport.py to-xyz <x> <y> [<z>] [--objlist PATH]
  teleport.py list-npcs        # show known important NPC positions
"""
import sys, os, argparse, shutil

DEFAULT_OBJLIST = '/home/anr2/u6-cht/working/game/SAVEGAME/OBJLIST'
AVATAR = 1

# Known NPC ids (from CONVERSE.A unpack)
NPC_NAMES = {
    1: 'Avatar', 2: 'Dupre', 3: 'Shamino', 4: 'Iolo', 5: 'Lord British',
    6: 'Nystul', 7: 'Geoffrey', 8: 'Tholden', 9: 'Sherry', 10: 'Chuckles',
    11: 'Kenneth', 12: 'Nan', 13: 'Ariana', 14: 'Matt', 15: 'Anya',
    16: 'Gwenneth', 17: 'Peyton', 18: 'Max', 19: 'Lazeena',
    33: 'Mariah', 187: 'Linda',
}


def read_pos(data, idx):
    off = 0x100 + idx * 3
    b1, b2, b3 = data[off], data[off + 1], data[off + 2]
    x = b1 + ((b2 & 0x03) << 8)
    y = ((b2 & 0xfc) >> 2) + ((b3 & 0x0f) << 6)
    z = (b3 & 0xf0) >> 4
    return x, y, z


def write_pos(data, idx, x, y, z):
    off = 0x100 + idx * 3
    data[off]     = x & 0xFF
    data[off + 1] = ((x >> 8) & 0x03) | ((y & 0x3F) << 2)
    data[off + 2] = ((y >> 6) & 0x0F) | ((z & 0x0F) << 4)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('cmd', choices=['to-npc', 'to-xyz', 'list-npcs'])
    ap.add_argument('arg1', nargs='?', default=None)
    ap.add_argument('arg2', nargs='?', default=None)
    ap.add_argument('arg3', nargs='?', default='0')
    ap.add_argument('--objlist', default=DEFAULT_OBJLIST)
    ap.add_argument('--no-backup', action='store_true')
    args = ap.parse_args()

    data = bytearray(open(args.objlist, 'rb').read())

    if args.cmd == 'list-npcs':
        for npc_id, name in NPC_NAMES.items():
            x, y, z = read_pos(data, npc_id)
            print(f'  NPC {npc_id:3d}: ({x:4d},{y:4d},{z:1d}) {name}')
        return

    avatar_pos = read_pos(data, AVATAR)
    print(f'Avatar @ {avatar_pos}')

    if args.cmd == 'to-npc':
        npc_id = int(args.arg1)
        if npc_id not in NPC_NAMES:
            print(f'(warn: unknown NPC id {npc_id})')
        target = read_pos(data, npc_id)
        print(f'Target NPC {npc_id} ({NPC_NAMES.get(npc_id,"?")}) @ {target}')
        # Place avatar 1 tile west of NPC (NPC sees east)
        new_x, new_y, new_z = target[0] - 1, target[1], target[2]
    else:  # to-xyz
        new_x = int(args.arg1)
        new_y = int(args.arg2)
        new_z = int(args.arg3)

    print(f'Teleport avatar to ({new_x},{new_y},{new_z})')

    if not args.no_backup:
        bak = args.objlist + '.teleport.bak'
        if not os.path.exists(bak):
            shutil.copy(args.objlist, bak)
            print(f'Backed up to {bak}')

    write_pos(data, AVATAR, new_x, new_y, new_z)
    open(args.objlist, 'wb').write(bytes(data))
    print(f'Wrote {args.objlist}')

    # Verify
    data2 = open(args.objlist, 'rb').read()
    px, py, pz = read_pos(data2, AVATAR)
    print(f'Avatar now @ ({px},{py},{pz})')


if __name__ == '__main__':
    main()
