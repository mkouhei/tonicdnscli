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
import sys
import json
import socket
import utils
from __init__ import __timeout__
from converter import JSONConverter
if sys.version_info > (2, 6) and sys.version_info < (2, 8):
    import urllib2 as urllib
elif sys.version_info > (3, 0):
    import urllib.request as urllib


def get_token(username, password, server):
    """Retrieve token of TonicDNS API.

    Arguments:

        usename:  TonicDNS API username
        password: TonicDNS API password
        server:   TonicDNS API server
    """
    method = 'PUT'
    uri = 'https://' + server + '/authenticate'
    token = ''

    authinfo = {
        "username": username,
        "password": password,
        "local_user": username
        }

    token = tonicdns_client(uri, method, token, data=authinfo)

    return token


def tonicdns_client(uri, method, token='', data='', keyword='',
                    content='', raw_flag=False):
    """TonicDNS API client

    Arguments:

        uri:      TonicDNS API URI
        method:   TonicDNS API request method
        token:    TonicDNS API authentication token
        data:     Post data to TonicDNS API
        keyword:  Processing keyword of response
        content:  data exist flag
        raw_flag: True is return response data, False is pretty printing
    """
    res = request(uri, method, data, token)
    if token:
        if keyword == 'serial':
            args = {"token": token, "keyword": keyword, "content": content}
            cur_soa, new_soa = response(uri, method, res, **args)
            return cur_soa, new_soa

        else:
            if content is None:
                args = {"token": token, "keyword": keyword,
                        "content": content.get('domain')}
                response(uri, method, res, **args)
            else:
                # get sub command
                args = {"token": token, "keyword": keyword,
                        "raw_flag": raw_flag}
                data = response(uri, method, res, **args)
                return data

    else:
        args = {"token": token, "keyword": keyword}
        token = response(uri, method, res, **args)
        return token


def request(uri, method, data, token=''):
    """Request to TonicDNS API.

    Arguments:

        uri:     TonicDNS API URI
        method:  TonicDNS API request method
        data:    Post data to TonicDNS API
        token:   TonicDNS API authentication token
    """
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


def response(uri, method, res, token='', keyword='',
             content='', raw_flag=False):
    """Response of tonicdns_client request

    Arguments:

        uri:      TonicDNS API URI
        method:   TonicDNS API request method
        res:      Response of against request to TonicDNS API
        token:    TonicDNS API token
        keyword:  Processing keyword
        content:  JSON data
        raw_flag: True is return responsed raw data, False is pretty print
    """
    if method == 'GET' or (method == 'PUT' and not token):
        # response body
        data = res.read()
        data_utf8 = data.decode('utf-8')
        if token:
            datas = json.loads(data_utf8)
        else:
            token = json.loads(data_utf8)['hash']
            return token

        if keyword == 'serial':
            # filtering with keyword
            record = search_record(datas, 'SOA')[0]

            # if SOA record, remove priority unnecessary
            del record['priority']

            # override ttl
            record['ttl'] = int(record['ttl'])

            c = JSONConverter(content['domain'])
            new_record = c.get_soa(record, content)
            return record, new_record

        elif keyword:
            # '--search' option of 'get' subcommand
            records = search_record(datas, keyword)
            datas.update({"records": records})

        if uri.split('/')[3] == 'template':
            # 'tmpl_get' subcommand

            if len(uri.split('/')) == 5:
                # when specify template identfier
                print_formatted(datas)

            else:
                # when get all templates
                for data in datas:
                    print_formatted(data)

        else:
            # 'get' subcommand
            if raw_flag:
                return datas
            else:
                print_formatted(datas)

    else:
        # response non JSON data
        data = res.read()
        print(data)


def search_record(datas, keyword):
    """Search target JSON -> dictionary

    Arguments:

        datas: dictionary of record datas
        keyword: search keyword (default is null)

    Key target is "name" or "content" or "type". default null.
    Either key and type, or on the other hand.

    When keyword has include camma ",",
    Separate keyword to name, type, content.
    """

    key_name, key_type, key_content = False, False, False

    if keyword.find(',') > -1:
        if len(keyword.split(',')) == 3:
            key_content = keyword.split(',')[2]
        key_name = keyword.split(',')[0]
        key_type = keyword.split(',')[1]

    result = []

    for record in datas['records']:

        if key_name and key_type:
            if key_content:
                if (record['name'].find(key_name) > -1 and
                    record['type'] == key_type and
                    record['content'].find(key_content) > -1):
                    result.append(record)
            else:
                if (record['name'].find(key_name) > -1 and
                    record['type'] == key_type):
                    result.append(record)

        elif (record['name'].find(keyword) >= 0 or
            record['content'].find(keyword) >= 0 or
            record['type'] == keyword):
            result.append(record)

    return result


def print_formatted(datas):
    """Pretty print JSON DATA

    Argument:

        datas: dictionary of data
    """
    if not datas:
        print("No data")
        exit(1)

    if isinstance(datas, list):
        # get all zones
        # API /zone without :identifier
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

        # print header
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

    elif datas.get('identifier'):
        # for template
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
