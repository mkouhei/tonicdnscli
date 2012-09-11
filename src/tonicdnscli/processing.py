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

----
`data' is list. Item of list is dictionary as
  1) {"records": records}
  2) {"name": domain, "records": records}
This is work around, see also commit 7571109.
"""
import connect
from converter import JSONConverter


def create_zone(server, token, domain, identifier, dtype, master=None):
    """Create zone records.

    Arguments:

        server:     TonicDNS API server
        token:      TonicDNS API authentication token
        domain:     Specify domain name
        identifier: Template ID
        dtype:      MASTER|SLAVE|NATIVE (default: MASTER)
        master:     master server ip address when dtype is SLAVE
                    (default: None)

    ContentType: application/json
    x-authentication-token: token
    """
    method = 'PUT'
    uri = 'https://' + server + '/zone'

    obj = JSONConverter(domain)
    obj.generate_zone(domain, identifier, dtype, master)
    connect.tonicdns_client(uri, method, token, obj.zone)


def create_records(server, token, domain, data):
    """Create records of specific domain.

    Arguments:

        server: TonicDNS API server
        token:  TonicDNS API authentication token
        domain: Specify domain name
        data:   Create records

    ContentType: application/json
    x-authentication-token: token
    """
    method = 'PUT'
    uri = 'https://' + server + '/zone/' + domain
    for i in data:
        connect.tonicdns_client(uri, method, token, i)


def delete_records(server, token, data):
    """Delete records of specific domain.

    Arguments:

        server: TonicDNS API server
        token:  TonicDNS API authentication token
        data:   Delete records

    ContentType: application/json
    x-authentication-token: token
    """
    method = 'DELETE'
    uri = 'https://' + server + '/zone'
    for i in data:
        connect.tonicdns_client(uri, method, token, i)


def get_zone(server, token, domain, keyword=''):
    """Retrieve zone records.

    Argument:

        server:  TonicDNS API server
        token:   TonicDNS API authentication token
        domain:  Specify domain name
        keyword: Search keyword

    x-authentication-token: token
    """
    method = 'GET'
    uri = 'https://' + server + '/zone/' + domain
    connect.tonicdns_client(uri, method, token, data=False, keyword=keyword)


def get_all_zone(server, token):
    """Retrieve all zones.

    Argument:

        server: TonicDNS API server
        token:  TonicDNS API authentication token

    x-authentication-token: token
    """
    method = 'GET'
    uri = 'https://' + server + '/zone'
    connect.tonicdns_client(uri, method, token, data=False)


def delete_zone(server, token, domain):
    """Delete specific zone.

    Argument:

        server: TonicDNS API server
        token:  TonicDNS API authentication token
        domain: Specify domain name

    x-authentication-token: token
    """
    method = 'DELETE'
    uri = 'https://' + server + '/zone/' + domain
    connect.tonicdns_client(uri, method, token, data=False)


def create_template(server, token, identifier, template):
    """Create template.

    Argument:

        server:     TonicDNS API server
        token:      TonicDNS API authentication token
        identifier: Template identifier
        template:   Create template datas

    ContentType: application/json
    x-authentication-token: token
    """
    method = 'PUT'
    uri = 'https://' + server + '/template/' + identifier
    connect.tonicdns_client(uri, method, token, data=template)


def delete_template(server, token, template):
    """Delete template.

    Argument:

        server:     TonicDNS API server
        token:      TonicDNS API authentication token
        template:   Delete template datas

    x-authentication-token: token
    """
    method = 'DELETE'
    uri = 'https://' + server + '/template/' + template
    connect.tonicdns_client(uri, method, token, data=False)


def get_template(server, token, template):
    """Retrieve template.

    Argument:

        server:   TonicDNS API server
        token:    TonicDNS API authentication token
        template: Retrieve template datas

    x-authentication-token: token
    """
    method = 'GET'
    uri = 'https://' + server + '/template/' + template
    connect.tonicdns_client(uri, method, token, data=False)


def get_all_templates(server, token):
    """Retrieve all templates.

    Argument:

        server:   TonicDNS API server
        token:    TonicDNS API authentication token

    x-authentication-token: token
    """
    method = 'GET'
    uri = 'https://' + server + '/template'
    connect.tonicdns_client(uri, method, token, data=False)


def update_soa_serial(server, token, soa_content):
    """Update SOA serial

    Argument:

        server:      TonicDNS API server
        token:       TonicDNS API authentication token
        soa_content: SOA record data

    x-authentication-token: token
    Get SOA record
    `cur_soa` is current SOA record.
    `new_soa` is incremental serial SOA record.
    """
    method = 'GET'
    uri = 'https://' + server + '/zone/' + soa_content.get('domain')
    cur_soa, new_soa = connect.tonicdns_client(
        uri, method, token, data=False, keyword='serial', content=soa_content)
    # set JSON

    domain = soa_content.get('domain')
    cur_o = JSONConverter(domain)
    new_o = JSONConverter(domain)
    cur_o.records = [cur_soa]
    new_o.records = [new_soa]
    cur_o.generata_data(False)
    new_o.generata_data(True)

    # Create new SOA record
    uri = 'https://' + server + '/zone/' + domain
    method = 'PUT'
    connect.tonicdns_client(uri, method, token, new_o.dict_records[0])

    # Delete current SOA record why zone has only one SOA record.
    method = 'DELETE'
    uri = 'https://' + server + '/zone'
    connect.tonicdns_client(uri, method, token, cur_o.dict_records[0])
