# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXBUILD   = sphinx-build
SPHINXAPIDOC   = sphinx-apidoc
SPHINXPROJ    = VICTA
SOURCEDIR     = .
BUILDDIR      = ../../apidoc
PROJDIR     = ../victa

%: Makefile
	@$(SPHINXAPIDOC) -f -o "$(SOURCEDIR)"  "$(PROJDIR)"
	@$(SPHINXBUILD) -M html "$(SOURCEDIR)" "$(BUILDDIR)"