with open('out/dict', 'w') as of:
    with open('src/deleni.txt') as inpf:
        for line in inpf:
            if line == "":
                continue
            split = line.split(";")
            of.write(split[1])