# Language-independent system for hyphenation pattern generation with `patgen`

See paper [Unreasonable Effectiveness of Pattern Generation](paper.pdf).

Inspired by German hyphenation patterns, see [git repo](http://repo.or.cz/wortliste.git).

## Prerequisites

- GNU coreutils & friends
- recode
- python3
- make

## Filename endings in use

See sketch.jpg for a graphical overview.

- .wlh 
    - hyphenated word list
- .wls
    - newline separated list of unhyphenated words
- .wl
    - word;wo=rd
    - the format to be edited by humans
- .par
    - parameters for patgen
- .pat
    - generated pattern
- .wleval
    - patgen output after validation pass
    - contains validation statistics

## Naming scheme

lang-type-subtype-version.\[wl/pat/wleval]

.,$s/\([plkmnjhbgtvfžřčšrcdxszwq][\*\.-]\)s[\*\.-]ký/\1ský/g