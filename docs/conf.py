# Configuration file for the Sphinx documentation builder.

project = 'Protein Explorer'
author = 'Ekaterina Paramonova'
copyright = '2025, ' + author
release = '0.1.0'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

html_theme = 'furo'
html_static_path = ["_static"]
