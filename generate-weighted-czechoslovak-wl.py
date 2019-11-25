# generates cssk-all-weighted.wlh. works with utf-8.

OUTPUT = "out/cssk-all-weighted.wlh"

CORRECTIONS = "src/sk-corrections.wlh"
JOIN = "out/cssk-all-join.wlh"
INTERSECT = "out/cssk-all-intersect.wlh"

WEIGHT_JOIN = 1
WEIGHT_INTERSECT = 2
WEIGHT_CORRECTIONS = 4

def remove_hyphens(word):
    return word.replace("-","")

def add_wordlist_to_list(words, wordlist_filename, weight, corrections):
    with open(wordlist_filename) as f:
        for word in f.readlines():
            if remove_hyphens(word) in corrections:
                word = corrections[remove_hyphens(word)]
            if word in words:
                words[word] = words[word] + weight
            else:
                words[word] = weight

    return words

# 1. load corrections

with open(CORRECTIONS) as f:
    corrections_raw = f.readlines()


corrections = {} # unhyphenated -> hyphenated. small.

for correction in corrections_raw:
    corrections[remove_hyphens(correction)] = correction

del corrections_raw

words = {} # hyphenated word -> frequency

# load wordlist, add to words with given frequency

words = add_wordlist_to_list(words, JOIN, WEIGHT_JOIN, corrections)
words = add_wordlist_to_list(words, INTERSECT, WEIGHT_INTERSECT, corrections)
words = add_wordlist_to_list(words, CORRECTIONS, WEIGHT_CORRECTIONS, corrections) # to make sure words in corrections that are not present in the wordlists still get added to training with adequate weight

# generate the weighted czechoslovak wlh for patgen

output = open(OUTPUT, "w")
for word, freq in words.items():
    if freq > 9: freq = 9
    output.write(str(freq)+word)
