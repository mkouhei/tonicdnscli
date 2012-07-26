#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests of processing.py
"""
import unittest
import sys
if sys.version_info > (2, 6) and sys.version_info < (2, 8):
    import StringIO as io
elif sys.version_info > (3, 0):
    import io as io
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
        self.dict2 = {'identifier': self.identifier,
                      'description': 'example',
                      'entries': [
                {'name': self.domain,
                 'type': 'SOA',
                 'content': 'ns.example.org hostmaster.example.org \
2012020501 3600 900 86400 3600',
                 'ttl': 86400},
                {'name': self.domain,
                 'type': 'NS',
                 'content': 'ns' + self.domain,
                 'ttl': 86400},
                {'name': self.domain,
                 'type': 'A',
                 'content': '10.0.0.100',
                 'ttl': 86400},
                {'name': self.domain,
                 'type': 'MX',
                 'content': 'mx.' + self.domain,
                 'ttl': 86400,
                 'priority': 10},
                ]}

    def test_create_records(self):
        conn.tonicdns_client = Mock(return_value='true')
        dumpout = io.StringIO()
        ostdout = sys.stdout
        sys.stdout = dumpout
        print(conn.tonicdns_client())
        p.create_records(self.server, self.token, self.domain, self.dict0)
        sys.stdout = ostdout
        dumpout.seek(0)
        dumpout.getvalue()
        self.assertEquals('true\n', dumpout.getvalue())

    def test_delete_records(self):
        conn.tonicdns_client = Mock(return_value='true')
        dumpout = io.StringIO()
        ostdout = sys.stdout
        sys.stdout = dumpout
        print(conn.tonicdns_client())
        p.delete_records(self.server, self.token, self.dict1)
        sys.stdout = ostdout
        dumpout.seek(0)
        dumpout.getvalue()
        self.assertEquals('true\n', dumpout.getvalue())

    def test_create_template(self):
        conn.tonicdns_client = Mock(return_value='true')
        dumpout = io.StringIO()
        ostdout = sys.stdout
        sys.stdout = dumpout
        print(conn.tonicdns_client())
        p.create_template(self.server, self.token,
                         self.identifier, self.dict2)
        sys.stdout = ostdout
        dumpout.seek(0)
        dumpout.getvalue()
        self.assertEquals('true\n', dumpout.getvalue())

    def test_delete_template(self):
        conn.tonicdns_client = Mock(return_value='true')
        dumpout = io.StringIO()
        ostdout = sys.stdout
        sys.stdout = dumpout
        print(conn.tonicdns_client())
        p.delete_template(self.server, self.token,
                         self.identifier)
        sys.stdout = ostdout
        dumpout.seek(0)
        dumpout.getvalue()
        self.assertEquals('true\n', dumpout.getvalue())

if __name__ == '__main__':
    unittest.main()
