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
from . import connect as conn


def unprovide():
    print("ERROR: This feature does not provide")
    exit(10)


# `data' is list.
# item of list is dictionary as
# 1) {"records": records}
# 2) {"name": domain, "records": records}
#This is work around, see also commit 7571109.
def createZoneRecords(server, token, domain, data, identifier):
    # ContentType: application/json
    # x-authentication-token: token
    method = 'PUT'
    uri = 'https://' + server + '/zone'

    for i, v in enumerate(data):

        if i == 0:
            from converter import JSONConvert
            obj = JSONConvert(domain)
            zone = obj.generateZone(domain, identifier, v)
            conn.tonicDNSClient(uri, method, token, zone)

        else:
            # method: PUT
            uri = 'https://' + server + '/zone/' + domain
            conn.tonicDNSClient(uri, method, token, v)


def createRecords(server, token, domain, data):
    # ContentType: application/json
    # x-authentication-token: token
    method = 'PUT'
    uri = 'https://' + server + '/zone/' + domain
    for i in data:
        conn.tonicDNSClient(uri, method, token, i)


def deleteRecords(server, token, data):
    # ContentType: application/json
    # x-authentication-token: token
    method = 'DELETE'
    uri = 'https://' + server + '/zone'
    for i in data:
        conn.tonicDNSClient(uri, method, token, i)


def getZone(server, token, domain, keyword=''):
    # x-authentication-token: token
    method = 'GET'
    uri = 'https://' + server + '/zone/' + domain
    conn.tonicDNSClient(uri, method, token, data=False, keyword=keyword)


def getAllZone(server, token):
    # x-authentication-token: token
    method = 'GET'
    uri = 'https://' + server + '/zone'
    conn.tonicDNSClient(uri, method, token, data=False)


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
    conn.tonicDNSClient(uri, method, token, data=template)


def updateTemplate(server, token, identifier, template):
    # ContentType: application/json
    # x-authentication-token: token
    method = 'POST'
    uri = 'https://' + server + '/template/' + identifier
    conn.tonicDNSClient(uri, method, token, data=template)


def deleteTemplate(server, token, template):
    # x-authentication-token: token
    method = 'DELETE'
    uri = 'https://' + server + '/template/' + template
    conn.tonicDNSClient(uri, method, token, data=False)


def getTemplate(server, token, template):
    # x-authentication-token: token
    method = 'GET'
    uri = 'https://' + server + '/template/' + template
    conn.tonicDNSClient(uri, method, token, data=False)


def getAllTemplates(server, token):
    # x-authentication-token: token
    method = 'GET'
    uri = 'https://' + server + '/template'
    conn.tonicDNSClient(uri, method, token, data=False)


def updateSerial(server, token, domain):
    # x-authentication-token: token

    # Get SOA record
    # `cur_soa` is current SOA record.
    # `new_soa` is incremental serial SOA record.
    method = 'GET'
    uri = 'https://' + server + '/zone/' + domain
    cur_soa, new_soa = conn.tonicDNSClient(uri, method, token, data=False,
                                           keyword='serial', domain=domain)
    # set JSON
    from converter import JSONConvert
    cur_o = JSONConvert(domain)
    new_o = JSONConvert(domain)
    cur_o.records = [cur_soa]
    new_o.records = [new_soa]
    cur_o.genData(False)
    new_o.genData(True)

    # Create new SOA record
    uri = 'https://' + server + '/zone/' + domain
    method = 'PUT'
    conn.tonicDNSClient(uri, method, token, new_o.dict_records[0])

    # Delete current SOA record why zone has only one SOA record.
    method = 'DELETE'
    uri = 'https://' + server + '/zone'
    conn.tonicDNSClient(uri, method, token, cur_o.dict_records[0])
