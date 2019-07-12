# Generate cstenten.wls from cstenten.out (majka output)

import argparse

def has_forbidden_character(string):
    try:
        string.encode('iso-8859-2')
    except UnicodeEncodeError:
        return True
    return False

def parse_line(text: str) -> str:
    """Parses one line into a word."""
    text = text.rstrip()
    if text[0] == "+":
        return text[1:]
    if text[0] == "@" or text[0] == "!" or text[0] == "$":
        w = text.split("\t")[1]
        if "#" in w:
            return w.split("#")[0].rstrip()
        else:
            return w
    raise ValueError("Invalid input: "+text)

parser = argparse.ArgumentParser()
parser.add_argument('outf', type=str,
                    help='wls output file')

parser.add_argument('inpf', type=str,
                    help='majka input file')

args = parser.parse_args()

words = set()

with open(args.inpf) as inpf:
    for line in inpf:
        words.add(parse_line(line))

assert len(words) > 0, "no words found"
words_ordered = list(words)
words_ordered.sort()
assert len(words) == len(words_ordered)

with open(args.outf, "w") as outf:
    for word in words_ordered:
        outf.write(word+"\n")
