#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests of converter.py
"""
import unittest
from tonicdnscli.converter import JSONConvert
from datetime import date


class JSONConvertTests(unittest.TestCase):
    def setUp(self):
        self.str1 = """# name type content ttl priority
test0.example.org A 10.10.10.10 86400
test1.example.org A 10.10.10.11 86400
test2.example.org A 10.10.10.12 86400
example.org MX mx.example.org 86400 0
example.org MX mx2.example.org 86400 10
mx.example.org A 10.10.11.10 3600
mx2.example.org A\t\t10.10.11.10 3600"""
        self.list1 = ["""test0.example.org A 10.10.10.10 86400
test1.example.org A 10.10.10.11 86400
test2.example.org A 10.10.10.12 86400
example.org MX mx.example.org 86400 0
example.org MX mx2.example.org 86400 10
mx.example.org A 10.10.11.10 3600
mx2.example.org A\t\t10.10.11.10 3600
"""]
        self.list2 = ["""test0.example.org A 10.10.10.10 86400
test1.example.org A 10.10.10.11 86400
test2.example.org A 10.10.10.12 86400\n""",
"""example.org MX mx.example.org 86400 0
example.org MX mx2.example.org 86400 10
mx.example.org A 10.10.11.10 3600\n""",
'mx2.example.org A\t\t10.10.11.10 3600\n']

        self.list3 = [{'name': 'test0.example.org', 'type': 'A',
                       'content': '10.10.10.10', 'ttl': 86400}]
        self.list4 = [{'name': 'example.org', 'type': 'MX',
                       'content': 'mx.example.org',
                       'ttl': 86400, 'priority': 0}]

        self.dicts1 = [{'content': '10.10.10.10', 'name': 'test0.example.org',
                        'ttl': 86400, 'type': 'A'},
                       {'content': '10.10.10.11', 'name': 'test1.example.org',
                        'ttl': 86400, 'type': 'A'},
                       {'content': '10.10.10.12', 'name': 'test2.example.org',
                        'ttl': 86400, 'type': 'A'},
                       {'content': 'mx.example.org', 'name': 'example.org',
                        'priority': 0, 'ttl': 86400, 'type': 'MX'},
                       {'content': 'mx2.example.org', 'name': 'example.org',
                        'priority': 10, 'ttl': 86400, 'type': 'MX'},
                       {'content': '10.10.11.10', 'name': 'mx.example.org',
                        'ttl': 3600, 'type': 'A'},
                       {'content': '10.10.11.10', 'name': 'mx2.example.org',
                        'ttl': 3600, 'type': 'A'}]
        self.line1 = "test0.example.org A 10.10.10.10 86400"
        self.line2 = "example.org MX mx.example.org 86400 0"
        self.line3 = "mx2.example.org A\t\t10.10.11.10 3600"

        self.older_cur_soa = {
            'name': 'example.org',
            'type': 'SOA',
            'content': 'ns.example.org postmaster.example.org 2012040501',
            'ttl': 86400,
            'priority': None
            }
        today = date.strftime(date.today(), '%Y%m%d')
        self.today_cur_soa = {
            'name': 'example.org',
            'type': 'SOA',
            'content': 'ns.example.org postmaster.example.org ' + \
                today + '01',
            'ttl': 86400,
            'priority': None
            }
        self.new_soa = {
            'name': 'example.org',
            'type': 'SOA',
            'content': 'ns.example.org postmaster.example.org ' + \
                today + '01 3600 900 86400 3600',
            'ttl': 86400,
            'priority': None
            }

    def test__init__(self):
        o = JSONConvert('example.org')
        self.assertEquals('example.org', o.domain)
        self.assertEquals(0, o.split_index)
        self.assertListEqual([], o.records)
        self.assertListEqual([], o.separated_list)
        self.assertFalse(o.delta)

    def test_readRecords(self):
        o = JSONConvert('example.org')
        o.readRecords(self.str1.splitlines())
        self.assertListEqual(self.dicts1, o.records)

    def test_checkkey(self):
        o = JSONConvert('example.org')
        self.assertEquals("test0.example.org", o.checkkey(self.line1, 0))
        self.assertEquals("A", o.checkkey(self.line1, 1))
        self.assertEquals("10.10.10.10", o.checkkey(self.line1, 2))
        self.assertEquals("86400", o.checkkey(self.line1, 3))
        self.assertFalse(o.checkkey(self.line1, 4))
        self.assertEquals("0", o.checkkey(self.line2, 4))
        self.assertFalse(o.checkkey(self.line2, 5))
        self.assertEquals("10.10.11.10", o.checkkey(self.line3, 2))

    def test_generateDict(self):
        o = JSONConvert('example.org')
        o.generateDict(self.line1)
        self.assertListEqual(self.list3, o.records)
        o2 = JSONConvert('example.org')
        o2.generateDict(self.line2)
        self.assertListEqual(self.list4, o2.records)

    def test_genData(self):
        o1 = JSONConvert('example.org')
        o1.genData(True)
        self.assertListEqual([{'records': []}], o1.dict_records)
        o2 = JSONConvert('example.org')
        o2.genData(False)
        self.assertListEqual([{'records': [], 'name': 'example.org'}],
                          o2.dict_records)

    def test_separateInputFile(self):
        import os.path
        sample = os.path.dirname(__file__) + \
            '/../../../examples/example.org.txt'
        o = JSONConvert('example.org')
        with open(sample, 'r') as f:
            o.separateInputFile(f)
        self.maxDiff = None
        self.assertListEqual(self.list1, o.separated_list)
        o2 = JSONConvert('example.org')
        o2.delta = 3
        with open(sample, 'r') as f2:
            o2.separateInputFile(f2)
        self.assertListEqual(self.list2, o2.separated_list)

    def test_getSOA(self):
        o = JSONConvert('exmaple.org')
        self.assertEquals(self.new_soa, o.getSOA(self.older_cur_soa))
        self.assertNotEquals(self.new_soa, o.getSOA(self.today_cur_soa))

if __name__ == '__main__':
    unittest.main()
