import os
import sys
sys.path.insert(0, os.path.abspath('..'))

project = 'Protein Explorer'
author = 'Ekaterina Paramonova'
release = '0.1.0'
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx_autodoc_typehints',
    'sphinxcontrib.httpdomain',
    'myst_nb',
]
autosummary_generate = True
templates_path = ['_templates']
exclude_patterns = ['_build','Thumbs.db','.DS_Store']
html_theme = 'furo'
html_static_path = ['_static']
html_logo = '_static/logo.png'
html_favicon = '_static/logo.png'
html_css_files = ['custom.css']
nb_execution_mode = 'off'