all: Formulario.pdf

Formulario.pdf: Formulario.tex
	pdflatex -interaction=nonstopmode Formulario.tex

watch:
	latexmk -pdf -pvc -interaction=nonstopmode Formulario.tex

clean:
	rm -f *.aux *.log *.out *.fls *.fdb_latexmk
