#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests of converter.py
"""
import unittest
from tonicdnscli.converter import JSONConvert


class JSONConvertTests(unittest.TestCase):

    l = """# name type content ttl priority
test0.example.org A 10.10.10.10 86400
test1.example.org A 10.10.10.11 86400
test2.example.org A 10.10.10.12 86400
example.org MX mx.example.org 86400 0
example.org MX mx2.example.org 86400 10
mx.example.org A 10.10.11.10 3600
mx2.example.org A\t\t10.10.11.10 3600"""

    lists = ["""test0.example.org A 10.10.10.10 86400
test1.example.org A 10.10.10.11 86400
test2.example.org A 10.10.10.12 86400
example.org MX mx.example.org 86400 0
example.org MX mx2.example.org 86400 10
mx.example.org A 10.10.11.10 3600
mx2.example.org A\t\t10.10.11.10 3600
"""]

    lists2 = ["""test0.example.org A 10.10.10.10 86400
test1.example.org A 10.10.10.11 86400
test2.example.org A 10.10.10.12 86400\n""",
"""example.org MX mx.example.org 86400 0
example.org MX mx2.example.org 86400 10
mx.example.org A 10.10.11.10 3600\n""",
'mx2.example.org A\t\t10.10.11.10 3600\n']

    d = [{'content': '10.10.10.10', 'name': 'test0.example.org',
          'ttl': '86400', 'type': 'A'},
         {'content': '10.10.10.11', 'name': 'test1.example.org',
          'ttl': '86400', 'type': 'A'},
         {'content': '10.10.10.12', 'name': 'test2.example.org',
          'ttl': '86400', 'type': 'A'},
         {'content': 'mx.example.org', 'name': 'example.org',
          'priority': '0', 'ttl': '86400', 'type': 'MX'},
         {'content': 'mx2.example.org', 'name': 'example.org',
          'priority': '10', 'ttl': '86400', 'type': 'MX'},
         {'content': '10.10.11.10', 'name': 'mx.example.org',
          'ttl': '3600', 'type': 'A'},
         {'content': '10.10.11.10', 'name': 'mx2.example.org',
          'ttl': '3600', 'type': 'A'}]
    l1 = "test0.example.org A 10.10.10.10 86400"
    l2 = "example.org MX mx.example.org 86400 0"
    l3 = "mx2.example.org A\t\t10.10.11.10 3600"

    def test__init__(self):
        o = JSONConvert('example.org')
        self.assertEquals('example.org', o.domain)
        self.assertEquals(0, o.split_index)
        self.assertListEqual([], o.records)
        self.assertListEqual([], o.separated_list)
        self.assertFalse(o.delta)

    def test_readRecords(self):
        o = JSONConvert('example.org')
        o.readRecords(self.l.splitlines())
        self.assertListEqual(self.d, o.records)

    def test_checkkey(self):
        o = JSONConvert('example.org')
        self.assertEquals("test0.example.org", o.checkkey(self.l1, 0))
        self.assertEquals("A", o.checkkey(self.l1, 1))
        self.assertEquals("10.10.10.10", o.checkkey(self.l1, 2))
        self.assertEquals("86400", o.checkkey(self.l1, 3))
        self.assertFalse(o.checkkey(self.l1, 4))
        self.assertEquals("0", o.checkkey(self.l2, 4))
        self.assertFalse(o.checkkey(self.l2, 5))
        self.assertEquals("10.10.11.10", o.checkkey(self.l3, 2))

    def test_generateDict(self):
        o = JSONConvert('example.org')
        o.generateDict(self.l1)
        self.assertListEqual([{'name': 'test0.example.org', 'type': 'A',
                            'content': '10.10.10.10', 'ttl': '86400'}],
                          o.records)
        o2 = JSONConvert('example.org')
        o2.generateDict(self.l2)
        self.assertListEqual([{'name': 'example.org', 'type': 'MX',
                            'content': 'mx.example.org', 'ttl': '86400',
                            'priority': '0'}], o2.records)

    def test_genData(self):
        o = JSONConvert('example.org')
        o.genData(True)
        self.assertDictEqual({'records': []}, o.dict_records)
        o.genData(False)
        self.assertDictEqual({'records': [], 'name': 'example.org'},
                          o.dict_records)

    def test_separateInputFile(self):
        import os.path
        sample = os.path.dirname(__file__) + \
            '/../../../examples/example.org.txt'
        o = JSONConvert('example.org')
        with open(sample, 'r') as f:
            o.separateInputFile(f)
        self.maxDiff = None
        self.assertListEqual(self.lists, o.separated_list)
        o2 = JSONConvert('example.org')
        o2.delta = 3
        with open(sample, 'r') as f2:
            o2.separateInputFile(f2)
        self.assertListEqual(self.lists2, o2.separated_list)

if __name__ == '__main__':
    unittest.main()
