#!/bin/bash
# -*- coding: utf-8 -*-

#
# This script executes multiple hyphenation passes over source data.
# Adapted from German hyphenation patterns project: git://repo.or.cz/wortliste.git
#
# Usage:
#
#   sh make-full-pattern.sh DICTIONARY_FILE TRANSLATE_FILE PARAMETERS_FILE
#
#
# Input:   DICTIONARY_FILE    a list of hyphenated words
#          TRANSLATE_FILE     for patgen, see patgen manpage
#          PARAMETERS_FILE    parameters to supply to patgen
#
# Output:  pattmp.[1-8]       patgen results
#          pattern.[0-8]      hyphenation patterns
#          pattern.[1-8].log  log data
#


set -e
#set -o pipefail

# Parameters for PATGEN, passes 1 to 8 sourced from PARAMETERS_FILE
source $3

rm -f pattern.0
touch pattern.0

for i in 1 2 3 4 5 6 7 8; do

  # Erzeuge Muster des aktuellen Levels.  Steuereingaben werden patgen
  # mittels einer Pipe übergeben.
  printf "%s\n%s\n%s\n%s" "${hyph_start_finish[$i]}" \
                          "${pat_start_finish[$i]}" \
                          "${good_bad_thres[$i]}" \
                          "y" \
  | ../patgen $1 pattern.$(($i-1)) pattern.$i $2 \
  | tee pattern.$i.log

  if [ "$i" -ge "${#good_bad_thres[@]}" ]
  then
    break
  fi

done

cp pattern.`expr ${#good_bad_thres[@]} - 1` pattern.final