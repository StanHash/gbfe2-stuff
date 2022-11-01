import sys, re

def parse_map_file_and_get_compare_blocks(f):
    segment_offset = -1
    segment_addr = 0

    blocks = []

    for line in f.readlines():
        if len(line) == 0:
            continue

        if line[0] == ' ':
            # starts with space, this is within a segment

            if segment_offset < 0:
                continue

            m = re.match(r'\s+SECTION:\s+\$(?P<first>[0-9A-Fa-f]+)-\$(?P<last>[0-9A-Fa-f]+)\s+\(\$\w+ bytes\) \["(?P<name>.+)"\]', line)

            if m != None:
                addr = int(m.group('first'), base = 16)
                size = int(m.group('last'), base = 16) + 1 - addr
                name = m.group('name')

                blocks.append((segment_offset + addr - segment_addr, size, name))

        else:
            m = re.match(r"(?P<kind>\w+)\s+bank\s+#(?P<bank>\w+):", line)

            if m != None:
                kind = m.group("kind")
                bank = int(m.group("bank"))

                if kind == "ROM0":
                    segment_offset = 0x4000 * bank
                    segment_addr = 0

                elif kind == "ROMX":
                    segment_offset = 0x4000 * bank
                    segment_addr = 0x4000

                else:
                    segment_offset = -1
                    segment_addr = 0

    return blocks

def main():
    try:
        map_file = sys.argv[1]
        rom_a_file = sys.argv[2]
        rom_b_file = sys.argv[3]

    except:
        sys.exit(f"Usage: [python 3] {sys.argv[0]} MAP BASEROM NEWROM")

    with open(map_file, 'r') as f:
        blocks = parse_map_file_and_get_compare_blocks(f)

    with open(rom_a_file, 'rb') as f:
        rom_a = f.read()

    with open(rom_b_file, 'rb') as f:
        rom_b = f.read()

    ok = True

    for offset, length, name in blocks:
        for i in range(offset, offset + length):
            if rom_a[i] != rom_b[i]:
                print(f"{name}+{i - offset:04X} :: {rom_a[i]:02X} {rom_b[i]:02X}")
                ok = False

    if ok:
        print("Ok!")

if __name__ == '__main__':
    main()
