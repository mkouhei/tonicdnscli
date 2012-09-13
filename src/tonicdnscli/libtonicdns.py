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
import os.path
import connect
import processing
if sys.version_info > (2, 6) and sys.version_info < (2, 8):
    import ConfigParser as configparser
elif sys.version_info > (3, 0):
    import configparser as configparser


CONFIG_FILE = os.path.expanduser('~/.tdclirc')


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
        domain = conf.get('global', 'domain')
    except configparser.NoSectionError:
        domain = False
    except configparser.NoOptionError:
        domain = False

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

    return server, username, password, domain


def get_content_name_dict():
    """Retrieve content vs. name dictionary."""
    server, username, password, domain = check_config(CONFIG_FILE)
    token = connect.get_token(username, password, server)

    # When specified zone
    zone_data = processing.get_zone(server, token, domain,
                               keyword='', raw_flag=True)

    records = zone_data.get('records')
    addr_name_dict = dict((record.get('content'), record.get('name'))
                          for record in records)
    return content_name_dict
