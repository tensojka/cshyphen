# Language-independent system for hyphenation pattern generation with `patgen`

See paper [Unreasonable Effectiveness of Pattern Generation](paper.pdf).

Now working on implementing ideas described in paper [Towards Universal Hyphenation Patterns](paper-towards-universal.pdf).

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

## Licenses

The project is available under the MIT license. Files src/cs-all-cstenten.wls, src/cs-all-cstenten.wl and src/cstenten1[2,7].frqwl are available under the license [CC-BY-NC-SA](https://creativecommons.org/licenses/by-nc-sa/3.0/legalcode). For commercial use of the cstenten word lists, contact inquiries@sketchengine.eu.