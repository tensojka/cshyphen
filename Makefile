PYTHON=python3
PATTERNTOUSE=out/skhyphen.pat
WORDLISTTOUSE=src/cs-all-cstenten.wlh
VALIDATIONWL=src/cs-lemma-ujc-4.wlh

.SECONDARY: 

%.wleval: %.pat $(VALIDATIONWL)
	recode UTF8..ISO-8859-2 $(VALIDATIONWL)
	printf "%s\n%s\n%s\n%s" "1 1" \
	"1 9" \
	"1 1 10000" \
	"y" \
	| ./patgen $(VALIDATIONWL) $< /dev/null czech.tra \
	| tee $@
	recode ISO-8859-2..UTF8 $(VALIDATIONWL)

%.pat: %.par $(WORDLISTTOUSE) czech.tra make-full-pattern.sh
	rm -f out/pattern.*
	recode UTF8..ISO-8859-2 $(WORDLISTTOUSE)
	(cd out && bash ../make-full-pattern.sh ../$(WORDLISTTOUSE) ../czech.tra ../$<)
	recode ISO-8859-2..UTF8 $(WORDLISTTOUSE)
	mv out/pattern.final $@

out/%: src/%
	cp $< $@

# hyphenate
%.wlh: %.wls $(PATTERNTOUSE)
	recode UTF8..ISO-8859-2 $<
	printf "%s\n%s\n%s\n%s" "1 1" \
	"1 1" \
	"1 1 1" \
	"y" \
	| ./patgen $< $(PATTERNTOUSE) /dev/null czech.tra
	mv pattmp.1 $@
	recode ISO-8859-2..UTF8 $<
	recode ISO-8859-2..UTF8 $@
	sed -i -e 's/\./-/g' $@

%.wls: %.wl wl2wls.py
	$(PYTHON) wl2wls.py $@ $<

%.wlh: %.wl wl2wlh.py
	$(PYTHON) wl2wlh.py $@ $<

out/cstenten%.frqwl: src/cstenten%.frqwl # lowercase
	cp $< $@
	sed -i -e 's/./\L\0/g' $@

out/cstenten.wls: out/cstenten17.frqwl out/cstenten12.frqwl frqwl2wls.py
	$(PYTHON) frqwl2wls.py $@ out/cstenten17.frqwl out/cstenten12.frqwl --minfreq=100

out/cstenten.frqwl: out/cstenten17.frqwl out/cstenten12.frqwl frqwl2wls.py
	$(PYTHON) frqwl2wls.py -k $@ out/cstenten17.frqwl out/cstenten12.frqwl --minfreq=100

out/cssk-all-weighted.wlh: out/cssk-all-join.wlh out/cssk-all-intersect.wlh src/sk-corrections.wlh generate-weighted-czechoslovak-wl.py
	python3 generate-weighted-czechoslovak-wl.py

csskhyphen.pat: src/cs-sojka-correctoptimized.par out/cssk-all-weighted.wlh # make sure PATTERNTOUSE is good czech patterns
	rm -f out/pattern.*
	recode UTF8..ISO-8859-2 out/cssk-all-weighted.wlh
	(cd out && bash ../make-full-pattern.sh cssk-all-weighted.wlh ../czech.tra ../$<)
	recode ISO-8859-2..UTF8 out/cssk-all-weighted.wlh
	mv out/pattern.final $@

src/cs-all-cstenten.wls: cstenten.out #majka (morphological analyzer) output
	grep '^[$@]' /tmp/cstenten.out \
	| sed -e 's/\t/\n/g' \
	| sed -e '/[$@]/d' \
	| grep -xv '[0-9]*' > src/czbf.wls
	make -s out/ujc.wls
	cat out/ujc.wls >> src/czbf.wls
	sort -u -o src/czbf.wls src/czbf.wls

src/cs-all-cstenten.wlh:
	touch $@

out/cstentenfreq.wlh: out/cstenten.wlh
	python3 add-frequencies-to-wlh.py src/cstenten17.frqwl $< $@

clean:
	rm -rf out
	mkdir out
