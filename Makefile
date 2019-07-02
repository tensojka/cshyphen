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

clean:
	rm -rf out
	mkdir out