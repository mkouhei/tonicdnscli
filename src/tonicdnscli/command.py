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


def parse_options():
    import sys
    import argparse
    from __init__ import __version__

    parser = argparse.ArgumentParser(description='usage')

    parser.add_argument('-v', '--version', action='version',
                        version=__version__)

    subparsers = parser.add_subparsers(help='sub-commands')
    parser_show = subparsers.add_parser('show',
                                         help='show converted JSON')
    parser_show.add_argument('domain', action='store', 
                                 help='specify domain name')

    parser_retrieve = subparsers.add_parser('retrieve',
                                            help='retrieve records of specific zone')
    parser_retrieve.add_argument('domain', action='store', 
                                 help='specify domain FQDN')
    parser_retrieve.add_argument('-s', dest='server',
                                 help='specify TonicDNS FQDN')
    parser_retrieve.add_argument('-u', dest='user',
                                 help='TonicDNS username')
    parser_retrieve.add_argument('-p', dest='password',
                                 help='TonicDNS password')
    parser_retrieve.add_argument('-P', action='store_true',
                                 help='TonicDNS password prompt')

    parser_create = subparsers.add_parser('create',
                                          help='create records of specific zone')
    parser_create.add_argument('infile', action='store', 
                                 help='pre-converted text file')
    parser_create.add_argument('-s', dest='server',
                               help='specify TonicDNS FQDN')
    parser_create.add_argument('-u', dest='user',
                               help='TonicDNS username')
    parser_create.add_argument('-p', dest='password',
                               help='TonicDNS password')
    parser_create.add_argument('-P', action='store_true',
                               help='TonicDNS password prompt')

    parser_delete = subparsers.add_parser('delete',
                                          help='delete records of specific zone')
    parser_delete.add_argument('infile', action='store', 
                                 help='pre-converted text file')
    parser_delete.add_argument('-s', dest='server',
                               help='specify TonicDNS FQDN')
    parser_delete.add_argument('-u', dest='user',
                               help='TonicDNS username')
    parser_delete.add_argument('-p', dest='password',
                               help='TonicDNS password')
    parser_delete.add_argument('-P', action='store_true',
                               help='TonicDNS password prompt')

    args = parser.parse_args()

    if len(args) == 0:
        parser.print_help()
        sys.exit(0)

    return options, args


def main():
    import os.path
    import sys
    import json
    import converter
    import tdauth
    import processing as p

    try:
        options, args = parse_options()
    except RuntimeError as e:
        sys.stderr.write("ERROR: %s\n" % e)
        return

    if options.delete:
        act = False
    else:
        act = True

    filename = args[0]
    if os.path.isfile(filename):
        domain = os.path.basename(filename).split('.txt')[0]
        f = open(filename, 'r')

    o = converter.JSONConvert(domain)
    o.separateInputFile(f)
    for listitem in o.separated_list:
        o.readRecords(listitem.splitlines())
        o.genData(act)

        if options.show:
            print(json.dumps(o.dict_records, sort_keys=True, indent=2))
        else:
            dict_records = o.dict_records
            if options.fqdn:
                server = options.fqdn
            if options.username:
                username = options.username
            if options.password:
                password = options.password
            elif options.P:
                import getpass
                password = getpass.getpass(prompt='TonicDNS user password: ')

            try:
                a = tdauth.authInfo(username, password, server)
                a.getToken()

                # Retrieve zone records
                if options.retrieve:
                    p.getZone(server, a.token, domain)
                    exit

                # Retrieve all zones
                #p.getAllZone(server, a.token)

                # create recores
                if options.create:
                    p.createRecords(server, a.token, domain, dict_records)
                    exit

                # delete recores
                if options.delete:
                    p.deleteRecords(server, a.token, dict_records)
                    exit

            except UnboundLocalError as e:
                sys.stderr.write("ERROR: %s\n" % e)
                return

if __name__ == "__main__":
    main()
