import sys
from typing import IO, List, Tuple

def read_byte(f: IO):
    return f.read(1)[0]

def read_word(f: IO):
    return int.from_bytes(f.read(2), byteorder = 'little', signed = False)

def seek_addr(f: IO, addr: Tuple[int, int]):
    f.seek(addr[0] * 0x4000 + (addr[1] & 0x3FFF))

MAP_COUNT = 0xB5

def read_line_2bpp(f: IO):
    lobits = read_byte(f)
    hibits = read_byte(f)

    return [((lobits & (1 << i)) >> i) | (((hibits & (1 << i)) >> i) * 2) for i in reversed(range(8))]

def read_tile_2bpp(f: IO):
    return [read_line_2bpp(f) for _ in range(8)]

def write_image(filename: str, bitmap: List[List[int]], colors: List[Tuple[int, int, int]]):
    import png

    real_colors = [(((c & 0x1F) << 3), ((c & 0x3E0) >> 2), ((c & 0x7C00) >> 7)) for c in colors]

    with open(filename, 'wb') as f:
        w = png.Writer(
            size = (len(bitmap[0]), len(bitmap)),
            palette = real_colors,
            bitdepth = 8)

        w.write(f, bitmap)

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

        seek_addr(f, (1, 0x481F)) # terrain lists
        terrains = [read_word(f) for _ in range(MAP_COUNT)]

        for i in range(MAP_COUNT):
            print(f"map {i:02X}: {{ pal: {banks[i]:02X}:{palettes[i]:04X}, grid: {banks[i]:02X}:{grids[i]:04X}, tileset: {banks[i]:02X}:{tileset_tm[i]:04X}, gfx list: {banks[i]:02X}:{graphic_lists[i]:04X} }}")

            seek_addr(f, (banks[i], palettes[i]))
            colors = [read_word(f) for _ in range(4 * 8)]

            seek_addr(f, (banks[i], grids[i]))
            grid_w = read_byte(f)
            grid_h = read_byte(f)
            grid = [[read_byte(f) for _ in range(grid_w)] for _ in range(grid_h)]

            tilemap = [[0 for _ in range(grid_w * 2)] for _ in range(grid_h * 2)]
            attrmap = [[0 for _ in range(grid_w * 2)] for _ in range(grid_h * 2)]

            for iy in range(grid_h):
                for ix in range(grid_w):
                    metatile = grid[iy][ix]
                    seek_addr(f, (banks[i], tileset_tm[i] + 8 * metatile))

                    tilemap[iy * 2 + 0][ix * 2 + 0] = read_byte(f)
                    tilemap[iy * 2 + 0][ix * 2 + 1] = read_byte(f)
                    tilemap[iy * 2 + 1][ix * 2 + 0] = read_byte(f)
                    tilemap[iy * 2 + 1][ix * 2 + 1] = read_byte(f)
                    attrmap[iy * 2 + 0][ix * 2 + 0] = read_byte(f)
                    attrmap[iy * 2 + 0][ix * 2 + 1] = read_byte(f)
                    attrmap[iy * 2 + 1][ix * 2 + 0] = read_byte(f)
                    attrmap[iy * 2 + 1][ix * 2 + 1] = read_byte(f)

            graphics_addrs = {}

            seek_addr(f, (banks[i], graphic_lists[i]))

            while True:
                head = read_byte(f)

                if head == 0:
                    break

                is_bank1 = (head & 1)
                base_addr = ((head & 0xFE) << 8)
                rom_addr = read_word(f)

                for tile in range(0x80):
                    graphics_addrs[(is_bank1, base_addr + tile * 0x10)] = rom_addr + 0x10 * tile

            bitmap = [[0 for _ in range(16 * grid_w)] for _ in range(16 * grid_h)]

            for iy, (tile_list, attr_list) in enumerate(zip(tilemap, attrmap)):
                for ix, (tile, attr) in enumerate(zip(tile_list, attr_list)):
                    vram_bank = (attr & 8) >> 3
                    vram_addr = id2vram0(tile)

                    if (vram_bank, vram_addr) not in graphics_addrs:
                        continue

                    seek_addr(f, (banks[i], graphics_addrs[(vram_bank, vram_addr)]))

                    tile_2bpp = read_tile_2bpp(f)
                    pal = attr & 7

                    for ity in range(8):
                        for itx in range(8):
                            bitmap[iy * 8 + ity][ix * 8 + itx] = tile_2bpp[ity][itx] + pal * 4

            write_image(f"map_{i}_{i:02X}.png", bitmap, colors)

if __name__ == '__main__':
    main(sys.argv)
