import sys

def has_forbidden_character(string):
    try:
        string.encode('iso-8859-2')
    except UnicodeEncodeError:
        return True
    return False

if not (len(sys.argv[1]) > 0 and len(sys.argv[2]) > 0):
    print("Supply output file and input file.", file=sys.stderr)
    exit(1)

with open(sys.argv[1], 'w') as of:
    with open(sys.argv[2]) as inpf:
        for line in inpf:
            if has_forbidden_character(line):
                continue
            split = line.split(";")
            try:
                of.write(split[1].replace('=','-')) # TODO what about '-' when part of word?
            except IndexError:
                pass
