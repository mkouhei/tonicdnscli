#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests of tdauth.py
"""
import unittest
from tonicdnscli.tdauth import Auth
from mock import Mock


class AuthTests(unittest.TestCase):
    def setUp(self):
        self.username = 'tonicuser'
        self.password = 'tonicpw'
        self.server = 'tonic.example.org'
        self.token0 = 'efb9fc406a15bf9bdc60f52b36c14bcc6a1fd041'
        self.token1 = 'efb9fc406a15bf9bdc60f52b36c14bcc6a1fd042'
        self.a = Auth(self.username, self.password, self.server)
        self.authinfo = {"username": self.username,
                         "password": self.password,
                         "local_user": self.username}

    def test__init__(self):
        self.assertEquals(self.username, self.a.username)
        self.assertEquals(self.password, self.a.password)
        self.assertEquals('', self.a.token)
        self.assertEquals('https://tonic.example.org/authenticate',
                          self.a.uri)

    def test_setInfo(self):
        self.assertDictEqual(self.authinfo, self.a.setInfo())

    def test_getToken(self):
        a_mock = Auth(self.username, self.password, self.server)
        a_mock.tonicDNSClient = Mock(return_value=self.token0)
        token = a_mock.tonicDNSClient()
        self.assertEquals(self.token0, token)
        self.assertNotEquals(self.token1, token)

if __name__ == '__main__':
    unittest.main()
