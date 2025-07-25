# -- Path setup --------------------------------------------------------------

import os
import sys

sys.path.insert(0, os.path.abspath('..'))

# -- Project information -----------------------------------------------------

project = 'Protein Structure Explorer'
author = 'Ekaterina Paramonova'
release = '0.1.0'

# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
]

templates_path = ['_templates']

# -- Options for HTML output -------------------------------------------------

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
exclude_patterns: list[str] = ['_build', 'Thumbs.db', '.DS_Store']
html_logo = '_static/logo.png'
html_favicon = '_static/favicon.ico'
