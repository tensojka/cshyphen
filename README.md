# Czech hyphenation patterns

Inspired by German hyphenation patterns, see [git repo](git://repo.or.cz/wortliste.git).

Input files are expected to be encoded in 21st-century format. Output encoding is latin-2. To convert files back to the 21st century, use `recode ISO-8859-2..UTF8 FILENAME`.

## Prerequisites

- recode (`dnf install recode`)
- python3

## Usage

`make`