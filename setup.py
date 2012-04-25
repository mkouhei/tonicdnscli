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

import os
import sys
from setuptools import setup, find_packages

sys.path.insert(0, 'src')
import tonicdnscli

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
        open(os.path.join("src","README.rst")).read() + \
        open(os.path.join("src","TODO.rst")).read()

requires = ['setuptools']

setup(name='tonicdnscli',
      version=tonicdnscli.__version__,
      description='TonicDNS CLI tool',
      long_description=long_description,
      author='Kouhei Maeda',
      author_email='mkouhei@palmtb.net',
      url='https://github.com/mkouhei/tonicdnscli',
      license=' GNU General Public License version 3',
      classifiers=classifiers,
      packages=find_packages('src'),
      package_dir={'': 'src'},
      data_files = [('share/tonicdnscli/examples', ['examples/example.org.txt'])],
      install_requires=requires,
      extras_require=dict(
        test=[
            'Nose',
            'pep8',
            'unittest',
            ],
        ),
      test_suite='nose.collector',
      tests_require=['Nose','pep8'],
      entry_points="""
        [console_scripts]
        tonicdnscli = tonicdnscli.command:main
""",
)
