# Generate a .wls (wordlist separated by newlines) from one or more frqwl

import argparse
import copy
from typing import Dict

def has_forbidden_character(string):
    try:
        string.encode('iso-8859-2')
    except UnicodeEncodeError:
        return True
    return False

def parse_frqwl(filename: str, inp1=None) -> Dict[str,int]:
    if inp1 != None:
        freq = copy.copy(inp1)
    else:
        freq = dict()
    with open(filename) as inpf:
        ln = 0

        for line in inpf:
            if has_forbidden_character(line):
                continue
            split = line.split("\t")
            try:
                if inp1 != None and split[0] not in inp1:
                    continue
                if split[0] in freq:
                    freq[split[0]] = freq[split[0]] + int(split[1])
                else:
                    freq[split[0]] = int(split[1])
                    
            except IndexError:
                raise ValueError("Invalid format of "+filename+" on line "+str(ln))
            ln += 1
    return freq

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

parser.add_argument("-k", action='store_true',
                    help='output frequencies')

args = parser.parse_args()

inp1 = parse_frqwl(args.inpf)
if args.inpf2 != None:
    freqmap = parse_frqwl(args.inpf2, inp1)
else:
    freqmap = inp1

out = [] # type: List[str]

for word, frequency in freqmap.items():
    if frequency >= args.minfreq:
        out.append(word)

with open(args.outf, 'w') as of:
    out.sort()
    for word in out:
        if args.k:
            of.write(word+"\t"+str(freqmap[word])+"\n")
        else:
            of.write(word+"\n")

if args.v:
    print("Words in input file 1: "+str(len(inp1)))
    print("Words in output: "+str(len(out)))