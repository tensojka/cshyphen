PYTHON=python3

runpatgen: out/dict src/czech.tra make-full-pattern.sh
	(cd out && sh ../make-full-pattern.sh dict ../czech.tra)

out/dict: src/deleni.txt generate-dict.py
	mkdir -p out
	$(PYTHON) generate-dict.py
	recode UTF8..ISO-8859-2 out/dict

clean:
	rm -rf out
