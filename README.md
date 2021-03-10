# Towards Universal Hyphenation Patterns: Czechoslovak hyphenation patterns

## *Why* create czechoslovak hyphenation patterns?

Current Czech patterns were generated in 1995. Not only has the language evolved, but better training data for the patterns became available, making development of superior patterns possible. Why not generate Czech patterns only?

There is no reliable hyphenated wordlist available for Slovak to serve as training data. Whereas the Institute of the Czech Language provided a hyphenated form for every word in its database, there is no equivalent resource available for Slovak.

Because the languages are very similar and there are nearly no words that have the same spelling but different hyphenation, we can generate patterns that achieve better results than both current monolingual patterns.

## About

The first paper [Unreasonable Effectiveness of Pattern Generation](paper.pdf) describes how we bootstrapped the generation of Czech hyphenation patterns. Second paper [Towards Universal Hyphenation Patterns](paper-towards-universal.pdf) expands on the idea of universal hyphenation patterns.

Inspired by German hyphenation patterns, see [git repo](http://repo.or.cz/wortliste.git).

## Usage: pregenerated patterns

You can find generated patterns in the file `csskhyphen.pat`.

## Pattern evaluation

See [Jupyter notebook](evaluation.ipynb).

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