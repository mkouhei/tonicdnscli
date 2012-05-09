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
        self.sample = os.path.dirname(__file__) + \
            '/../../../examples/example.org.txt'
        self.domain = 'example.org'
        self.cu_records = [{'records':
                         [{'content': '10.10.10.10',
                           'type': 'A',
                           'name': 'test0.example.org',
                           'ttl': '86400'},
                          {'content': '10.10.10.11',
                           'type': 'A',
                           'name': 'test1.example.org',
                           'ttl': '86400'},
                          {'content': '10.10.10.12',
                           'type': 'A',
                           'name': 'test2.example.org',
                           'ttl': '86400'},
                          {'content': 'mx.example.org',
                           'priority': '0',
                           'type': 'MX',
                           'name': 'example.org',
                           'ttl': '86400'},
                          {'content': 'mx2.example.org',
                           'priority': '10',
                           'type': 'MX',
                           'name': 'example.org',
                           'ttl': '86400'},
                          {'content': '10.10.11.10',
                           'type': 'A',
                           'name': 'mx.example.org',
                           'ttl': '3600'},
                          {'content': '10.10.11.10',
                           'type': 'A',
                           'name': 'mx2.example.org',
                           'ttl': '3600'}]
                         }]
        self.r_records = [{'name': 'example.org',
                           'records': self.cu_records[0].get('records')}]

    def test_checkInfile(self):
        self.assertEquals(self.domain, c.checkInfile(
                self.sample))

    def test_getJSON(self):
        self.assertEquals(self.cu_records,
                     c.getJSON(self.domain, self.sample, True))
        self.assertEquals(self.r_records,
                     c.getJSON(self.domain, self.sample, False))

if __name__ == '__main__':
    unittest.main()
