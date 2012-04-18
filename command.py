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
    from optparse import OptionParser
    usage = "usage: %prog [options] inputfile"
    parser = OptionParser(usage=usage)
    parser.add_option("-o", "--stdout", action="store_true", help="print json format to stdout")
    parser.add_option("-c", "--create", action="store_true", help="create records")
    parser.add_option("-d", "--delete", action="store_true", help="delete records")
    parser.add_option("-g", "--retrieve", action="store_true", help="retrieve records")
    parser.add_option("-s", dest='fqdn', help="specify TonicDNS server")
    parser.add_option("-u", dest='username', help="TonicDNS username")
    parser.add_option("-p", dest='password', help="TonicDNS password")
    options, args = parser.parse_args()

    if len(args) == 0:
        parser.print_help()
        sys.exit(0)

    return options, args


def main():
    import os.path, sys
    import converter, tdauth
    import processing as p

    try:
        options, args = parse_options()
    except RuntimeError, e:
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
    o.readRecords(f)
    o.genDict(act)
    if options.stdout:
        print o.dict_records
    else:
        dict_records = o.dict_records
        if options.fqdn:
            server = options.fqdn
        if options.username:
            username = options.username
        if options.password:
            password = options.password

        try:
            o = tdauth.authInfo(username, password, server)
            o.getToken()


            # Retrieve zone records
            if options.retrieve:
                p.getZone(server, o.token, domain)
                exit

            # Retrieve all zones
            #p.getAllZone(server, o.token)

            # create recores
            if options.create:
                p.createRecords(server, o.token, domain, dict_records)
                exit

            # delete recores
            if options.delete:
                p.deleteRecords(server, o.token, dict_records)
                exit

        except UnboundLocalError, e:
            sys.stderr.write("ERROR: %s\n" % e)
            return

if __name__ == "__main__":
    main()
