import sys
from typing import IO, List, Tuple

def read_byte(f: IO):
    return f.read(1)[0]

def read_word(f: IO):
    return int.from_bytes(f.read(2), byteorder = 'little', signed = False)

def seek_addr(f: IO, addr: Tuple[int, int]):
    f.seek(addr[0] * 0x4000 + (addr[1] & 0x3FFF))

MAP_COUNT = 0xB5

def id2vram0(id: int):
    return 0x8800 + ((id * 0x10 + 0x800) % 0x1000)

def id2vram1(id: int):
    return 0x8000 + id * 0x10

def main(args: List[str]):
    try:
        filepath = args[1]

    except IndexError:
        sys.exit(f"Usage: [python 3] {args[0]} FILEPATH")

    with open(filepath, 'rb') as f:
        seek_addr(f, (1, 0x4058)) # banks
        banks = [read_byte(f) for _ in range(MAP_COUNT)]

        seek_addr(f, (1, 0x410D)) # palettes
        palettes = [read_word(f) for _ in (range(MAP_COUNT))]

        seek_addr(f, (1, 0x4277)) # grids
        grids = [read_word(f) for _ in range(MAP_COUNT)]

        seek_addr(f, (1, 0x43E1)) # tile tms
        tileset_tm = [read_word(f) for _ in range(MAP_COUNT)]

        seek_addr(f, (1, 0x454B)) # graphic lists
        graphic_lists = [read_word(f) for _ in range(MAP_COUNT)]

        seek_addr(f, (1, 0x46B5)) # actors?
        unk_46B5 = [read_word(f) for _ in range(MAP_COUNT)]

        seek_addr(f, (1, 0x481F)) # terrain lists
        terrains = [read_word(f) for _ in range(MAP_COUNT)]

        seek_addr(f, (1, 0x4989)) # unk
        unk_4989 = [read_word(f) for _ in range(MAP_COUNT)]

        seek_addr(f, (1, 0x4AF3)) # actors again?
        unk_4AF3 = [read_word(f) for _ in range(MAP_COUNT)]

        datamap = {}

        for i in range(MAP_COUNT):
            datamap[(banks[i], palettes[i])] = (f"Map_{i:02X}.palette", 0x80)

            seek_addr(f, (banks[i], grids[i]))
            grid_w = read_byte(f)
            grid_h = read_byte(f)
            grid = [[read_byte(f) for _ in range(grid_w)] for _ in range(grid_h)]

            datamap[(banks[i], grids[i])] = (f"Map_{i:02X}.metatile_grid", (grid_w * grid_h) + 2)

            max_metatile = 0

            for iy in range(grid_h):
                for ix in range(grid_w):
                    metatile = grid[iy][ix]
                    max_metatile = max(max_metatile, metatile + 1)

            datamap[(banks[i], tileset_tm[i])] = (f"Map_{i:02X}.tileset", max_metatile * 8)
            datamap[(banks[i], terrains[i])] = (f"Map_{i:02X}.terrain", max_metatile)

            graphics_addrs = []
            graphics_addr_map = {}

            seek_addr(f, (banks[i], graphic_lists[i]))

            while True:
                head = read_byte(f)

                if head == 0:
                    break

                is_bank1 = (head & 1) # never set but technically supported! (we don't care)
                base_addr = ((head & 0xFE) << 8)
                rom_addr = read_word(f)

                graphics_addrs.append(base_addr)
                graphics_addr_map[base_addr] = rom_addr

            datamap[(banks[i], graphic_lists[i])] = (f"Map_{i:02X}.chr_list", 3 * len(graphics_addrs) + 1)

            max_tiles = {addr: 0 for addr in graphics_addrs}

            for metatile in range(max_metatile):
                seek_addr(f, (banks[i], tileset_tm[i] + 8 * metatile))

                for _ in range(4):
                    tile = read_byte(f)
                    vram = id2vram0(tile)

                    tile_base = tile & 0x7F
                    vram_base = vram & 0xF800

                    max_tiles[vram_base] = max(max_tiles[vram_base], tile_base + 1)

            for addr in graphics_addrs:
                datamap[(banks[i], graphics_addr_map[addr])] = (f"Map_{i:02X}.chr_{addr:04X}", max_tiles[addr] * 0x10)

            seek_addr(f, (banks[i], unk_46B5[i]))

            max_actors = 0

            while True:
                head = read_byte(f)

                if (head & 1) != 0:
                    break

                max_actors = max_actors + 1
                f.read(15)

            datamap[(banks[i], unk_46B5[i])] = (f"Map_{i:02X}.actors_1", max_actors * 0x10 + 1)

            seek_addr(f, (banks[i], unk_4AF3[i]))

            max_actors = 0

            while True:
                head = read_byte(f)

                if (head & 1) != 0:
                    break

                max_actors = max_actors + 1
                f.read(15)

            datamap[(banks[i], unk_4AF3[i])] = (f"Map_{i:02X}.actors_2", max_actors * 0x10 + 1)

            seek_addr(f, (banks[i], unk_4989[i]))

            max_events = 0

            while True:
                head = read_byte(f)

                if head == 0xFF:
                    break

                max_events = max_events + 1
                f.read(12)

            datamap[(banks[i], unk_4989[i])] = (f"Map_{i:02X}.events", max_events * 13 + 1)

        last_bank = 0
        last_addr = 0

        for bank, addr in sorted(datamap.keys()):
            if last_bank == bank and (last_addr != addr):
                print(f"# GAP @ {bank:02X}:{last_addr:04X} (len = {addr - last_addr:02X})")

            name, size = datamap[(bank, addr)]
            print(f"{bank:02X}:{addr:04X} ({bank * 0x4000 + (addr & 0x3FFF):06X}) {name} (len = {size:04X})")

            last_bank = bank
            last_addr = addr + size

if __name__ == '__main__':
    main(sys.argv)
