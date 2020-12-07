file_name = template

.PHONY: all
all:
	#pdflatex $(file_name).tex
	#bibtex $(file_name)
	#pdflatex $(file_name).tex
	pdflatex $(file_name).tex
	evince $(file_name).pdf &

.PHONY: clean
clean:
	rm -f $(file_name).[^t]* $(file_name).toc

.PHONY: cln
cln: clean
