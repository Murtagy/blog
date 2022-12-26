# This file is only used if you use `make publish` or
# explicitly specify it as your config file.

import os
import sys
sys.path.append(os.curdir)
from pelicanconf import *

# If your site is available via HTTPS, make sure SITEURL begins with https://
SITEURL = 'https://www.murtagy.me'
RELATIVE_URLS = False

FEED_ALL_ATOM = 'feeds/all.atom.xml'
CATEGORY_FEED_ATOM = 'feeds/{slug}.atom.xml'

DELETE_OUTPUT_DIRECTORY = True

GOOGLE_ANALYTICS = "UA-234232113-1"
DISQUS_SITENAME = 'www-murtagy-me'

# Take advantage of the following defaults
# STATIC_SAVE_AS = '{path}'
# STATIC_URL = '{path}'

# A list of directories (relative to PATH (default to content dir)) in which to look for static files. Such files will be copied to the output directory without modification.
STATIC_PATHS = ['static', 'images']

# Copy static files to the root of the site
EXTRA_PATH_METADATA = {
    'static/robots.txt': {'path': 'robots.txt'},
    'static/favicon.ico': {'path': 'favicon.ico'},
}
