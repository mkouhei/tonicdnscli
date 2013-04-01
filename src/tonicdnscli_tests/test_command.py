# -*- coding: utf-8 -*-

"""
Tests of command.py
"""
import unittest
import sys
import os.path
sys.path.append(os.path.abspath('src'))
import tonicdnscli.command as c
import test_vars as v


class commandTests(unittest.TestCase):
    def setUp(self):
        import os.path
        self.maxDiff = None
        self.domain = 'example.org'
        self.cu_records = [{'records': v.dicts1}]
        self.r_records = [{'name': 'example.org',
                           'records': self.cu_records[0].get('records')}]
        self.record = ['test3.example.org A 10.10.20.10 3600']
        self.d_cu_record = [{'records': [{'name': 'test3.example.org',
                                          'type': 'A',
                                          'content': '10.10.20.10',
                                          'ttl': 3600}]}]
        self.d_r_record = [{'name': self.domain,
                            'records': [{'name': 'test3.example.org',
                                         'type': 'A',
                                         'content': '10.10.20.10',
                                         'ttl': 3600}]}]
        sample0 = os.path.dirname(__file__) + \
            '/../../../examples/example.org.txt'
        sample1 = os.path.dirname(__file__) + '/../../examples/example.org.txt'
        if os.path.isfile(sample0):
            self.sample = sample0
        elif os.path.isfile(sample1):
            self.sample = sample1

    def test_check_infile(self):
        self.assertEquals(self.domain, c.check_infile(self.sample))

    def test_set_json(self):
        self.assertEquals(self.cu_records,
                          c.set_json(self.domain, True, filename=self.sample))
        self.assertEquals(self.r_records,
                          c.set_json(self.domain, False, filename=self.sample))
        self.assertEquals(self.d_cu_record,
                          c.set_json(self.domain, True, record=self.record))
        self.assertEquals(self.d_r_record,
                          c.set_json(self.domain, False, record=self.record))
