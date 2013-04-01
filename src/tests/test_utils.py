# -*- coding: utf-8 -*-

"""
Tests of utils.py
"""
import unittest
import sys
import os.path
sys.path.append(os.path.abspath('src'))
import test_vars as v
import tonicdnscli.utils as u


class connectTests(unittest.TestCase):
    def setUp(self):

        self.datajson = v.datajson
        self.datadict = v.datadict

    def test_print_inline(self):
        pass

    def test_error(self):
        pass

    def test_get_columns_width(self):
        pass

    def test_generate_row_s(self):
        pass

    def test_get_row_s(self):
        pass

    def test_print_header(self):
        pass

    def test_print_bottom(self):
        pass

    def test_pretty_print(self):
        pass

    def test_pretty_print_zones(self):
        pass

    def test_pretty_print_domain(self):
        pass
