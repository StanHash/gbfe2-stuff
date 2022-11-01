import enum
import sys, io
from typing import List, Sequence

PATTERN = (0, 2, 3, 4, 1, 1, 4, 4, 1, 1, 1, 1, 1, 1)

def search_pattern(data: bytes, pattern: Sequence[int]):
    for i in range(len(data) - len(pattern)):
        byte_map = {}
        found = True

        for j, patbyte in enumerate(pattern):
            byte = data[i + j]
            if patbyte in byte_map:
                if byte_map[patbyte] != byte:
                    found = False
                    break

                continue

            if byte in byte_map.values():
                found = False
                break

            byte_map[patbyte] = byte

        if found:
            yield i

def main(args: List[str]):
    try:
        filepath = args[1]

    except IndexError:
        sys.exit(f"Usage: [python 3] {args[0]} FILEPATH")

    with open(filepath, 'rb') as f:
        f.seek(0, io.SEEK_END)
        bank_count = (f.tell() + 0x3FFF) // 0x4000

        for bank in range(1, bank_count):
            f.seek(0x4000 * bank)
            data = f.read(0x4000)
            for off in search_pattern(data, PATTERN):
                print(f"{bank:02X}:{0x4000 + off:04X} ({bank * 0x4000 + off:X})")

if __name__ == '__main__':
    main(sys.argv)
