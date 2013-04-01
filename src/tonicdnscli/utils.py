# -*- coding: utf-8 -*-
"""
    Copyright (C) 2012, 2013 Kouhei Maeda <mkouhei@palmtb.net>

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
from datetime import datetime


def print_inline(arg):
    sys.stdout.write("%s" % arg)


def error(msg):
    print("ERROR: %s" % msg)
    exit(1)


def get_columns_width(rows, columns_width, domain=False):
    soa = None
    for row in rows:
        if row.get('type') == 'SOA':
            soa = row
        else:
            if 'change_date' in row:
                row['change_date'] = datetime.fromtimestamp(
                    int(row.get('change_date'))).strftime("%Y%m%d-%H%M%S")
            else:
                if domain:
                    row['change_date'] = None

            # row is content, priority, type, name, ttl
            for i, value in enumerate(row.values()):
                if value is None:
                    value = '-'
                if columns_width[i] <= len(value):
                    columns_width[i] = len(value)
                else:
                    columns_width[i] = columns_width[i]

    return columns_width, soa


def generate_row_s(row, columns_width, domain):
    row_s = ''

    # for domains
    row_l = [i for i in row]
    row_l.reverse()

    for i, column in enumerate(row_l):
        if i == 0:
            row_s += ('| ' + column + ' ' *
                      (columns_width[i] - len(column) - domain + 1))
        else:
            row_s += ('| ' + column + ' ' *
                      (columns_width[i] - len(column) + 1))
    row_s += '|'
    return row_s


def get_row_s(row_d, key, col_width, domain=None):
    if row_d.get(key):
        value = row_d.get(key)
        hostname = lambda domain: value.split(domain)[0]

        def compare(value, domain):
            if value == domain:
                #return value
                return ""
            else:
                return hostname(domain)
        name_ = compare(value, domain)

        if domain:
            return (" " + name_ + " " *
                    (col_width - len(name_) - len(domain) + 1))
        else:
            return (" " + name_ + " " *
                    (col_width - len(name_) + 1))


def print_header(cols_width, col_header_l, domain=0):
    border = '+'
    for i, col_width in enumerate(cols_width):
        if i == 0:
            border += "-" * (col_width - domain + 1) + '-+'
        else:
            border += "-" * (col_width + 1) + '-+'

    sys.stdout.write("%s\n" % border)
    print(generate_row_s(col_header_l, cols_width, domain))
    sys.stdout.write("%s\n" % border)


def print_bottom(cols_width, domain=0):
    border = '+'
    for i, col_width in enumerate(cols_width):
        if i == 0:
            border += "-" * (col_width - domain + 1) + '-+'
        else:
            border += "-" * (col_width + 1) + '-+'
    sys.stdout.write("%s\n" % border)


def pretty_print(rows, keyword, domain):
    """
    rows is
    list when get domains
    dict when get specific domain
    """
    if isinstance(rows, dict):
        pretty_print_domain(rows, keyword, domain)
    elif isinstance(rows, list):
        pretty_print_zones(rows)


def pretty_print_zones(rows):
    col_header_l = ['notified_serial', 'type', 'name']
    col_width_l = [len(i) for i in col_header_l]
    col_width, dummy = get_columns_width(rows, col_width_l)

    col_width.reverse()

    print_header(col_width, col_header_l)

    for row in rows:
        print generate_row_s(row.values(), col_width, 0)

    print_bottom(col_width)


def pretty_print_domain(rows, keyword, domain):
    """
    Arguments:

        rows:    get response data
        keyword: search keyword

    """
    if len(rows.get('records')) == 0:
        return None

    # six columns; priority, name, content, ttl, change_date, type
    header_l = ['prio', 'name', 'content',
                'ttl', 'change date', 'type']
    # 0->4, 1->0, 2->2, 3->3, 4->5, 5->1
    header_l_sorted = ['name', 'type', 'content',
                       'ttl', 'prio', 'change date']
    header_l_sorted.reverse()

    cols_width = [len(i) for i in header_l]

    """
    if key == 'change_date':
        value = datetime.fromtimestamp(
            int(row_d.get(key))).strftime("%Y%m%d-%H%M%S")
            """

    cw_, soa = get_columns_width(rows.get('records'),
                                 cols_width, True)

    # sorted as name, type, content, ttl, priority, change_date
    cols_width_sorted = [cw_[1], cw_[5], cw_[2],
                         cw_[3], cw_[0], cw_[4]]

    if isinstance(soa, dict):
        soa_s = ('zone:        ' + soa.get('name') + '\n' +
                 'SOA record:  ' + soa.get('content') + '\n' +
                 'ttl:         ' + soa.get('ttl') + '\n' +
                 'change date: ' + soa.get('change_date'))
        domain = soa.get('name')
        print(soa_s)

    print domain

    if keyword != 'SOA':
        print_header(cols_width_sorted, header_l_sorted, len(domain))
        str_value = ''
        for row in rows.get('records'):
            if row.get('type') == 'SOA':
                pass
            else:
                # name
                if row.get('name'):
                    str_value = get_row_s(row, 'name',
                                          cols_width_sorted[0],
                                          domain=domain)
                    sys.stdout.write("|%s" % str_value)
                # type
                if row.get('type'):
                    str_value = get_row_s(row, 'type',
                                          cols_width_sorted[1])
                    sys.stdout.write("|%s" % str_value)
                # content
                if row.get('content'):
                    str_value = get_row_s(row, 'content',
                                          cols_width_sorted[2])
                    sys.stdout.write("|%s" % str_value)
                # ttl
                if row.get('ttl'):
                    str_value = get_row_s(row, 'ttl',
                                          cols_width_sorted[3])
                    sys.stdout.write("|%s" % str_value)
                # priority
                if row.get('priority') is None:
                    val = {'priority': '-'}
                else:
                    val = row.copy()
                str_value = get_row_s(val, 'priority',
                                      cols_width_sorted[4])
                sys.stdout.write("|%s" % str_value)
                if row.get('change_date') is None:
                    val = {'change_date': '-'}
                else:
                    val = row.copy()
                str_value = get_row_s(val, 'change_date',
                                      cols_width_sorted[5])
                print("|%s|" % str_value)

        print_bottom(cols_width_sorted, len(domain))
