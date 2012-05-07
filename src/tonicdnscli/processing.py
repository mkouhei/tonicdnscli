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


def tonicDNSClient(uri, method, token, data, keyword=''):
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
        # filtering with keyword
        if keyword:
            records = searchRecord(datas, keyword)
            datas.update({"records": records})
        if uri.split('/')[3] == 'template':
            if len(uri.split('/')) == 5:
                formattedPrint(datas)
            else:
                for data in datas:
                    formattedPrint(data)
        else:
            formattedPrint(datas)
    else:
        data = url.read()
        print(data)


def formattedPrint(datas):
    import sys
    if sys.version_info > (2, 6) and sys.version_info < (2, 8):
        import utils2 as utils
    elif sys.version_info > (3, 0):
        import utils3 as utils
    if not datas:
        print("No data")
        exit(1)
    if datas.get('records'):
        print("domain: %(name)s" % datas)
        if datas.get('type') == 'MASTER':
            print("serial: %(notified_serial)s" % datas)
        print("DNS   : %(type)s" % datas)
        hr()
        print('%-33s %-5s %-25s %-5s %-3s'
              % ('name', 'type', 'content', 'ttl', 'prio'))
        hr()
        for record in datas.get('records'):
            utils.print_inline("%(name)-33s" % record)
            if record.get('type') == 'SOA':
                print("%(type)-5s" % record)
            else:
                utils.print_inline("%(type)-5s" % record)
            if record.get('type') == 'SOA':
                utils.print_inline(">\t\t%(content)-25s " % record)
            else:
                utils.print_inline("%(content)-25s" % record)
            if record.get('priority'):
                utils.print_inline("%(ttl)5s" % record)
                print("%(priority)2s" % record)
            else:
                print("%(ttl)5s " % record)
        hr()
    elif datas.get('identifier'):
        print("identifier : %(identifier)s" % datas)
        print("description: %(description)s" % datas)
        hr()
        print('%-33s %-5s %-25s %-5s %-3s'
              % ('name', 'type', 'content', 'ttl', 'prio'))
        for record in datas.get('entries'):
            utils.print_inline("%(name)-33s" % record)
            if record.get('type') == 'SOA':
                print("%(type)-5s" % record)
            else:
                utils.print_inline("%(type)-5s" % record)
            if record.get('type') == 'SOA':
                utils.print_inline("> %(content)-25s " % record)
            else:
                utils.print_inline("%(content)-24s" % record)
            if record.get('priority') != None:
                utils.print_inline("%(ttl)5s" % record)
                print("%(priority)2s" % record)
            else:
                print("%(ttl)5s " % record)
        hr()
    else:
        print("No match records")


def hr():
    print('=' * 78)


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


def getZone(server, token, domain, keyword=''):
    # x-authentication-token: token
    method = 'GET'
    uri = 'https://' + server + '/zone/' + domain
    tonicDNSClient(uri, method, token, data=False, keyword=keyword)


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


def createTemplate(server, token, identifier, template):
    # ContentType: application/json
    # x-authentication-token: token
    method = 'PUT'
    uri = 'https://' + server + '/template/' + identifier
    tonicDNSClient(uri, method, token, data=template)


def updateTemplate(server, token, identifier, template):
    # ContentType: application/json
    # x-authentication-token: token
    method = 'POST'
    uri = 'https://' + server + '/template/' + identifier
    tonicDNSClient(uri, method, token, data=template)


def deleteTemplate(server, token, template):
    # x-authentication-token: token
    method = 'DELETE'
    uri = 'https://' + server + '/template/' + template
    tonicDNSClient(uri, method, token, data=False)


def getTemplate(server, token, template):
    # x-authentication-token: token
    method = 'GET'
    uri = 'https://' + server + '/template/' + template
    tonicDNSClient(uri, method, token, data=False)


def getAllTemplates(server, token):
    # x-authentication-token: token
    method = 'GET'
    uri = 'https://' + server + '/template'
    tonicDNSClient(uri, method, token, data=False)


def searchRecord(datas, keyword):
    # search target JSON -> dictionary
    # key target is "name" or "content"
    # type is "type", default null
    # either key and type, or on the other hand
    # data is dictionaly
    result = []
    for record in datas['records']:
        if record['name'].find(keyword) >= 0 or \
                record['content'].find(keyword) >= 0 or \
                record['type'] == keyword:
            result.append(record)
    return result
