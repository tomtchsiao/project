FILES = $(addsuffix .pdf, $(basename $(wildcard *.tex)))
LATEX = xelatex
RM = rm -f
all: $(FILES) clean
%.pdf: %.tex
	$(LATEX) $<
	$(LATEX) $<
clean:
	$(RM) *.aux *.log *.nav *.out *.snm *.toc
cleanall:
	$(RM) *.pdf
.PHONY: all clean cleanall