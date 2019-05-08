#!/bin/bash
# -*- coding: utf-8 -*-

#
# Dieses Skript generiert deutsche Trennmuster.
#
# Aufruf:
#
#   sh make-full-pattern.sh words.hyphenated german.tr
#
#
# Eingabe: words.hyphenated   Liste von getrennten Wörtern.
#          german.tr          Translationsdatei für patgen.
#
# Ausgabe: pattmp.[1-8]       patgen-Resultate.
#          pattern.[0-8]      Trennmuster -- pattern.8 ist die finale
#                             Trennmusterdatei.
#          pattern.[1-8].log  Log-Dateien.
#          pattern.rules      Die patgen-Parameter in kompakter Form.
#


# Die Parameter für patgen für die Level eins bis acht.

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


# Erzeuge leere Startmuster, lösche Datei mit patgen-Parametern.
rm -f pattern.0 pattern.rules
touch pattern.0

for i in 1 ; do

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

# eof
