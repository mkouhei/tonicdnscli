# -*- coding: utf-8 -*-
"""
variable for tests
"""
from datetime import date


datajson = (
    '{"name": "example.org", "type": "MASTER",'
    '"notified_serial": "2012042701", '
    '"records": [{"name": "example.org", "type": "SOA", "content": '
    '"ns.example.org hostmaster.example.org 2012020501 '
    '3600 900 86400 3600", "ttl": "86400", "priority": null, '
    '"change_date": "1328449038"},'
    '{"name": "example.org", "type": "NS", '
    '"content": "ns.example.org", "ttl": "86400", "priority": null, '
    '"change_date":"1328449038"}]}')

datadict = {"name": "example.org", "type": "MASTER",
            "notified_serial": "2012042701",
            "records": [
            {"name": "example.org", "type": "SOA",
             "content": "ns.example.org hostmaster.example.org "
             "2012020501 3600 900 86400 3600",
             "ttl": "86400", "priority": False,
             "change_date": "1328449038"},
            {"name": "example.org", "type": "NS",
             "content": "ns.example.org",
             "ttl": "86400", "priority": False,
             "change_date": "1328449038"}]}

uri = 'https://ns.example.org'
token = 'efb9fc406a15bf9bdc60f52b36c14bcc6a1fd041'

str_l = ['test0.example.org A 10.10.10.10 86400\n'
         'test1.example.org A 10.10.10.11 86400\n'
         'test2.example.org A 10.10.10.12 86400\n',
         'example.org MX mx.example.org 86400 0\n'
         'example.org MX mx2.example.org 86400 10\n'
         'mx.example.org A 10.10.11.10 3600\n',
         'mx2.example.org A\t\t10.10.11.10 3600\n']

str1 = (str_l[0] + str_l[1] + str_l[2])

str2 = ('# name type content ttl priority\n' + str1)

list3 = [{'name': 'test0.example.org', 'type': 'A',
          'content': '10.10.10.10', 'ttl': 86400}]

list4 = [{'name': 'example.org', 'type': 'MX',
          'content': 'mx.example.org', 'ttl': 86400, 'priority': 0}]

dicts1 = [{'content': '10.10.10.10', 'name': 'test0.example.org',
           'ttl': 86400, 'type': 'A'},
          {'content': '10.10.10.11', 'name': 'test1.example.org',
           'ttl': 86400, 'type': 'A'},
          {'content': '10.10.10.12', 'name': 'test2.example.org',
           'ttl': 86400, 'type': 'A'},
          {'content': 'mx.example.org', 'name': 'example.org',
           'priority': 0, 'ttl': 86400, 'type': 'MX'},
          {'content': 'mx2.example.org', 'name': 'example.org',
           'priority': 10, 'ttl': 86400, 'type': 'MX'},
          {'content': '10.10.11.10', 'name': 'mx.example.org',
           'ttl': 3600, 'type': 'A'},
          {'content': '10.10.11.10', 'name': 'mx2.example.org',
           'ttl': 3600, 'type': 'A'}]

line1 = "test0.example.org A 10.10.10.10 86400"
line2 = "example.org MX mx.example.org 86400 0"
line3 = "mx2.example.org A\t\t10.10.11.10 3600"

older_cur_soa = {
    'name': 'example.org',
    'type': 'SOA',
    'content': 'ns.example.org postmaster.example.org 2012040501',
    'ttl': 86400,
    'priority': None}

today = date.strftime(date.today(), '%Y%m%d')

today_cur_soa = {
    'name': 'example.org',
    'type': 'SOA',
    'content': 'ns.example.org postmaster.example.org ' + today + '01',
    'ttl': 86400,
    'priority': None}

new_soa = {
    'name': 'example.org',
    'type': 'SOA',
    'content': 'ns.example.org postmaster.example.org '
    + today + '01 3600 900 86400 3600',
    'ttl': 86400,
    'priority': None}

content = {
    'domain': 'example.org',
    'mname': 'ns.example.org',
    'rname': 'postmaster.example.org',
    'refresh': 3600,
    'retry': 900,
    'expire': 86400,
    'minimum': 3600}
