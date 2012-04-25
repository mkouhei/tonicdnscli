#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests of tdauth.py
"""
import unittest
from tonicdnscli.tdauth import authInfo


class authInfoTests(unittest.TestCase):
    def test__init__(self):
        o = authInfo('tonicuser', 'tonicpw', 'tonic.example.org')
        self.assertEquals('tonicuser', o.username)
        self.assertEquals('tonicpw', o.password)
        self.assertEquals('', o.token)
        self.assertEquals('https://tonic.example.org/authenticate', o.uri)

    def test_setInfo(self):
        o = authInfo('tonicuser', 'tonicpw', 'tonic.example.org')
        authinfo = {'username': 'tonicuser', 'password': 'tonicpw',
                    'local_user': 'tonicuser'}
        self.assertDictEqual(authinfo, o.setInfo())

    '''
    def test_getToken(self):
    '''

if __name__ == '__main__':
    unittest.main()
