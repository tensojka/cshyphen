PYTHON=python3

runpatgen: out/dict.wlh src/czech.tra make-full-pattern.sh
	(cd out && sh ../make-full-pattern.sh dict ../czech.tra)

out/dict.wlh: src/deleni.wl generate-dict.py
	mkdir -p out
	$(PYTHON) generate-dict.py
	#recode UTF8..ISO-8859-2 out/dict

out/cstenten.wls: src/cstenten17.frqwl src/cstenten12.frqwl frqwl2wls.py
	$(PYTHON) frqwl2wls.py $@ src/cstenten17.frqwl src/cstenten12.frqwl --minfreq=100

clean:
	rm -rf out
