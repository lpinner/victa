# Minimal makefile for VICTA
#

BUILDDIR      = ../build
DISTDIR      = ../dist

.PHONY: dist
dist: 
	python setup.py sdist --dist-dir="$(DISTDIR)"
	python setup.py bdist_wheel --dist-dir="$(DISTDIR)" --bdist-dir="$(BUILDDIR)"
	rm -rf build 
	rm -rf VICTA.egg-info 

