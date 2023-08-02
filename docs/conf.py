import sys
import os
import re
import sphinx_rtd_theme
from sphinx.locale import _


project = u'T3SF'
slug = re.sub(r'\W+', '-', project.lower())
version = "2.5"
release = "2.5"
language = 'en'

extensions = ['sphinx_rtd_theme', 'sphinx_toolbox.confval',]

html_theme = "sphinx_rtd_theme"
html_theme_options = {
    'logo_only': True,
    'navigation_depth': 5,
    'style_nav_header_background': 'white',
}

html_logo = "images/logo.png"
html_show_sourcelink = True
html_show_copyright = False