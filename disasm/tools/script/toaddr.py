import sys

def main(args):
    try:
        off = int(args[1], base = 16)

    except IndexError:
        sys.exit(f"Usage: [python 3] {args[0]} OFFSET")

    except ValueError:
        sys.exit(f"'{args[1]}' isn't a valid hexadecimal number")

    b = off // 0x4000
    a = off & 0x3FFF

    if b > 0:
        a = a + 0x4000

    print(f"{b:02X}:{a:04X}")

if __name__ == '__main__':
    main(sys.argv)
