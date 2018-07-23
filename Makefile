# Minimal makefile for VICTA
#
SHELL=/bin/bash

.PHONY: dist doc
dist: 
	python setup.py bdist_wheel --dist-dir="dist" --universal
	rm -rf build 
	rm -rf VICTA.egg-info 

test:
	
	pytest

doc:
	
	cd docs && sphinx-apidoc -f -o "."  "../victa"
	cd docs && sphinx-build -M html "." 
	pandoc -o README.docx -f markdown -t docx README.md --reference-docx=src/docs/reference.docx

