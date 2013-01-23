# -*- coding: utf-8 -*-

"""
variable for tests
"""

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
             "change_date":"1328449038"}]}

uri = 'https://ns.example.org'
token = 'efb9fc406a15bf9bdc60f52b36c14bcc6a1fd041'
