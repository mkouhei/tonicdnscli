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
def getJSON(domain, filename, act):
    import converter
    o = converter.JSONConvert(domain)
    with open(filename, 'r') as f:
        o.separateInputFile(f)
    for listitem in o.separated_list:
        o.readRecords(listitem.splitlines())
        o.genData(act)
    return o.dict_records


# get token
def token(username, password, server):
    from tdauth import authInfo
    a = authInfo(username, password, server)
    a.getToken()
    return a.token


# get password
def getPassword(args):
    password = ''
    if args.password:
        password = args.password
    elif args.P:
        while True:
            if password:
                break
            else:
                from getpass import getpass
                password = getpass(prompt='TonicDNS user password: ')
    return password


# Convert and print JSON
def show(args):
    import sys
    import json
    domain = checkInfile(args.infile)
    try:
        print(json.dumps(getJSON(domain, args.infile, True),
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
    if args.search:
        keyword = args.search
    else:
        keyword = ''
    if args.domain:
        domain = args.domain
        processing.getZone(args.server, t, domain, keyword)
    else:
        processing.getAllZone(args.server, t)


# Create records
def create(args):
    import processing
    domain = checkInfile(args.infile)
    password = getPassword(args)
    t = token(args.username, password, args.server)
    processing.createRecords(args.server, t, domain,
                             getJSON(domain, args.infile, True))


# Delete records
def delete(args):
    import processing
    domain = checkInfile(args.infile)
    password = getPassword(args)
    t = token(args.username, password, args.server)
    processing.deleteRecords(args.server, t,
                             getJSON(domain, args.infile, False))


# Retrieve template
def template_get(args):
    import processing
    password = getPassword(args)
    t = token(args.username, password, args.server)
    if args.template:
        template = args.template
        processing.getTemplate(args.server, t, template)
    else:
        processing.getAllTemplates(args.server, t)


# Create or update template
def template_create_or_update(args):
    import processing
    import converter
    domain = args.domain
    if args.template:
        identifier = args.template
    else:
        identifier = domain.replace('.', '_')
    o = converter.JSONConvert(domain)
    dnsaddr = args.dnsaddr
    desc = args.desc if args.desc else ''
    password = getPassword(args)
    t = token(args.username, password, args.server)
    o.generateTemplate(domain, dnsaddr, desc=desc)
    if args.template:
        processing.updateTemplate(args.server, t, identifier, o.record)
    else:
        processing.createTemplate(args.server, t, identifier, o.record)


# Delete template
def template_delete(args):
    import processing
    import converter
    password = getPassword(args)
    if args.template:
        template = args.template
    t = token(args.username, password, args.server)
    processing.deleteTemplate(args.server, t, template)


def setoption(obj, keyword, prefix=False, required=False):
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
    if keyword == 'template':
        msg = 'specify template identifier'
        if prefix:
            msg = prefix + msg
        if required:
            obj.add_argument('--template', action='store',
                             required=True, help=msg)
        else:
            obj.add_argument('--template', action='store',
                             help=msg)
    if keyword == 'search':
        obj.add_argument('--search', action='store',
                         help='partial match search')


def conn_options(obj, server=False, username=False, password=False):
    if server and username and password:
        obj.set_defaults(server=server, username=username,
                         password=password)
    elif server and username:
        obj.set_defaults(server=server, username=username)

    if not server:
        setoption(obj, 'server')
    if not username:
        setoption(obj, 'username')
    if not password:
        setoption(obj, 'password')


# Define sub-commands and command line options
def parse_options():
    import argparse
    import os
    from __init__ import __version__

    server, username, password = False, False, False

    CONFIGFILE = os.environ['HOME'] + '/.tdclirc'
    if os.path.isfile(CONFIGFILE):
        server, username, password = checkConfig(CONFIGFILE)

    prs = argparse.ArgumentParser(description='usage')
    prs.add_argument('-v', '--version', action='version',
                        version=__version__)
    prs.add_argument('--config', action='store',
                        help='config file path')

    subprs = prs.add_subparsers(help='commands')

    # Convert and print JSON
    prs_show = subprs.add_parser('show',
                                    help='show converted JSON')
    setoption(prs_show, 'infile')
    prs_show.set_defaults(func=show)

    # Retrieve records
    prs_get = subprs.add_parser(
        'get', help='retrieve records of specific zone')
    prs_get.add_argument('--domain', action='store',
                            help='specify domain FQDN')
    conn_options(prs_get, server, username, password)
    setoption(prs_get, 'search')
    prs_get.set_defaults(func=get)

    # Create records
    prs_create = subprs.add_parser(
        'create', help='create records of specific zone')
    setoption(prs_create, 'infile')
    conn_options(prs_create, server, username, password)
    prs_create.set_defaults(func=create)

    # Delete records
    prs_delete = subprs.add_parser(
        'delete', help='delete records of specific zone')
    setoption(prs_delete, 'infile')
    conn_options(prs_delete, server, username, password)
    prs_delete.set_defaults(func=delete)

    # Retrieve template
    prs_tmpl_get = subprs.add_parser(
        'tmpl_get', help='retrieve templates')
    setoption(prs_tmpl_get, 'template')
    conn_options(prs_tmpl_get, server, username, password)
    prs_tmpl_get.set_defaults(func=template_get)

    # create or update template
    prs_tmpl_create_update = subprs.add_parser(
        'tmpl_create_update', help='create or update template')
    prs_tmpl_create_update.add_argument(
        '--domain', action='store', required=True,
        help='create template with specify domain')
    setoption(prs_tmpl_create_update, 'template', 'update template with ')
    prs_tmpl_create_update.add_argument(
        '--dnsaddr', action='store', required=True,
        help='specify IP address of NS record')
    prs_tmpl_create_update.add_argument(
        '--desc', action='store', help='description')
    conn_options(prs_tmpl_create_update, server, username, password)
    prs_tmpl_create_update.set_defaults(func=template_create_or_update)

    # delete template
    prs_tmpl_delete = subprs.add_parser(
        'tmpl_delete', help='delete template')
    setoption(prs_tmpl_delete, 'template', required=True)
    conn_options(prs_tmpl_delete, server, username, password)
    prs_tmpl_delete.set_defaults(func=template_delete)

    args = prs.parse_args()
    return args


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
