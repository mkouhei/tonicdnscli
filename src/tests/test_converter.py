# -*- coding: utf-8 -*-

"""
Tests of converter.py
"""
import unittest
import sys
import os.path
sys.path.append(os.path.abspath('src'))
from tonicdnscli.converter import JSONConverter
import test_vars as v


class JSONConvertTests(unittest.TestCase):

    def setUp(self):
        sample0 = os.path.dirname(__file__) + \
            '/../../../examples/example.org.txt'
        sample1 = os.path.dirname(__file__) + '/../../examples/example.org.txt'
        if os.path.isfile(sample0):
            self.sample = sample0
        elif os.path.isfile(sample1):
            self.sample = sample1

    def test__init__(self):
        o = JSONConverter('example.org')
        self.assertEquals('example.org', o.domain)
        self.assertEquals(0, o.split_index)
        self.assertListEqual([], o.records)
        self.assertListEqual([], o.separated_list)
        self.assertFalse(o.delta)

    def test_read_records(self):
        o = JSONConverter('example.org')
        o.read_records(v.str2.splitlines())
        self.assertListEqual(v.dicts1, o.records)

    def test_check_key(self):
        o = JSONConverter('example.org')
        self.assertEquals("test0.example.org", o.check_key(v.line1, 0))
        self.assertEquals("A", o.check_key(v.line1, 1))
        self.assertEquals("10.10.10.10", o.check_key(v.line1, 2))
        self.assertEquals("86400", o.check_key(v.line1, 3))
        self.assertFalse(o.check_key(v.line1, 4))
        self.assertEquals("0", o.check_key(v.line2, 4))
        self.assertFalse(o.check_key(v.line2, 5))
        self.assertEquals("10.10.11.10", o.check_key(v.line3, 2))

    def test_generate_records(self):
        o = JSONConverter('example.org')
        o.generate_records(v.line1)
        self.assertListEqual(v.list3, o.records)
        o2 = JSONConverter('example.org')
        o2.generate_records(v.line2)
        self.assertListEqual(v.list4, o2.records)

    def test_generata_data(self):
        o1 = JSONConverter('example.org')
        o1.generata_data(True)
        self.assertListEqual([{'records': []}], o1.dict_records)
        o2 = JSONConverter('example.org')
        o2.generata_data(False)
        self.assertListEqual([{'records': [], 'name': 'example.org'}],
                             o2.dict_records)

    def test_separate_input_file(self):
        import os.path
        o = JSONConverter('example.org')
        with open(self.sample, 'r') as f:
            o.separate_input_file(f)
        self.maxDiff = None
        self.assertListEqual([v.str1], o.separated_list)
        o2 = JSONConverter('example.org')
        o2.delta = 3
        with open(self.sample, 'r') as f2:
            o2.separate_input_file(f2)
        self.assertListEqual(v.str_l, o2.separated_list)

    def test_get_soa(self):
        o = JSONConverter('exmaple.org')
        self.assertEquals(v.new_soa,
                          o.get_soa(v.older_cur_soa, v.content))
        self.assertNotEquals(v.new_soa,
                             o.get_soa(v.today_cur_soa, v.content))
