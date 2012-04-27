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
    print("ERROR: This feature does not provide")
    exit(10)


def tonicDNSClient(uri, method, token, data):
    import sys
    import json
    if sys.version_info > (2, 6) and sys.version_info < (2, 8):
        import urllib2 as urllib
    elif sys.version_info > (3, 0):
        import urllib.request as urllib

    encoded = json.JSONEncoder().encode(data)

    o = urllib.build_opener(urllib.HTTPHandler)
    r = urllib.Request(uri, data=encoded.encode('utf-8'))

    r.add_header('x-authentication-token', token)

    # When encoded(=data) is False, retrieve data as GET method.
    if encoded:
        r.add_header('Content-Type', 'application/json')

    r.get_method = lambda: method
    try:
        url = o.open(r)
    except urllib.HTTPError as e:
        sys.stderr.write("ERROR: %s\n" % e)
        exit(1)

    # response body
    if method == 'GET':
        datas = json.loads(url.read().decode('utf-8'))
        formattedPrint(datas)
    else:
        data = url.read()
        print(data)


def formattedPrint(datas):
    print("domain: %(name)s" % datas)
    print("serial: %(notified_serial)s" % datas)
    print("DNS   : %(type)s" % datas)
    hr()
    print('%-25s %-4s %-50s %-5s %-3s'
          % ('name', 'type', 'content', 'ttl', 'prio'))
    hr()
    for record in datas['records']:
        print("%(name)-25s" % record),
        print("%(type)-4s" % record),
        print("%(content)-50s" % record),
        print("%(ttl)-5s" % record),
        if record['priority']:
            print("%(priority)2s" % record)
        else:
            print
    hr()


def hr():
    print('=' * 93)


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
    for i in data:
        tonicDNSClient(uri, method, token, i)


def deleteRecords(server, token, data):
    # ContentType: application/json
    # x-authentication-token: token
    method = 'DELETE'
    uri = 'https://' + server + '/zone'
    for i in data:
        tonicDNSClient(uri, method, token, i)


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


def searchRecord(key, type, data):
    # search target JSON -> dictionary
    # key target is "name" or "content"
    # type is "type", default null
    # either key and type, or on the other hand
    # data is dictionaly
    import re
    for item in data:
        re.search(key, str(item['key']))
