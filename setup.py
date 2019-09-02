#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'readme.md'), encoding='utf-8') as f:
    long_description = f.read()

VERSION = "0.1.0"
DOWNLOAD_URL = \
    'https://github.com/rubenbe/comfospottwin40/archive/{}.zip'.format(VERSION)

EXTRAS_REQUIRE = {
    'async': ['pyserial == 3.4']
}

PACKAGES = find_packages(exclude=['tests', 'tests.*'])

setup(
  name='pycomfospottwin40',
  packages=PACKAGES,
  python_requires='>=3.4',
  version=VERSION,
  description='IKEA Trådfri/Tradfri API. Control and observe your '
              'lights from Python.',
  long_description=long_description,
  author='rubenbe',
  author_email='no@email.com',
  long_description_content_type="text/markdown",
  url='https://github.com/rubenbe/comfospottwin40',
  license='MIT',
  keywords='zehnder iot homeautomation',
  download_url=DOWNLOAD_URL,
  extras_require=EXTRAS_REQUIRE,
)
