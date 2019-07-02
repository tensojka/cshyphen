PYTHON=python3
PATTERNTOUSE=out/czhyphen1-libreoffice.pat

# Make cheatsheet :)
# $@ output
# $< input

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

%.wlh: %.wl wl2wlh.py
	$(PYTHON) wl2wlh.py $@ $<
#	sed -i -e 's/-/=/g' $@

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