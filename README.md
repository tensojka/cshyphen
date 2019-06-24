# Czech hyphenation patterns

Inspired by German hyphenation patterns, see [git repo](http://repo.or.cz/wortliste.git).

Carefully check encodings; Unicode can't be used since patgen expects each character to be 1 byte. Output encoding is latin-2. To convert files back to the 21st century, use `recode ISO-8859-2..UTF8 FILENAME`.

## Prerequisites

- recode (`dnf install recode`)
- python3

## Usage

`make`

## Intermediate formats in use

- .wlh 
    - hyphenated word list
- .wls
    - newline separated list of unhyphenated words