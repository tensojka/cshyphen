# Generate a .wls (wordlist separated by newlines) from one or more frqwl

import argparse

def has_forbidden_character(string):
    try:
        string.encode('iso-8859-2')
    except UnicodeEncodeError:
        return True
    return False

def parse_frqwl(filename, minfreq=0):
    wl = set()
    with open(filename) as inpf:
        ln = 0

        for line in inpf:
            if has_forbidden_character(line):
                continue
            split = line.split("\t")
            try:
                if int(split[1]) > minfreq:
                    wl.add(split[0])
            except IndexError:
                raise ValueError("Invalid format of "+filename+" on line "+str(ln))
            ln += 1
    return wl

parser = argparse.ArgumentParser()
parser.add_argument('outf', type=str,
                    help='wls output file')

parser.add_argument('inpf', type=str,
                    help='frqwl input file')

parser.add_argument('inpf2', type=str, nargs='?',
                    help='frqwl input file to intersect with the first')

parser.add_argument("--minfreq", type=int, nargs='?',
                    help='throw away words with frequency lower than')

parser.add_argument("-v", action='store_true',
                    help='verbose')

args = parser.parse_args()

inp1 = parse_frqwl(args.inpf, args.minfreq)
if args.inpf2 != None:
    inp2 = parse_frqwl(args.inpf2, args.minfreq)
    out = inp1.intersection(inp2)
else:
    out = inp1

if args.v:
    print("Words in input file 1: "+str(len(inp1)))
    print("Words in input file 2: "+str(len(inp2)))
    print("Words in output: "+str(len(out)))

with open(args.outf, 'w') as of:
    out = list(out)
    out.sort()
    for word in out:
        of.write(word+"\n")