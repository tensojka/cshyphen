PYTHON=python3

runpatgen: out/dict.wlh czech.tra make-full-pattern.sh
	rm out/pattern.*
	(cd out && sh ../make-full-pattern.sh dict ../czech.tra)

# hyphenate out/cstenten.wls
out/cstenten.wlh: out/cstenten.wls
	recode UTF8..ISO-8859-2 out/cstenten.wls
	printf "%s\n%s\n%s\n%s" "1 1" \
	"1 1" \
	"1 1 1" \
	"y" \
	| ../patgen out/cstenten.wls out/czhyphen1-libreoffice.pat /dev/null czech.tra
	mv pattmp.1 out/cstenten.wlh
	recode ISO-8859-2..UTF8 out/cstenten.wls
	recode ISO-8859-2..UTF8 out/cstenten.wlh

out/dict.wlh: src/deleni.wl generate-dict.py
	mkdir -p out
	$(PYTHON) generate-dict.py
	#recode UTF8..ISO-8859-2 out/dict

out/cstenten.wls: src/cstenten17.frqwl src/cstenten12.frqwl frqwl2wls.py
	$(PYTHON) frqwl2wls.py $@ src/cstenten17.frqwl src/cstenten12.frqwl --minfreq=100

clean:
	rm -rf out
