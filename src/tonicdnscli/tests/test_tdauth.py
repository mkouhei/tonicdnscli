#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests of tdauth.py
"""
import unittest
from minimock import mock, Mock, restore
from tonicdnscli.tdauth import authInfo


class authInfoTests(unittest.TestCase):
    def setUp(self):
        import sys
        from StringIO import StringIO
        if sys.version_info > (2, 6) and sys.version_info < (2, 8):
            import urllib2 as urllib
        elif sys.version_info > (3, 0):
            import urllib.request as urllib
        self.authjson = '''{"username": "tonicuser",
"valid_until": 1327146727,
"hash": "efb9fc406a15bf9bdc60f52b36c14bcc6a1fd041",
"token": "efb9fc406a15bf9bdc60f52b36c14bcc6a1fd041"}'''
        self.o = authInfo('tonicuser', 'tonicpw', 'tonic.example.org')
        self.token = 'efb9fc406a15bf9bdc60f52b36c14bcc6a1fd041'

        urllib.build_opener = Mock('build_opener',
            returns=Mock('opener',
                open=Mock('opener.open',
                    returns=Mock('opener.open',
                        read=Mock('opener.open.read',
                            returns=self.authjson)))))

        self.authinfo = {'username': 'tonicuser', 'password': 'tonicpw',
                         'local_user': 'tonicuser'}

    def tearDown(self):
        restore()

    def test__init__(self):
        self.assertEquals('tonicuser', self.o.username)
        self.assertEquals('tonicpw', self.o.password)
        self.assertEquals('', self.o.token)
        self.assertEquals('https://tonic.example.org/authenticate', self.o.uri)

    def test_setInfo(self):
        self.assertDictEqual(self.authinfo, self.o.setInfo())

    def test_getToken(self):
        self.o.getToken()
        self.assertEquals(self.o.token, self.token)

if __name__ == '__main__':
    unittest.main()
