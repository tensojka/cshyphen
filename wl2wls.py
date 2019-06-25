# Converts this:
#
# Aabye;Aa=bye
# Aachen;Aa=chen
# aachenský;aa=chen=ský
# aak;aak
# aalen;aa=len
#
# to this:
#
# Aabye
# Aachen
# aachenský
# aak
# aalen

# Yes, this could be done with awk.

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

with open(sys.argv[2]) as inpf:
    with open(sys.argv[1], 'w') as outf:
        for line in inpf:
            if has_forbidden_character(line):
                continue
            line = line.replace("=","-")
            split = line.split(";")
            outf.write(split[0]+"\n") 