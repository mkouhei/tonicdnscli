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
from . import __timeout__


def tonicDNSClient(uri, method, token='', data='', keyword='', domain=''):
    res = request(uri, method, data, token)
    if token:
        if keyword == 'serial':
            cur_soa, new_soa = response(uri, method,
                                        res, token, keyword, domain)
            return cur_soa, new_soa
        else:
            response(uri, method, res, token, keyword, domain)
    else:
        token = response(uri, method, res, token, keyword, domain)
        return token


def request(uri, method, data, token=''):
    import sys
    import json
    if sys.version_info > (2, 6) and sys.version_info < (2, 8):
        import urllib2 as urllib
    elif sys.version_info > (3, 0):
        import urllib.request as urllib
    import socket
    socket.setdefaulttimeout(__timeout__)

    obj = urllib.build_opener(urllib.HTTPHandler)

    # encoding json
    encoded = json.JSONEncoder(object).encode(data)
    # encoding utf8
    data_utf8 = encoded.encode('utf-8')
    req = urllib.Request(uri, data=data_utf8)

    # When encoded(=data) is False, retrieve data as GET method.
    if encoded:
        req.add_header('Content-Type', 'application/json')

    if token:
        req.add_header('x-authentication-token', token)

    req.get_method = lambda: method

    try:
        res = obj.open(req)
        return res

    except urllib.URLError as e:
        sys.stderr.write("ERROR: %s\n" % e)
        exit(1)

    except urllib.HTTPError as e:
        sys.stderr.write("ERROR: %s\n" % e)
        exit(1)


# separated from request (tonicDNSClient)
def response(uri, method, res, token='', keyword='', domain=''):
    import json

    # response body
    if method == 'GET' or (method == 'PUT' and not token):

        data = res.read()
        data_utf8 = data.decode('utf-8')
        if token:
            datas = json.loads(data_utf8)
        else:
            token = json.loads(data_utf8)['hash']
            return token

        # filtering with keyword
        if keyword == 'serial':
            from converter import JSONConvert
            record = searchRecord(datas, 'SOA')[0]

            # if SOA record, remove priority unnecessary
            del record['priority']

            # override ttl
            record['ttl'] = int(record['ttl'])

            c = JSONConvert(domain)
            new_record = c.getSOA(record)
            return record, new_record

        # '--search' option of 'get' subcommand
        elif keyword:
            records = searchRecord(datas, keyword)
            datas.update({"records": records})

        # 'tmpl_get' subcommand
        if uri.split('/')[3] == 'template':

            # when specify template identfier
            if len(uri.split('/')) == 5:
                formattedPrint(datas)

            # when get all templates
            else:
                for data in datas:
                    formattedPrint(data)

        # 'get' subcommand
        else:
            formattedPrint(datas)

    # response non JSON data
    else:
        data = res.read()
        print(data)


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


def formattedPrint(datas):
    import sys
    if sys.version_info > (2, 6) and sys.version_info < (2, 8):
        import utils2 as utils
    elif sys.version_info > (3, 0):
        import utils3 as utils

    if not datas:
        print("No data")
        exit(1)

    # get all zones
    # API /zone without :identifier
    if isinstance(datas, list):
        hr()
        print('%-20s %-8s %-12s'
              % ('name', 'type', 'notified_serial'))
        hr()
        for record in datas:

            # print 'NAME'
            utils.print_inline("%(name)-20s" % record)

            # print 'TYPE' of SOA record
            utils.print_inline("%(type)-8s" % record)

            if record.get('notified_serial'):
                print("%(notified_serial)s" % record)
            else:
                print('')

        exit(0)

    elif datas.get('records'):
        print("domain: %(name)s" % datas)

        if datas.get('type') == 'MASTER' and datas.get('notified_serial'):
            print("serial: %(notified_serial)s" % datas)

        print("DNS   : %(type)s" % datas)

        # header
        hr()
        print('%-33s %-5s %-25s %-5s %-3s'
              % ('name', 'type', 'content', 'ttl', 'prio'))
        hr()

        for record in datas.get('records'):

            # print 'NAME'
            utils.print_inline("%(name)-33s" % record)

            # print 'TYPE' of SOA record
            if record.get('type') == 'SOA':
                print("%(type)-5s" % record)

            # print 'TYPE' of non SOA record
            else:
                utils.print_inline("%(type)-5s" % record)

            # print 'CONTENT' of non SOA
            if record.get('type') == 'SOA':
                utils.print_inline(">\t\t%(content)-25s " % record)

            # print 'CONTENT' of SOA record
            else:
                utils.print_inline("%(content)-25s" % record)

            # print TTL, and PRIORITY for MX, SRV record
            if record.get('priority'):
                utils.print_inline("%(ttl)5s" % record)
                print("%(priority)2s" % record)

            # print ttl for non SOA record
            else:
                print("%(ttl)5s " % record)

        hr()

    # for template
    elif datas.get('identifier'):
        print("identifier : %(identifier)s" % datas)
        print("description: %(description)s" % datas)
        hr()
        print('%-33s %-5s %-25s %-5s %-3s'
              % ('name', 'type', 'content', 'ttl', 'prio'))

        for record in datas.get('entries'):

            # print 'NAME'
            utils.print_inline("%(name)-33s" % record)

            # print 'TYPE' for SOA
            if record.get('type') == 'SOA':
                print("%(type)-5s" % record)

            # print 'TYPE' for non SOA
            else:
                utils.print_inline("%(type)-5s" % record)

            # print 'CONTENT' for SOA
            if record.get('type') == 'SOA':
                utils.print_inline("> %(content)-25s " % record)

            # print 'CONTENT' for non SOA
            else:
                utils.print_inline("%(content)-24s" % record)

            # print 'TTL', and 'PRIORITY'
            if record.get('priority') is not None:
                utils.print_inline("%(ttl)5s" % record)
                print("%(priority)2s" % record)

            # print
            else:
                print("%(ttl)5s " % record)
        hr()
    else:
        print("No match records")


# print horizontal line
def hr():
    print('=' * 78)
