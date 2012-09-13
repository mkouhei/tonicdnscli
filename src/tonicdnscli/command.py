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
import os.path
import sys
import json
import argparse
import os
import copy
import processing
import connect
import utils
from __init__ import __version__
from converter import JSONConverter
if sys.version_info > (2, 6) and sys.version_info < (2, 8):
    import ConfigParser as configparser
elif sys.version_info > (3, 0):
    import configparser as configparser


def check_infile(filename):
    """Check text file exisitense.

    Argument:

        filename: text file of bulk updating
    """
    if os.path.isfile(filename):
        domain = os.path.basename(filename).split('.txt')[0]
        return domain
    else:
        sys.stderr.write("ERROR: %s : No such file\n" % filename)
        sys.exit(1)


def set_json(domain, action, filename=False, record=False):
    """Convert text file to JSON.

    Arguments:

        domain:   domain name of updating target
        action:   True ; for PUT/POST HTTP method
                  False; for DELETE HTTP method
        filename: text file of bulk updating (default is False)
        record:   json record of updating single record (default is False)
    """
    o = JSONConverter(domain)

    if filename:
        # for 'bulk_create/bulk_delete'
        with open(filename, 'r') as f:
            o.separate_input_file(f)
            for item in o.separated_list:
                o.read_records(item.splitlines())
                o.generata_data(action)

    elif record:
        # for 'create/delete'
        o.read_records(record)
        o.generata_data(action)

    return o.dict_records


def get_password(args):
    """Get password

    Argument:

        args: arguments object

    Return: password string
    """
    password = ''

    if args.__dict__.get('password'):
        # Specify password as argument (for -p option)
        password = args.password

    elif args.__dict__.get('P'):
        # Enter password interactively (for -P option)
        while True:
            # When setting password in $HOME/.tdclirc, using it.
            if password:
                break

            else:
                # Not set in $HOME/.tdclirc, attempt input prompt
                from getpass import getpass
                password = getpass(prompt='TonicDNS user password: ')

    return password


def get_record_params(args):
    """Get record parameters from command options.

    Argument:

        args: arguments object
    """
    name, rtype, content, ttl, priority = (
        args.name, args.rtype, args.content, args.ttl, args.priority)
    return name, rtype, content, ttl, priority


def show(args):
    """Convert and print JSON.

    Argument:

        args: arguments object
    """
    domain = check_infile(args.infile)
    action = True
    try:
        print(json.dumps(set_json(domain, action, filename=args.infile),
                         sort_keys=True, indent=2))
    except UnicodeDecodeError as e:
        sys.stderr.write("ERROR: \"%s\" is invalid format file.\n"
                         % args.infile)
        exit(1)


def get(args):
    """Retrieve records.

    Argument:

        args: arguments object
    """
    password = get_password(args)
    token = connect.get_token(args.username, password, args.server)

    if args.__dict__.get('search'):
        # When using '--search' option
        keyword = args.search

    else:
        keyword = ''

    if args.__dict__.get('raw_flag'):
        raw_flag = True
    else:
        raw_flag = False

    if args.__dict__.get('domain'):
        # When specified zone
        domain = args.domain
        data = processing.get_zone(args.server, token, domain,
                                   keyword, raw_flag)
        return data

    else:
        # When get all zones
        processing.get_all_zone(args.server, token)


def create(args):
    """Create records.

    Argument:

        args: arguments object
    """
    # for PUT HTTP method
    action = True

    if (args.__dict__.get('domain') and args.__dict__.get('name')
        and args.__dict__.get('rtype') and args.__dict__.get('content')):
        # for create sub-command

        domain = args.domain
        o = JSONConverter(domain)

        name, rtype, content, ttl, priority = get_record_params(args)
        record_dict = o.set_record(name, rtype, content, ttl, priority)

        json = set_json(domain, action, record=record_dict)

    else:
        # for bulk_create sub-command
        if args.__dict__.get('domain'):
            domain = args.domain
        else:
            domain = check_infile(args.infile)
        json = set_json(domain, action, filename=args.infile)

    password = get_password(args)
    token = connect.get_token(args.username, password, args.server)
    processing.create_records(args.server, token, domain, json)

    if args.auto_update_soa == 'True':
        update_soa_serial(args)


def delete(args):
    """Delete records.

    Argument:

        args: arguments object
    """
    # for DELETE HTTP method
    action = False

    if (args.__dict__.get('domain') and args.__dict__.get('name')
        and args.__dict__.get('rtype') and args.__dict__.get('content')):
        # for delete sub-command

        domain = args.domain
        o = JSONConverter(domain)

        name, rtype, content, ttl, priority = get_record_params(args)
        record_dict = o.set_record(name, rtype, content, ttl, priority)

        json = set_json(domain, action, record=record_dict)

    else:
        # for bulk_delete sub-command
        if args.__dict__.get('domain'):
            domain = args.domain
        else:
            domain = check_infile(args.infile)
        json = set_json(domain, action, filename=args.infile)

    password = get_password(args)
    token = connect.get_token(args.username, password, args.server)
    processing.delete_records(args.server, token, json)

    if args.auto_update_soa == 'True':
        update_soa_serial(args)


def update(args):
    """Update a record.

    Argument:

        args: arguments object

    Firstly call delete(), then create().
    """
    # Check specifying some new values
    if (not args.__dict__.get('new_type') and
        not args.__dict__.get('new_content') and
        not args.__dict__.get('new_ttl') and
        not args.__dict__.get('new_priority')):
        utils.error("Not update any values.")

    args.__dict__['search'] = (args.__dict__.get('name') + ',' +
                               args.__dict__.get('rtype') + ',' +
                               args.__dict__.get('content'))

    args.__dict__['raw_flag'] = True
    data = get(args)
    if len(data.get('records')) == 1:
        cur_ttl = data.get('records')[0].get('ttl')
        cur_priority = data.get('records')[0].get('priority')
    elif len(data.get('records')) > 1:
        utils.error("Match multiple records")
    else:
        utils.error("No match records")

    new_args = copy.copy(args)

    if new_args.__dict__.get('new_type'):
        new_args.__dict__['rtype'] = new_args.__dict__.get('new_type')

    if new_args.__dict__.get('new_content'):
        new_args.__dict__['content'] = new_args.__dict__.get('new_content')

    if new_args.__dict__.get('new_ttl'):
        new_args.__dict__['ttl'] = new_args.__dict__.get('new_ttl')
    else:
        new_args.__dict__['ttl'] = cur_ttl

    if new_args.__dict__.get('new_priority'):
        new_args.__dict__['priority'] = new_args.__dict__.get('new_priority')
    else:
        if cur_priority:
            new_args.__dict__['priority'] = cur_priority

    delete(args)
    create(new_args)


def retrieve_tmpl(args):
    """Retrieve template.

    Argument:

        args: arguments object
    """
    password = get_password(args)
    token = connect.get_token(args.username, password, args.server)

    if args.__dict__.get('template'):
        # When specified template identifier
        template = args.template
        processing.get_template(args.server, token, template)

    else:
        # When get all templates
        processing.get_all_templates(args.server, token)


def delete_tmpl(args):
    """Delete template.

    Argument:

        args: arguments object
    """
    if args.__dict__.get('template'):
        template = args.template

    password = get_password(args)
    token = connect.get_token(args.username, password, args.server)
    processing.delete_template(args.server, token, template)


def update_soa_serial(args):
    """Update SOA serial.

    Argument:

        args: arguments object
    """
    password = get_password(args)
    token = connect.get_token(args.username, password, args.server)
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
    processing.update_soa_serial(args.server, token, soa_content)


def create_zone(args):
    """Create zone.

    Argument:

        args: arguments object
    """
    action = True

    password = get_password(args)
    token = connect.get_token(args.username, password, args.server)

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
    o = JSONConverter(domain)
    o.generate_template(domain, dnsaddr, desc='')

    # create template
    processing.create_template(args.server, token, template, o.record)

    # create zone
    processing.create_zone(args.server, token, domain, template, dtype, master)

    # delete template
    processing.delete_template(args.server, token, template)


def delete_zone(args):
    """Delete zone.

    Argument:

        args: arguments object
    """
    if args.__dict__.get('domain'):
        domain = args.domain

    password = get_password(args)
    token = connect.get_token(args.username, password, args.server)
    processing.delete_zone(args.server, token, domain)


def set_option(prs, keyword, required=False):
    """Set options of command line.

    Arguments:

        prs:      parser object of argparse
        keyword:  processing keyword
        required: True is required option (default is False)
    """
    if keyword == 'server':
        prs.add_argument(
            '-s', dest='server', required=True,
            help='specify TonicDNS Server hostname or IP address')

    if keyword == 'username':
        prs.add_argument('-u', dest='username', required=True,
                         help='TonicDNS username')

    if keyword == 'password':
        group = prs.add_mutually_exclusive_group(required=True)
        group.add_argument('-p', dest='password',
                           help='TonicDNS password')
        group.add_argument('-P', action='store_true',
                           help='TonicDNS password prompt')

    if keyword == 'infile':
        prs.add_argument('infile', action='store',
                           help='pre-converted text file')

    if keyword == 'domain':
        prs.add_argument('--domain', action='store', required=True,
                           help='create record with specify domain')
        prs.add_argument('--name', action='store', required=True,
                         help='specify with domain option')
        prs.add_argument('--rtype', action='store', required=True,
                         help='specify with domain option')
        prs.add_argument('--content', action='store', required=True,
                         help='specify with domain option')
        prs.add_argument('--ttl', action='store', default='3600',
                     help='specify with domain option, default 3600')
        prs.add_argument('--priority', action='store', default=False,
            help='specify with domain and rtype options as MX|SRV')

    if keyword == 'update':
        prs.add_argument('--new-type', action='store',
                         help='specify new value with domain option')
        prs.add_argument('--new-content', action='store',
                         help='specify new value with domain option')
        prs.add_argument('--new-ttl', action='store',
                         help='specify new value with domain option')
        prs.add_argument('--new-priority', action='store',
                         help='specify new value with domain option')

    if keyword == 'template':
        msg = 'specify template identifier'
        if required:
            prs.add_argument('--template', action='store',
                             required=True, help=msg)
        else:
            prs.add_argument('--template', action='store',
                             help=msg)

    if keyword == 'search':
        prs.add_argument('--search', action='store',
                         help='partial match search or refine search.\
                         latter syntax is "name,rtype,content"')


def conn_options(prs, conn):
    """Set options of connecting to TonicDNS API server

    Arguments:

        prs:  parser object of argparse
        conn: dictionary of connection information
    """
    if conn.get('server') and conn.get('username') and conn.get('password'):
        prs.set_defaults(server=conn.get('server'),
                         username=conn.get('username'),
                         password=conn.get('password'))

    elif conn.get('server') and conn.get('username'):
        prs.set_defaults(server=conn.get('server'),
                         username=conn.get('username'))

    if conn.get('auto_update_soa'):
        prs.set_defaults(auto_update_soa=conn.get('auto_update_soa'))
    else:
        prs.set_defaults(auto_update_soa=False)

    if not conn.get('server'):
        set_option(prs, 'server')
    if not conn.get('username'):
        set_option(prs, 'username')
    if not conn.get('password'):
        set_option(prs, 'password')


def parse_options():
    """Define sub-commands and command line options."""

    server, username, password, auto_update_soa = False, False, False, False

    prs = argparse.ArgumentParser(description='usage')
    prs.add_argument('-v', '--version', action='version',
                        version=__version__)
    if os.environ.get('HOME'):
        config_file = os.environ.get('HOME') + '/.tdclirc'
        if os.path.isfile(config_file):
            (server, username,
             password, auto_update_soa) = check_config(config_file)

    conn = dict(server=server, username=username,
                password=password, auto_update_soa=auto_update_soa)

    subprs = prs.add_subparsers(help='commands')

    # Convert and print JSON
    parse_show(subprs)

    # Retrieve records
    parse_get(subprs, conn)

    # Create record
    parse_create(subprs, conn)

    # Create bulk_records
    parse_bulk_create(subprs, conn)

    # Delete record
    parse_delete(subprs, conn)

    # Delete bulk_records
    parse_bulk_delete(subprs, conn)

    # Update a record
    parse_update(subprs, conn)

    # Update SOA serial
    parse_update_soa(subprs, conn)

    # Create zone
    parse_create_zone(subprs, conn)

    # Delete zone
    parse_delete_zone(subprs, conn)

    # Retrieve template
    parse_get_tmpl(subprs, conn)

    # Delete template
    parse_delete_tmpl(subprs, conn)

    args = prs.parse_args()
    return args


def parse_show(prs):
    """Convert and print JSON.

    Argument:

        prs:  parser object of argparse
    """
    prs_show = prs.add_parser('show',
                                    help='show converted JSON')
    set_option(prs_show, 'infile')
    prs_show.set_defaults(func=show)


def parse_get(prs, conn):
    """Retrieve records.

    Arguments:

        prs:  parser object of argparse
        conn: dictionary of connection information
    """
    prs_get = prs.add_parser(
        'get', help='retrieve all zones or records with a specific zone')
    prs_get.add_argument('--domain', action='store',
                         help='specify domain FQDN')
    conn_options(prs_get, conn)
    set_option(prs_get, 'search')
    prs_get.set_defaults(func=get)


def parse_create(prs, conn):
    """Create record.

    Arguments:

        prs:  parser object of argparse
        conn: dictionary of connection information
    """
    prs_create = prs.add_parser(
        'create', help='create record of specific zone')
    set_option(prs_create, 'domain')
    conn_options(prs_create, conn)
    prs_create.set_defaults(func=create)


def parse_bulk_create(prs, conn):
    """Create bulk_records.

    Arguments:

        prs:  parser object of argparse
        conn: dictionary of connection information
    """
    prs_create = prs.add_parser(
        'bulk_create', help='create bulk records of specific zone')
    set_option(prs_create, 'infile')
    conn_options(prs_create, conn)
    prs_create.add_argument('--domain', action='store',
                            help='create records with specify zone')
    prs_create.set_defaults(func=create)


def parse_delete(prs, conn):
    """Delete record.

    Arguments:

        prs:  parser object of argparse
        conn: dictionary of connection information
    """
    prs_delete = prs.add_parser(
        'delete', help='delete a record of specific zone')
    set_option(prs_delete, 'domain')
    conn_options(prs_delete, conn)
    prs_delete.set_defaults(func=delete)


def parse_bulk_delete(prs, conn):
    """Delete bulk_records.

    Arguments:

        prs:  parser object of argparse
        conn: dictionary of connection information
    """
    prs_delete = prs.add_parser(
        'bulk_delete', help='delete bulk records of specific zone')
    set_option(prs_delete, 'infile')
    conn_options(prs_delete, conn)
    prs_delete.add_argument('--domain', action='store',
                            help='delete records with specify zone')
    prs_delete.set_defaults(func=delete)


def parse_update(prs, conn):
    """Update a record.

    Arguments:

        prs:  parser object of argparse
        conn: dictionary of connection information
    """

    prs_update = prs.add_parser(
        'update', help='update record of specific zone')
    set_option(prs_update, 'domain')
    set_option(prs_update, 'update')
    conn_options(prs_update, conn)
    prs_update.set_defaults(func=update)


def parse_get_tmpl(prs, conn):
    """Retrieve template.

    Arguments:

        prs:  parser object of argparse
        conn: dictionary of connection information
    """
    prs_tmpl_get = prs.add_parser(
        'tmpl_get', help='retrieve templates')
    set_option(prs_tmpl_get, 'template')
    conn_options(prs_tmpl_get, conn)
    prs_tmpl_get.set_defaults(func=retrieve_tmpl)


def parse_delete_tmpl(prs, conn):
    """Delete template.

    Arguments:

        prs:  parser object of argparse
        conn: dictionary of connection information
    """
    prs_tmpl_delete = prs.add_parser(
        'tmpl_delete', help='delete template')
    set_option(prs_tmpl_delete, 'template', required=True)
    conn_options(prs_tmpl_delete, conn)
    prs_tmpl_delete.set_defaults(func=delete_tmpl)


def parse_update_soa(prs, conn):
    """Update SOA serial.

    Arguments:

        prs:  parser object of argparse
        conn: dictionary of connection information
    """
    prs_soa = prs.add_parser('soa', help='update SOA record')
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
    prs_soa.set_defaults(func=update_soa_serial)


def parse_create_zone(prs, conn):
    """Create zone.

    Arguments:

        prs:  parser object of argparse
        conn: dictionary of connection information
    """
    prs_zone_create = prs.add_parser('zone_create', help='create zone')
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
    prs_zone_create.set_defaults(func=create_zone)


def parse_delete_zone(prs, conn):
    """Delete zone.

    Arguments:

        prs:  parser object of argparse
        conn: dictionary of connection information
    """
    prs_zone_delete = prs.add_parser('zone_delete', help='delete zone')
    prs_zone_delete.add_argument('--domain', action='store', required=True,
                                 help='specify zone')
    conn_options(prs_zone_delete, conn)
    prs_zone_delete.set_defaults(func=delete_zone)


def check_config(filename):
    """Check configuration file of TonicDNS CLI.

    Argument:

        filename: config file name (default is ~/.tdclirc)
    """
    conf = configparser.SafeConfigParser(allow_no_value=False)
    conf.read(filename)
    try:
        server = conf.get('global', 'server')
    except configparser.NoSectionError:
        server = False
    except configparser.NoOptionError:
        server = False
    try:
        username = conf.get('auth', 'username')
    except configparser.NoSectionError:
        username = False
    except configparser.NoOptionError:
        username = False
    try:
        password = conf.get('auth', 'password')
    except configparser.NoSectionError:
        password = False
    except configparser.NoOptionError:
        password = False
    try:
        auto_update_soa = conf.get('global', 'soa_update')
    except configparser.NoSectionError:
        auto_update_soa = False
    except configparser.NoOptionError:
        auto_update_soa = False

    return server, username, password, auto_update_soa


def main():

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
