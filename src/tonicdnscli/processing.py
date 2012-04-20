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


def unprovide():
    print "ERROR: This feature does not provide"
    exit(10)


def tonicDNSClient(uri, method, token, data):
    import json
    import urllib2

    encoded = json.JSONEncoder().encode(data)

    o = urllib2.build_opener(urllib2.HTTPHandler)
    r = urllib2.Request(uri, data=encoded)

    r.add_header('x-authentication-token', token)

    # When encoded(=data) is False, retrieve data as GET method.
    if encoded:
        r.add_header('Content-Type', 'application/json')

    r.get_method = lambda: method
    url = o.open(r)

    # response body
    if method == 'GET':
        datas = json.loads(url.read())
        print json.dumps(datas, sort_keys=True, indent=2)

    else:
        data = url.read()
        print data


def createZoneRecords():
    # ContentType: application/json
    # x-authentication-token: token
    # method: PUT
    # uri: /zone
    unprovide()


def createRecords(server, token, domain, data):
    # ContentType: application/json
    # x-authentication-token: token
    method = 'PUT'
    uri = 'https://' + server + '/zone/' + domain
    tonicDNSClient(uri, method, token, data)


def deleteRecords(server, token, data):
    # ContentType: application/json
    # x-authentication-token: token
    method = 'DELETE'
    uri = 'https://' + server + '/zone'
    tonicDNSClient(uri, method, token, data)


def getZone(server, token, domain):
    # x-authentication-token: token
    method = 'GET'
    uri = 'https://' + server + '/zone/' + domain
    tonicDNSClient(uri, method, token, data=False)


def getAllZone(server, token):
    # x-authentication-token: token
    method = 'GET'
    uri = 'https://' + server + '/zone'
    tonicDNSClient(uri, method, token, data=False)


def deleteDomain():
    # x-authentication-token: token
    # method: DELETE
    # uri: /zone/:domain
    unprovide()


def createTemplate():
    # ContentType: application/json
    # x-authentication-token: token
    # method: PUT
    # uri: /template/:template
    unprovide()


def updateTemplate():
    # ContentType: application/json
    # x-authentication-token: token
    # method: POST
    # uri: /template
    unprovide()


def deleteTemplate():
    # x-authentication-token: token
    # method: DELETE
    # uri: /template/:template
    unprovide()


def getTemplate():
    # x-authentication-token: token
    # method: GET
    # uri: /template/:template
    unprovide()


def getAllTemplates():
    # x-authentication-token: token
    # method: GET
    # uri: /template
    unprovide()
