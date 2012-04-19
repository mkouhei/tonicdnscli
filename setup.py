#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Copyright (C) 2012 Kouhei Maeda <mkouhei@palmtb.net>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import os, sys
from setuptools import setup, find_packages

sys.path.insert(0, 'src')
import tonicdns_cli

classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: System Administrators",
    "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
    "Programming Language :: Python",
    "Topic :: Internet",
    "Topic :: Internet :: Name Service (DNS)",
    "Topic :: System :: Systems Administration",
]

long_description = \
        open(os.path.join("src","README.md")).read() + \
        open(os.path.join("src","TODO.md")).read()

requires = ['setuptools']

setup(name='tonicdns_cli',
      version=tonicdns_cli.__version__,
      description='TonicDNS CLI tool',
      long_description=long_description,
      author='Kouhei Maeda',
      author_email='mkouhei@palmtb.net',
      url='https://github.com/mkouhei/tonicdns_cli',
      license=' GNU General Public License version 3',
      classifiers=classifiers,
      packages=find_packages('src'),
      package_dir={'': 'src'},
      package_data = {'sample': ['sample/*']},
      include_package_data=True,
      install_requires=requires,
      entry_points="""
        [console_scripts]
        tonicdns_cli = tonicdns_cli.command:main
""",
)
