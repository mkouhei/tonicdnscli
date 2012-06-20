#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests of processing.py
"""
import unittest
import sys
import StringIO
from mock import Mock
import tonicdnscli.connect as conn
import tonicdnscli.processing as p


class processingTests(unittest.TestCase):
    def setUp(self):
        self.server = 'tonic.example.org'
        self.domain = 'example.org'
        self.identifier = 'example_org'
        self.token = 'efb9fc406a15bf9bdc60f52b36c14bcc6a1fd041'
        self.list0 = [{'content': '10.10.10.10', 'name': 'test0.example.org',
                        'ttl': 86400, 'type': 'A'},
                       {'content': '10.10.10.11', 'name': 'test1.example.org',
                        'ttl': 86400, 'type': 'A'},
                       {'content': '10.10.10.12', 'name': 'test2.example.org',
                        'ttl': 86400, 'type': 'A'},
                       {'content': 'mx2.example.org', 'name': 'example.org',
                        'priority': 10, 'ttl': 86400, 'type': 'MX'},
                       {'content': '10.10.11.10', 'name': 'mx.example.org',
                        'ttl': 3600, 'type': 'A'},
                       {'content': '10.10.11.10', 'name': 'mx2.example.org',
                        'ttl': 3600, 'type': 'A'}]
        self.dict0 = {'records': self.list0}
        self.dict1 = {'name': self.domain,
                      'records': self.list0}

    def test_createRecords(self):
        conn.tonicDNSClient = Mock(return_value='true')
        dumpout = StringIO.StringIO()
        ostdout = sys.stdout
        sys.stdout = dumpout
        print(conn.tonicDNSClient())
        p.createRecords(self.server, self.token, self.domain, self.dict0)
        sys.stdout = ostdout
        dumpout.seek(0)
        dumpout.getvalue()
        self.assertEquals('true\n', dumpout.getvalue())

    def test_deleteRecords(self):
        conn.tonicDNSClient = Mock(return_value='true')
        dumpout = StringIO.StringIO()
        ostdout = sys.stdout
        sys.stdout = dumpout
        print(conn.tonicDNSClient())
        p.deleteRecords(self.server, self.token, self.dict1)
        sys.stdout = ostdout
        dumpout.seek(0)
        dumpout.getvalue()
        self.assertEquals('true\n', dumpout.getvalue())

if __name__ == '__main__':
    unittest.main()
