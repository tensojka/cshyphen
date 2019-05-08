#!/bin/bash
# -*- coding: utf-8 -*-

#
# This script executes multiple hyphenation passes over source data.
# Adapted from German hyphenation patterns project: git://repo.or.cz/wortliste.git
#
# Usage:
#
#   sh make-full-pattern.sh DICTIONARY_FILE TRANSLATE_FILE
#
#
# Input:   DICTIONARY_FILE    a list of hyphenated words
#          TRANSLATE_FILE     for patgen, see patgen manpage
#
# Output:  pattmp.[1-8]       patgen results
#          pattern.[0-8]      hyphenation patterns -- pattern.8 is the final one
#          pattern.[1-8].log  log data
#          pattern.rules      patgen parameters used
#


# Parameters for PATGEN, passes 1 to 8

hyph_start_finish[1]='1 1'
hyph_start_finish[2]='2 2'
hyph_start_finish[3]='3 3'
hyph_start_finish[4]='4 4'
hyph_start_finish[5]='5 5'
hyph_start_finish[6]='6 6'
hyph_start_finish[7]='7 7'
hyph_start_finish[8]='8 8'

pat_start_finish[1]='1 5'
pat_start_finish[2]='2 6'
pat_start_finish[3]='3 7'
pat_start_finish[4]='4 8'
pat_start_finish[5]='5 9'
pat_start_finish[6]='6 10'
pat_start_finish[7]='7 11'
pat_start_finish[8]='8 12'

good_bad_thres[1]='1 1 1'
good_bad_thres[2]='1 2 1'
good_bad_thres[3]='1 1 1'
good_bad_thres[4]='1 4 1'
good_bad_thres[5]='1 1 1'
good_bad_thres[6]='1 6 1'
good_bad_thres[7]='1 4 1'
good_bad_thres[8]='1 8 1'


rm -f pattern.0 pattern.rules
touch pattern.0

for i in 1 2 3 4 5 6 7 8; do

  # Erzeuge Muster des aktuellen Levels.  Steuereingaben werden patgen
  # mittels einer Pipe übergeben.
  printf "%s\n%s\n%s\n%s" "${hyph_start_finish[$i]}" \
                          "${pat_start_finish[$i]}" \
                          "${good_bad_thres[$i]}" \
                          "y" \
  | patgen $1 pattern.$(($i-1)) pattern.$i $2 \
  | tee pattern.$i.log

  # Sammle verwendete patgen-Parameter in Datei.
  printf "%%   %s | %s | %s\n" "${hyph_start_finish[$i]}" \
                               "${pat_start_finish[$i]}" \
                               "${good_bad_thres[$i]}" \
  >> pattern.rules

done
