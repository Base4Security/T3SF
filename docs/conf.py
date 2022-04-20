import sys
import os
import re
from sphinx_rtd_theme import __version__ as theme_version
from sphinx_rtd_theme import __version_full__ as theme_version_full
import sphinx_rtd_theme
from sphinx.locale import _


project = u'T3SF'
slug = re.sub(r'\W+', '-', project.lower())
version = theme_version
release = theme_version_full
author = u'Base4 Security (I+D+I Department) '
copyright = author
language = 'en'

extensions = ['sphinx_rtd_theme', 'sphinx_toolbox.confval',]

html_theme = "sphinx_rtd_theme"
html_theme_options = {
    'logo_only': True,
    'navigation_depth': 5,
    'style_nav_header_background': 'white',
}

html_logo = "logo.png"
html_show_sourcelink = True
