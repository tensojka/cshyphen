""" Adapted from https://nedbatchelder.com/code/modules/hyphenate.py """

import re
import random
from typing import List
import datetime
import os
from statistics import fmean 
from typing import Tuple

class Hyphenator:
    def __init__(self, patterns: List[str], exceptions=''):
        self.tree = {}
        for pattern in patterns:
            self._insert_pattern(pattern)

        self.exceptions = {}
        for ex in exceptions.split():
            # Convert the hyphenated pattern into a point array for use later.
            self.exceptions[ex.replace('-', '')] = [0] + [ int(h == '-') for h in re.split(r"[a-z]", ex) ]

    def _insert_pattern(self, pattern):
        # Convert the a pattern like 'a1bc3d4' into a string of chars 'abcd'
        # and a list of points [ 0, 1, 0, 3, 4 ].
        chars = re.sub('[0-9]', '', pattern)
        points = [ int(d or 0) for d in re.split("[.\D]", pattern) ]

        # Insert the pattern into the tree.  Each character finds a dict
        # another level down in the tree, and leaf nodes have the list of
        # points.
        t = self.tree
        for c in chars:
            if c not in t:
                t[c] = {}
            t = t[c]
        t[None] = points

    def hyphenate_word(self, word):
        """ Given a word, returns a list of pieces, broken at the possible
            hyphenation points.
        """
        # Short words aren't hyphenated.
        if len(word) <= 4:
            return [word]
        # If the word is an exception, get the stored points.
        if word.lower() in self.exceptions:
            points = self.exceptions[word.lower()]
        else:
            work = '.' + word.lower() + '.'
            points = [0] * (len(work)+1)
            for i in range(len(work)):
                t = self.tree
                for c in work[i:]:
                    if c in t:
                        t = t[c]
                        if None in t:
                            p = t[None]
                            for j in range(len(p)):
                                points[i+j] = max(points[i+j], p[j])
                    else:
                        break
            # No hyphens in the first two chars or the last two.
            points[1] = points[2] = points[-2] = points[-3] = 0

        # Examine the points to build the pieces list.
        pieces = ['']
        for c, p in zip(word, points[2:]):
            pieces[-1] += c
            if p % 2:
                pieces.append('')
        return pieces


# Given a filename of a hyphenated .wlh wordlist and a filename of
# patterns to use, report how many hyphenation points were correctly found.
# Returns (good, bad, missed)
def validate(wlh, pat):
    patfile = open(pat, "r")
    patterns = patfile.read().split('\n')
    hyphenator = Hyphenator(patterns)
    wlhfile = open(wlh, "r")
    good = 0  # present in validation wl and patterns
    bad = 0  # not present in validation wl, but in patterns
    missed = 0  # present in validation wl, but not in patterns
    for line in wlhfile.readlines():
        if line[0].isnumeric:
            line = line[1:]
        valid_hyph_word = line[:-1]
        word = valid_hyph_word.replace("-", "")
        pat_hyph_word = "-".join(hyphenator.hyphenate_word(word))
        pat_hyph_points = [pos for pos, char in enumerate(pat_hyph_word) if char == "-"]
        valid_hyph_points = [pos for pos, char in enumerate(valid_hyph_word) if char == "-"]
        valid_separators_encountered = 0
        offset = 0
        for pos, char in enumerate(valid_hyph_word):
            try:
                if char == "-" and pat_hyph_word[pos+offset] == "-":
                    if pos > 1 and pos < (len(pat_hyph_word)+offset-2):
                        good += 1
                elif char == "-" and pat_hyph_word[pos+offset] != "-":
                    if pos > 1 and pos < (len(pat_hyph_word)+offset-2):
                        missed += 1
                    offset -= 1
                elif char != "-" and pat_hyph_word[pos+offset] == "-":
                    if pos > 1 and pos < (len(pat_hyph_word)+offset-2):
                        bad += 1
                    offset += 1
            except IndexError:
                print("Val: "+valid_hyph_word)
                print("Pat: "+pat_hyph_word)


        #if valid_hyph_word != pat_hyph_word:
        #    print(valid_hyph_points)
        #    print(pat_hyph_points)
        #    print("Val: "+valid_hyph_word)
        #    print("Pat: "+pat_hyph_word)
    #total = good + missed + bad
    #print("good: " + str(good) + ", good %: " + str(round(100*(good/total),2)))
    #print("missed: " + str(missed) + ", missed %: " + str(round(100*(missed/total),2)))
    #print("bad: " + str(bad) + ", bad %: " + str(round(100*(bad/total),2)))
    return (good, bad, missed)


def k_cross_val(k, seed) -> Tuple[float, float, float]:
    start = datetime.datetime.now()
    passes = []
    for i in range(1, k+1):
        random.seed(seed)
        with open("out/holdout.wlh", "w") as holdout:
            with open("out/training.wlh", "w") as training:
                with open("out/cssk-all-weighted.wlh","r") as f:
                    for line in f:
                        r = random.randint(1, 10)
                        if r == i:
                            holdout.write(line)
                        else:
                            training.write(line)
        os.system("make out/training.pat")
        good, bad, missed = validate("out/holdout.wlh", "out/training.pat")
        total = good + bad + missed
        good_pct = 100*(good/total)
        bad_pct = 100*(bad/total)
        missed_pct = 100*(missed/total)
        passes.append((good_pct, bad_pct, missed_pct))
        os.system("rm out/training.pat")
    assert len(passes) == k
    print(str(k)+" passes done")
    print("Took: "+str(datetime.datetime.now()-start))
    return passes
    

wlh = "src/cs-lemma-ujc-4.wlh"

#validate("out/cssk-all-weighted.wlh", "out/csskhyphen.pat")
#print("ground truth: "+wlh)
#print("cssk results:")
#validate(wlh, "out/csskhyphen.pat")

wlh = "out/cssk-all-weighted.wlh"

#print("---------")
#print("ground truth: "+wlh)
#print("cssk results:")
#validate(wlh, "out/csskhyphen.pat")