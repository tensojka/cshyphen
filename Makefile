PYTHON=python3
PATTERNTOUSE=out/czhyphen1-patched.pat
WORDLISTTOUSE=out/cstenten.wlh

# Make cheatsheet :)
# $@ output
# $< input

.SECONDARY: 

%.wleval: %.pat out/ujc.wlh
	recode UTF8..ISO-8859-2 out/ujc.wlh
	printf "%s\n%s\n%s\n%s" "1 1" \
	"1 9" \
	"1 1 10000" \
	"y" \
	| ./patgen out/ujc.wlh $< /dev/null czech.tra \
	| tee $@
	recode ISO-8859-2..UTF8 out/ujc.wlh

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

clean:
	rm -rf out
	mkdir out
