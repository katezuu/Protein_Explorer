# Makefile for Sphinx documentation

SPHINXBUILD   = sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build

.PHONY: help clean html

help:
	@echo "Usage:"
	@echo "  make html   Build HTML documentation"
	@echo "  make clean  Remove build files"

html:
	$(SPHINXBUILD) -b html $(SOURCEDIR) $(BUILDDIR)/html

clean:
	@rm -rf $(BUILDDIR)/*