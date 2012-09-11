#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests of connect.py
"""
import unittest
from minimock import mock, Mock, restore
import tonicdnscli.connect as conn
import sys
if sys.version_info > (2, 6) and sys.version_info < (2, 8):
    import StringIO as io
elif sys.version_info > (3, 0):
    import io as io

if sys.version_info > (2, 6) and sys.version_info < (2, 8):
    import urllib2 as urllib
elif sys.version_info > (3, 0):
    import urllib.request as urllib


class connectTests(unittest.TestCase):
    def setUp(self):

        self.datajson = '''{"name": "example.org", "type": "MASTER",
"notified_serial": "2012042701",
"records": [{"name": "example.org", "type": "SOA", "content":
"ns.example.org hostmaster.example.org 2012020501 3600 900 86400 3600",
"ttl": "86400", "priority": null, "change_date": "1328449038"},
{"name": "example.org", "type": "NS", "content": "ns.example.org",
"ttl": "86400", "priority": null, "change_date":"1328449038"}]}'''

        self.datadict = {"name": "example.org", "type": "MASTER",
"notified_serial": "2012042701",
"records": [{"name": "example.org", "type": "SOA", "content":
"ns.example.org hostmaster.example.org 2012020501 3600 900 86400 3600",
"ttl": "86400", "priority": False, "change_date": "1328449038"},
{"name": "example.org", "type": "NS", "content": "ns.example.org",
"ttl": "86400", "priority": False, "change_date":"1328449038"}]}

        urllib.build_opener = Mock('build_opener',
            returns=Mock('opener',
                open=Mock('opener.open',
                    returns=Mock('opener.open',
                        read=Mock('opener.open.read',
                            returns=self.datajson)))))

        self.uri = 'https://ns.example.org'
        self.token = 'efb9fc406a15bf9bdc60f52b36c14bcc6a1fd041'
        self.data = ''

    def tearDown(self):
        restore()

    def test_tonicdns_client(self):
        dumpout = io.StringIO()
        ostdout = sys.stdout
        sys.stdout = dumpout
        uri = self.uri + '/zone/example.org'
        conn.tonicdns_client(uri,
                             'GET', self.token, self.data)
        sys.stdout = ostdout
        dumpout.seek(0)
        self.assert_(dumpout.getvalue())

    def test_print_formatted(self):
        dumpout = io.StringIO()
        ostdout = sys.stdout
        sys.stdout = dumpout
        conn.print_formatted(self.datadict)
        sys.stdout = ostdout
        dumpout.seek(0)
        self.assert_(dumpout.getvalue())

if __name__ == '__main__':
    unittest.main()
