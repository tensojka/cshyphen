PYTHON=python3
PATTERNTOUSE=out/czhyphen1-libreoffice.pat

runpatgen: out/dict.wlh czech.tra make-full-pattern.sh
	rm out/pattern.*
	(cd out && sh ../make-full-pattern.sh dict ../czech.tra)

out/%: src/%
	cp $< $@

# hyphenate
%.wlh: %.wls
	recode UTF8..ISO-8859-2 $<
	printf "%s\n%s\n%s\n%s" "1 1" \
	"1 1" \
	"1 1 1" \
	"y" \
	| ../patgen $< $(PATTERNTOUSE) /dev/null czech.tra
	mv pattmp.1 $@
	recode ISO-8859-2..UTF8 $<
	recode ISO-8859-2..UTF8 $@

%.wls: %.wl
	$(PYTHON) wl2wls.py $@ $<

out/cstenten.wls: src/cstenten17.frqwl src/cstenten12.frqwl frqwl2wls.py
	$(PYTHON) frqwl2wls.py $@ src/cstenten17.frqwl src/cstenten12.frqwl --minfreq=100

clean:
	rm -rf out
