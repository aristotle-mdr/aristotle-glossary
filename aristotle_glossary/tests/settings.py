import os, sys
from aristotle_mdr.tests.settings.settings import *
from aristotle_mdr.required_settings import INSTALLED_APPS

INSTALLED_APPS = (
    # The good stuff
    'aristotle_glossary',
) + INSTALLED_APPS

ARISTOTLE_SETTINGS['SEPARATORS']['DataElementConcept'] = '--'
ARISTOTLE_SETTINGS['CONTENT_EXTENSIONS'] = ARISTOTLE_SETTINGS['CONTENT_EXTENSIONS'] +['aristotle_glossary']

ROOT_URLCONF = 'aristotle_glossary.tests.urls'
