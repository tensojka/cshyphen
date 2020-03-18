# Language-independent system for hyphenation pattern generation with `patgen`

The first paper [Unreasonable Effectiveness of Pattern Generation](paper.pdf) describes how we bootstrapped the generation of Czech hyphenation patterns. Second paper [Towards Universal Hyphenation Patterns](paper-towards-universal.pdf) expands on the idea of universal hyphenation patterns. Czechoslovak patterns were then published in an update of *Towards Universal*, [Data Driven Development of New Czechoslovak Hyphenation Patterns](cssk.pdf).

Inspired by German hyphenation patterns, see [git repo](http://repo.or.cz/wortliste.git).

## Usage: generation of Czechoslovak patterns

First, install prerequisites:

- GNU coreutils
- recode
- python3
- make

Then run `make clean; make`. `out/csskhyphen.pat` contains generated Czechoslovak patterns.

### File structure and naming scheme

Source files (made by humans) can be found in the directory `src/`. All machine-generated files can be generated into the directory `out/`.

Files are mostly named like this: `lang-type-subtype-version.\[wl/pat/wleval]`

We also use a few nonstandard file extensions.

- .wlh 
    - hyphenated word list
- .wls
    - newline separated list of unhyphenated words
- .wl
    - word;wo=rd
    - contains both unhyphenated and hyphenated words
- .par
    - parameters for patgen
- .pat
    - generated pattern
- .wleval
    - patgen output after validation pass
    - contains validation statistics

## Licenses

The project is available under the MIT license. Files src/cs-all-cstenten.wls, src/cs-all-cstenten.wl and src/cstenten1[2,7].frqwl are available under the license [CC-BY-NC-SA](https://creativecommons.org/licenses/by-nc-sa/3.0/legalcode). For commercial use of the cstenten word lists, contact inquiries@sketchengine.eu.