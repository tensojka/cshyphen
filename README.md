# Czech hyphenation patterns

Inspired by German hyphenation patterns, see [git repo](http://repo.or.cz/wortliste.git).

Carefully check encodings; Unicode can't be used since patgen expects each character to be 1 byte. Output encoding is latin-2. To convert files back to the 21st century, use `recode ISO-8859-2..UTF8 FILENAME`.

## Prerequisites

- recode (`dnf install recode`)
- python3
- make
- 

## Usage

`make`

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

lang-type-subtype-version.\['wl'/'pat'/'wleval]