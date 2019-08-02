# this script reads a .frqwl and adds frequencies to a wordlist from a supplied .wl file.

import argparse
import copy
import math

DEFAULTFREQ = 10 # gets passed through log

def has_forbidden_character(string):
    try:
        string.encode('iso-8859-2')
    except UnicodeEncodeError:
        return True
    return False

def parse_frqwl(filename, inp1=None):
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

def strip_hyphens(withhyphens):
    return withhyphens.replace("-","").replace("\n","")

parser = argparse.ArgumentParser()
parser.add_argument('frqwl', type=str,
                    help='frequency wordlist')

parser.add_argument('inpwl', type=str,
                    help='wordlist without frequencies')

parser.add_argument('outwl', type=str,
                    help='output wordlist with frequencies')

args = parser.parse_args()

freqs = parse_frqwl(args.frqwl)

with open(args.outwl, "w") as outf:
    with open(args.inpwl, "r") as inpf:
        i = -1
        for line in inpf:
            i += 1
            if has_forbidden_character(line):
                print("skipping line "+str(i)+", has character outside latin-2")
                continue
            try:
                freq = freqs[strip_hyphens(line)]
            except KeyError:
                freq = DEFAULTFREQ 
            assert type(freq) is int
            outf.write(str(round(math.log(freq,10)))+line)
