def has_forbidden_character(string):
    try:
        string.encode('iso-8859-2')
    except UnicodeEncodeError:
        return True
    return False

with open('out/dict', 'w') as of:
    with open('src/deleni.txt') as inpf:
        for line in inpf:
            if has_forbidden_character(line):
                continue
            split = line.split(";")
            try:
                of.write(split[1])
            except IndexError:
                pass
