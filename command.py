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
    parser.add_option("-d", "--delete", action="store_true",
                      help="delete records")
    options, args = parser.parse_args()

    if len(args) == 0:
        parser.print_help()
        sys.exit(0)

    return options, args


def main():
    import os.path, sys
    import converter
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
        d = os.path.basename(filename).split('.txt')[0]
        f = open(filename, 'r')

    o = converter.JSONConvert(d)
    o.readRecords(f)
    o.serializeJSON(act)
    print o.build_records
    
if __name__ == "__main__":
    main()
