#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Copyright (C) 2012 Kouhei Maeda <mkouhei@palmtb.net>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""


class authInfo():

    def __init__(self, username, password, server):
        self.username = username
        self.password = password
        self.token = ''
        self.uri = 'https://' + server + '/authenticate'

    def setInfo(self):
        authinfo = {
                "username": self.username,
                "password": self.password,
                "local_user": self.username
                }
        return authinfo

    def getToken(self):
        import json
        import sys
        if sys.version_info > (2, 6) and sys.version_info < (2, 8):
            import urllib2 as urllib
        elif sys.version_info > (3, 0):
            import urllib.request as urllib
        authjson = json.JSONEncoder().encode(self.setInfo())
        o = urllib.build_opener(urllib.HTTPHandler)
        r = urllib.Request(self.uri, data=authjson.encode('utf-8'))
        r.add_header('Content-Type', 'application/json')
        r.get_method = lambda: 'PUT'
        try:
            self.token = json.loads(o.open(r).read().decode('utf-8'))["hash"]
        except urllib.HTTPError as e:
            sys.stderr.write("ERROR: %s\n" % e)
        except urllib.URLError as e:
            sys.stderr.write("ERROR: %s\n" % e)
            exit(1)
