# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXBUILD   = sphinx-build
SPHINXAPIDOC   = sphinx-apidoc
SPHINXPROJ    = VICTA
SOURCEDIR     = .
BUILDDIR      = ../../build
PROJDIR     = ../victa

%: Makefile
	@$(SPHINXAPIDOC) -f -o "$(BUILDDIR)"  "$(PROJDIR)"
	@$(SPHINXBUILD) -M html "$(SOURCEDIR)" "$(BUILDDIR)"