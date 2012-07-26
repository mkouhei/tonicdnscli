#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests of command.py
"""
import unittest
import tonicdnscli.command as c


class commandTests(unittest.TestCase):
    def setUp(self):
        import os.path
        self.maxDiff = None
        self.sample = os.path.dirname(__file__) + \
            '/../../../examples/example.org.txt'
        self.domain = 'example.org'
        self.cu_records = [{'records':
                         [{'content': '10.10.10.10',
                           'type': 'A',
                           'name': 'test0.example.org',
                           'ttl': 86400},
                          {'content': '10.10.10.11',
                           'type': 'A',
                           'name': 'test1.example.org',
                           'ttl': 86400},
                          {'content': '10.10.10.12',
                           'type': 'A',
                           'name': 'test2.example.org',
                           'ttl': 86400},
                          {'content': 'mx.example.org',
                           'priority': 0,
                           'type': 'MX',
                           'name': 'example.org',
                           'ttl': 86400},
                          {'content': 'mx2.example.org',
                           'priority': 10,
                           'type': 'MX',
                           'name': 'example.org',
                           'ttl': 86400},
                          {'content': '10.10.11.10',
                           'type': 'A',
                           'name': 'mx.example.org',
                           'ttl': 3600},
                          {'content': '10.10.11.10',
                           'type': 'A',
                           'name': 'mx2.example.org',
                           'ttl': 3600}]
                         }]
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

    def test_check_infile(self):
        self.assertEquals(self.domain, c.check_infile(
                self.sample))

    def test_set_json(self):
        self.assertEquals(self.cu_records,
                     c.set_json(self.domain, True, filename=self.sample))
        self.assertEquals(self.r_records,
                     c.set_json(self.domain, False, filename=self.sample))
        self.assertEquals(self.d_cu_record,
                     c.set_json(self.domain, True, record=self.record))
        self.assertEquals(self.d_r_record,
                     c.set_json(self.domain, False, record=self.record))

if __name__ == '__main__':
    unittest.main()
