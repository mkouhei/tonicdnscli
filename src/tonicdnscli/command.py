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


# Check text file exisitense
def checkInfile(filename):
    import os.path
    import sys
    if os.path.isfile(filename):
        domain = os.path.basename(filename).split('.txt')[0]
        return domain
    else:
        sys.stderr.write("ERROR: %s : No such file\n" % filename)
        sys.exit(1)


# Convert text file to JSON
# action: True  is for PUT/POST HTTP method
#         False is for DELETE HTTP method
def setJSON(domain, action, filename=False, record=False):
    import converter
    o = converter.JSONConvert(domain)

    # for 'bulk_create/bulk_delete'
    if filename:
        with open(filename, 'r') as f:
            o.separateInputFile(f)
            for item in o.separated_list:
                o.readRecords(item.splitlines())
                o.genData(action)

    # for 'create/delete'
    elif record:
        o.readRecords(record)
        o.genData(action)

    return o.dict_records


# get token
def token(username, password, server):
    from tdauth import Auth
    a = Auth(username, password, server)
    a.getToken()
    return a.token


# get password
def getPassword(args):
    password = ''

    # for -p option
    if args.__dict__.get('password'):
        password = args.password

    # for -P option
    elif args.__dict__.get('P'):

        while True:
            # When setting password in $HOME/.tdclirc, using it.
            if password:
                break

            # not set in $HOME/.tdclirc, attempt input prompt
            else:
                from getpass import getpass
                password = getpass(prompt='TonicDNS user password: ')

    return password


# get record parameters from command options
def getRecordParameters(obj):
    name, rtype, content, ttl, priority = \
        obj.name, obj.rtype, obj.content, obj.ttl, obj.priority
    return name, rtype, content, ttl, priority


# Convert and print JSON
def show(args):
    import sys
    import json
    domain = checkInfile(args.infile)
    action = True
    try:
        print(json.dumps(setJSON(domain, action, filename=args.infile),
                         sort_keys=True, indent=2))
    except UnicodeDecodeError as e:
        sys.stderr.write("ERROR: \"%s\" is invalid format file.\n"
                         % args.infile)
        exit(1)


# Retrieve records
def get(args):
    import processing
    password = getPassword(args)
    t = token(args.username, password, args.server)

    # When using '--search' option
    if args.__dict__.get('search'):
        keyword = args.search

    else:
        keyword = ''

    # When specified zone
    if args.__dict__.get('domain'):
        domain = args.domain
        processing.getZone(args.server, t, domain, keyword)

    # When get all zones
    else:
        processing.getAllZone(args.server, t)


# Create records
def create(args):
    import processing

    # for PUT HTTP method
    action = True

    # for create sub-command
    if (args.__dict__.get('domain') and args.__dict__.get('name')
        and args.__dict__.get('rtype') and args.__dict__.get('content')):

        from converter import JSONConvert
        domain = args.domain
        o = JSONConvert(domain)

        name, rtype, content, ttl, priority = getRecordParameters(args)
        record_dict = o.setRecord(name, rtype, content, ttl, priority)

        json = setJSON(domain, action, record=record_dict)

    # for bulk_create sub-command
    else:
        if args.__dict__.get('domain'):
            domain = args.domain
        else:
            domain = checkInfile(args.infile)
        json = setJSON(domain, action, filename=args.infile)

    password = getPassword(args)
    t = token(args.username, password, args.server)
    processing.createRecords(args.server, t, domain, json)


# Delete records
def delete(args):
    import processing

    # for DELETE HTTP method
    action = False

    # for delete sub-command
    if (args.__dict__.get('domain') and args.__dict__.get('name')
        and args.__dict__.get('rtype') and args.__dict__.get('content')):

        from converter import JSONConvert
        domain = args.domain
        o = JSONConvert(domain)

        name, rtype, content, ttl, priority = getRecordParameters(args)
        record_dict = o.setRecord(name, rtype, content, ttl, priority)

        json = setJSON(domain, action, record=record_dict)

    # for bulk_delete sub-command
    else:
        if args.__dict__.get('domain'):
            domain = args.domain
        else:
            domain = checkInfile(args.infile)
        json = setJSON(domain, action, filename=args.infile)

    password = getPassword(args)
    t = token(args.username, password, args.server)
    processing.deleteRecords(args.server, t, json)


# Retrieve template
def template_get(args):
    import processing
    password = getPassword(args)
    t = token(args.username, password, args.server)

    # When specified template identifier
    if args.__dict__.get('template'):
        template = args.template
        processing.getTemplate(args.server, t, template)

    # When get all templates
    else:
        processing.getAllTemplates(args.server, t)


# Delete template
def template_delete(args):
    import processing
    import converter

    if args.__dict__.get('template'):
        template = args.template

    password = getPassword(args)
    t = token(args.username, password, args.server)
    processing.deleteTemplate(args.server, t, template)


# Update SOA serial
def updateSOASerial(args):
    import processing

    password = getPassword(args)
    t = token(args.username, password, args.server)
    soa_content = dict(domain=args.domain)
    if args.__dict__.get('mname'):
        soa_content['mname'] = args.mname
    if args.__dict__.get('rname'):
        soa_content['rname'] = args.rname
    if args.__dict__.get('refresh'):
        soa_content['refresh'] = args.refresh
    if args.__dict__.get('retry'):
        soa_content['retry'] = args.retry
    if args.__dict__.get('expire'):
        soa_content['expire'] = args.expire
    if args.__dict__.get('minimum'):
        soa_content['minimum'] = args.minimum
    processing.updateSerial(args.server, t, soa_content)


# Create zone
def createZone(args):
    import processing
    from converter import JSONConvert

    action = True

    password = getPassword(args)
    t = token(args.username, password, args.server)

    domain = args.domain
    template = args.domain.replace('.', '_')

    master = None
    dnsaddr = args.dnsaddr
    if args.__dict__.get('S'):
        dtype = 'SLAVE'
        master = dnsaddr
    elif args.__dict__.get('N'):
        dtype = 'NATIVE'
    else:
        dtype = 'MASTER'

    # generate template data
    o = JSONConvert(domain)
    o.generateTemplate(domain, dnsaddr, desc='')

    # create template
    processing.createTemplate(args.server, t, template, o.record)

    # create zone
    processing.createZoneRecords(
        args.server, t, domain, template, dtype, master)

    # delete template
    processing.deleteTemplate(args.server, t, template)


# Delete zone
def zone_delete(args):
    import processing
    import converter

    if args.__dict__.get('domain'):
        domain = args.domain

    password = getPassword(args)
    t = token(args.username, password, args.server)
    processing.deleteZone(args.server, t, domain)


def setoption(obj, keyword, required=False):
    if keyword == 'server':
        obj.add_argument(
            '-s', dest='server', required=True,
            help='specify TonicDNS Server hostname or IP address')

    if keyword == 'username':
        obj.add_argument('-u', dest='username', required=True,
                         help='TonicDNS username')

    if keyword == 'password':
        group = obj.add_mutually_exclusive_group(required=True)
        group.add_argument('-p', dest='password',
                           help='TonicDNS password')
        group.add_argument('-P', action='store_true',
                           help='TonicDNS password prompt')

    if keyword == 'infile':
        obj.add_argument('infile', action='store',
                           help='pre-converted text file')

    if keyword == 'domain':
        obj.add_argument('--domain', action='store', required=True,
                           help='create record with specify domain')
        obj.add_argument('--name', action='store', required=True,
                         help='specify with domain option')
        obj.add_argument('--rtype', action='store', required=True,
                         help='specify with domain option')
        obj.add_argument('--content', action='store', required=True,
                         help='specify with domain option')
        obj.add_argument('--ttl', action='store', default='3600',
                     help='specify with domain option, default 3600')
        obj.add_argument('--priority', action='store', default=False,
            help='specify with domain and rtype options as MX|SRV')

    if keyword == 'template':
        msg = 'specify template identifier'
        if required:
            obj.add_argument('--template', action='store',
                             required=True, help=msg)
        else:
            obj.add_argument('--template', action='store',
                             help=msg)

    if keyword == 'search':
        obj.add_argument('--search', action='store',
                         help='partial match search')


def conn_options(obj, conn):
    if conn.get('server') and conn.get('username') and conn.get('password'):
        obj.set_defaults(server=conn.get('server'),
                         username=conn.get('username'),
                         password=conn.get('password'))

    elif conn.get('server') and conn.get('username'):
        obj.set_defaults(server=conn.get('server'),
                         username=conn.get('username'))

    if not conn.get('server'):
        setoption(obj, 'server')
    if not conn.get('username'):
        setoption(obj, 'username')
    if not conn.get('password'):
        setoption(obj, 'password')


# Define sub-commands and command line options
def parse_options():
    import argparse
    import os
    from __init__ import __version__

    server, username, password = False, False, False

    prs = argparse.ArgumentParser(description='usage')
    prs.add_argument('-v', '--version', action='version',
                        version=__version__)
    if os.environ.get('HOME'):
        CONFIGFILE = os.environ.get('HOME') + '/.tdclirc'
        if os.path.isfile(CONFIGFILE):
            server, username, password = checkConfig(CONFIGFILE)

    conn = dict(server=server, username=username, password=password)

    subprs = prs.add_subparsers(help='commands')

    # Convert and print JSON
    prsShow(subprs)

    # Retrieve records
    prsGet(subprs, conn)

    # Create record
    prsCreate(subprs, conn)

    # Create bulk_records
    prsBulkCreate(subprs, conn)

    # Delete record
    prsDelete(subprs, conn)

    # Delete bulk_records
    prsBulkDelete(subprs, conn)

    # Update SOA serial
    prsSOAUpdate(subprs, conn)

    # Create zone
    prsZoneCreate(subprs, conn)

    # Delete zone
    prsZoneDelete(subprs, conn)

    # Retrieve template
    prsTmplGet(subprs, conn)

    # Delete template
    prsTmplDelete(subprs, conn)

    args = prs.parse_args()
    return args


# Convert and print JSON
def prsShow(obj):
    prs_show = obj.add_parser('show',
                                    help='show converted JSON')
    setoption(prs_show, 'infile')
    prs_show.set_defaults(func=show)


# Retrieve records
def prsGet(obj, conn):
    prs_get = obj.add_parser(
        'get', help='retrieve all zones or records with a specific zone')
    prs_get.add_argument('--domain', action='store',
                         help='specify domain FQDN')
    conn_options(prs_get, conn)
    setoption(prs_get, 'search')
    prs_get.set_defaults(func=get)


# Create record
def prsCreate(obj, conn):
    prs_create = obj.add_parser(
        'create', help='create record of specific zone')
    setoption(prs_create, 'domain')
    conn_options(prs_create, conn)
    prs_create.set_defaults(func=create)


# Create bulk_records
def prsBulkCreate(obj, conn):
    prs_create = obj.add_parser(
        'bulk_create', help='create bulk records of specific zone')
    setoption(prs_create, 'infile')
    conn_options(prs_create, conn)
    prs_create.add_argument('--domain', action='store',
                            help='create records with specify zone')
    prs_create.set_defaults(func=create)


# Delete record
def prsDelete(obj, conn):
    prs_delete = obj.add_parser(
        'delete', help='delete a record of specific zone')
    setoption(prs_delete, 'domain')
    conn_options(prs_delete, conn)
    prs_delete.set_defaults(func=delete)


# Delete bulk_records
def prsBulkDelete(obj, conn):
    prs_delete = obj.add_parser(
        'bulk_delete', help='delete bulk records of specific zone')
    setoption(prs_delete, 'infile')
    conn_options(prs_delete, conn)
    prs_delete.add_argument('--domain', action='store',
                            help='delete records with specify zone')
    prs_delete.set_defaults(func=delete)


# Retrieve template
def prsTmplGet(obj, conn):
    prs_tmpl_get = obj.add_parser(
        'tmpl_get', help='retrieve templates')
    setoption(prs_tmpl_get, 'template')
    conn_options(prs_tmpl_get, conn)
    prs_tmpl_get.set_defaults(func=template_get)


# Delete template
def prsTmplDelete(obj, conn):
    prs_tmpl_delete = obj.add_parser(
        'tmpl_delete', help='delete template')
    setoption(prs_tmpl_delete, 'template', required=True)
    conn_options(prs_tmpl_delete, conn)
    prs_tmpl_delete.set_defaults(func=template_delete)


# Update SOA serial
def prsSOAUpdate(obj, conn):
    prs_soa = obj.add_parser('soa', help='update SOA record')
    prs_soa.add_argument('--domain', action='store', required=True,
                            help='specify domain FQDN')
    prs_soa.add_argument('--mname', action='store',
                         help='specify MNAME of SOA record')
    prs_soa.add_argument('--rname', action='store',
                         help='specify RNAME of SOA record')
    prs_soa.add_argument('--refresh', action='store', type=int,
                         help='specify REFRESH of SOA record')
    prs_soa.add_argument('--retry', action='store', type=int,
                         help='specify RETRY of SOA record')
    prs_soa.add_argument('--expire', action='store', type=int,
                         help='specify EXPIRE of SOA record')
    prs_soa.add_argument('--minimum', action='store', type=int,
                         help='specify MINIMUM of SOA record')
    conn_options(prs_soa, conn)
    prs_soa.set_defaults(func=updateSOASerial)


# Create zone
def prsZoneCreate(obj, conn):
    prs_zone_create = obj.add_parser('zone_create', help='create zone')
    prs_zone_create.add_argument(
        '--domain', action='store', required=True, help='specify zone')
    prs_zone_create.add_argument('--dnsaddr', action='store', required=True,
        help='specify IP address of DNS master')
    group_zone_create = prs_zone_create.add_mutually_exclusive_group()
    group_zone_create.add_argument('-S', action='store_true',
                                   help='create zone to SLAVE')
    group_zone_create.add_argument('-N', action='store_true',
                                   help='create zone to NATIVE')
    conn_options(prs_zone_create, conn)
    prs_zone_create.set_defaults(func=createZone)


# Delete zone
def prsZoneDelete(obj, conn):
    prs_zone_delete = obj.add_parser('zone_delete', help='delete zone')
    prs_zone_delete.add_argument('--domain', action='store', required=True,
                                 help='specify zone')
    conn_options(prs_zone_delete, conn)
    prs_zone_delete.set_defaults(func=zone_delete)


def checkConfig(filename):
    import os.path
    import sys
    if sys.version_info > (2, 6) and sys.version_info < (2, 8):
        import ConfigParser as configparser
    elif sys.version_info > (3, 0):
        import configparser as configparser
    conf = configparser.SafeConfigParser(allow_no_value=False)
    conf.read(filename)
    try:
        server = conf.get('global', 'server')
    except conigparser.NoOptionError:
        server = False
    try:
        username = conf.get('auth', 'username')
    except configparser.NoOptionError:
        username = False
    try:
        password = conf.get('auth', 'password')
    except configparser.NoOptionError:
        password = False
    return server, username, password


def main():
    import sys

    try:
        args = parse_options()
        args.func(args)
    except RuntimeError as e:
        sys.stderr.write("ERROR: %s\n" % e)
        return
    except UnboundLocalError as e:
        sys.stderr.write("ERROR: %s\n" % e)
        return

if __name__ == "__main__":
    main()
