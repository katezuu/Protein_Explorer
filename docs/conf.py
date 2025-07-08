import os
import sys
sys.path.insert(0, os.path.abspath('..'))

project = 'Protein Explorer'
author = 'Katezuu'
release = '0.1'

extensions = [
    'myst_parser',
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
]

# enable more Markdown features
myst_enable_extensions = [
    'colon_fence',
    'deflist',
    'html_admonition',
    'html_image',
    'substitution',
]

source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}

master_doc = 'index'

html_theme = 'furo'
html_static_path = ['_static']
