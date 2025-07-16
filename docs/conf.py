import os
import sys

sys.path.insert(0, os.path.abspath('..'))

project = 'Protein Structure Explorer'
author = 'Ekaterina Paramonova'
release = '0.1.0'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',  # для Google/NumPy docstrings
    'myst_parser',  # если вы хотите Markdown
]

templates_path = ['_templates']
exclude_patterns: list[str] = []

# HTML output
html_theme = 'furo'
html_static_path = ['_static']
