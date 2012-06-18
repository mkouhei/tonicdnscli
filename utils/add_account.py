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

import MySQLdb as mdb
from datetime import date as d
import argparse
from getpass import getpass


prs = argparse.ArgumentParser(description='usage')
prs.add_argument('-u', dest='user', help='mysql dbuser', required=True)
prs.add_argument('-P', action='store_true',
                 help='mysql password  prompt', required=True)
prs.add_argument('-d', dest='db', help='mysql dbname', required=True)
prs.add_argument('-e', dest='email', help='request user email', required=True)
prs.add_argument('-H', dest='passmd5',
                 help='request user hashed password', required=True)
args = prs.parse_args()
passwd = ''

if args.__dict__.get('P'):
    while True:
        if passwd:
            break
        else:
            passwd = getpass(prompt='MySQL user passowrd: ')

user = args.__dict__.get('user')
db = args.__dict__.get('db')
email = args.__dict__.get('email')
passmd5 = args.__dict__.get('passmd5')
username = email.split('@')[0]
fullname = username.split('_')[0].title() +\
    ' ' + username.split('_')[1].title()
comment = 'add ' + d.today().isoformat()

con = mdb.connect('localhost', user, passwd, db)

with con:
    cur = con.cursor()
    cur.execute("SELECT * from users WHERE username = %s", username)
    if cur.rowcount:
        print('Already that useraccount exists')
    else:
        cur.execute(
            "INSERT INTO users VALUES (NULL, %s, %s, %s, %s, %s, 0, 0)",
                    (username, passmd5, fullname, email, comment))
