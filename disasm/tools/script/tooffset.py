import sys, re

RE = re.compile(r'(?P<bank>[0-9A-Fa-f]{2}):(?P<addr>[0-9A-Fa-f]{4})')

def main(args):
    try:
        m = RE.match(args[1])

        bank = int(m.group('bank'), base = 16)
        addr = int(m.group('addr'), base = 16)

    except IndexError:
        sys.exit(f"Usage: [python 3] {args[0]} OFFSET")

    except ValueError:
        sys.exit(f"'{args[1]}' isn't a valid hexadecimal number")

    print(f"{bank * 0x4000 + (addr & 0x3FFF):X}")

if __name__ == '__main__':
    main(sys.argv)
