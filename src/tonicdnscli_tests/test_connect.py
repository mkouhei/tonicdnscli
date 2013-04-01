# -*- coding: utf-8 -*-

"""
Tests of connect.py
"""
import unittest
from minimock import mock, Mock, restore
import sys
if sys.version_info > (2, 6) and sys.version_info < (2, 8):
    import StringIO as io
elif sys.version_info > (3, 0):
    import io as io
if sys.version_info > (2, 6) and sys.version_info < (2, 8):
    import urllib2 as urllib
elif sys.version_info > (3, 0):
    import urllib.request as urllib
import os.path
sys.path.append(os.path.abspath('src'))
import tonicdnscli.connect as conn
import test_vars as v


class connectTests(unittest.TestCase):
    def setUp(self):
        self.datajson = v.datajson

        self.datadict = v.datadict

        urllib.build_opener = Mock(
            'build_opener',
            returns=Mock(
                'opener',
                open=Mock(
                    'opener.open',
                    returns=Mock(
                        'opener.open',
                        read=Mock(
                            'opener.open.read',
                            returns=self.datajson)))))

        self.uri = v.uri
        self.token = v.token
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
