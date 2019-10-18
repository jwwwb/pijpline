#! /usr/bin/env python3
"""Setup script for the pijpline tool."""

import sys
from setuptools import setup

if sys.version_info[:2] < (3, 5):
    raise ValueError('Please use python3.5 and above.')

setup(name="pijpline",
      version="0.3a1",
      scripts=['bin/pijp'],
      install_requires=['pyyaml'],
      packages=['pijpline'])
