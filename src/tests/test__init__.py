# -*- coding: utf-8 -*-

"""
Tests of __init__.py
"""
import unittest
import sys
import os.path
sys.path.append(os.path.abspath('src'))
import tonicdnscli


class InitTests(unittest.TestCase):
    def test_version_defined(self):
        actual_version = tonicdnscli.__version__
        self.assertTrue(actual_version)
