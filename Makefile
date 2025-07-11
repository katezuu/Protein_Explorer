SPHINXBUILD = sphinx-build
SOURCEDIR   = docs
BUILDDIR    = docs/_build

.PHONY: html
html:
$(SPHINXBUILD) -M html $(SOURCEDIR) $(BUILDDIR)