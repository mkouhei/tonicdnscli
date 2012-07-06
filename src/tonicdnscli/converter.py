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


class JSONConvert(object):
    # This magic number is work around.
    # Body size limitation with PUT method,
    # The boudnary of body size in over 27915 byte and under 27938 byte.
    maxdata = 100

    def __init__(self, domain):
        self.domain = domain
        self.split_index = 0
        self.records = []
        self.separated_list = []
        self.delta = False
        self.dict_records = []
        self.zone = ''
        self.refresh = '3600'
        self.retry = '900'
        self.expire = '86400'
        self.ttl = 3600

    def setRecord(self, name, rtype, content, ttl=3600, priority=False):
        line = name + ' ' + rtype + ' ' + content + ' ' + str(ttl)
        if priority:
            line += ' ' + str(priority)
        record = [line]
        return record

    def readRecords(self, listitems):
        import re
        for line in listitems:
            # Ignore number(#) at begining of a line.
            # and ignore blank lines.
            if not re.search('^#|^$', line):
                self.generateRecords(line)

    def generateRecords(self, line):
        d = {
            "name": self.checkkey(line, 0),
            "type": self.checkkey(line, 1),
            "content": self.checkkey(line, 2),
            "ttl": int(self.checkkey(line, 3))
            }
        if self.checkkey(line, 4):
            d.update(
                {"priority": int(self.checkkey(line, 4))}
                )
        self.records.append(d)

    def generateTemplate(self, domain, ipaddr, desc):
        from datetime import date
        serial = date.strftime(date.today(), '%Y%m%d') + '01'
        ns = 'ns.' + domain
        soa = (ns + ' hostmaster.' + domain +
            ' ' + serial + ' ' + self.refresh + ' ' + self.retry +
            ' ' + self.expire + ' ' + str(self.ttl))
        self.record = {
                'identifier': domain.replace('.', '_'),
                'description': desc,
                'entries': [
                self.record(domain, 'SOA', soa),
                self.record(domain, 'NS', ns),
                self.record(ns, 'A', ipaddr)
                ]}

    def record(self, name, rtype, content):
        record_d = {
            'name': name,
            'type': rtype,
            'content': content,
            'ttl': self.ttl
            }
        return record_d

    def generateZone(self, domain, template, dtype, master=None):
        # If there is a SOA record in records,
        # add self SOA records.
        self.zone = {
            "name": domain,
            "type": dtype,
            "master": master,
            "templates": [
                {"identifier": template}
                ]
            }

    def checkkey(self, key, index):
        import re
        length = len(re.split('\s*', key))
        if length > index:
            v = re.split('\s*', key)[index]
        else:
            v = None
        return v

    def genData(self, act):
        data = lambda act: {"records": self.records} \
            if act else {"name": self.domain, "records": self.records}
        self.dict_records.append(data(act))
        self.records = []

    def separateInputFile(self, file):
        import re
        line_index = 1
        separated_str = ''
        if self.delta:
            # for test only
            delta = self.delta
        else:
            delta = self.maxdata

        for line in file:
            if not re.search('^#|^$', line):
                if line_index > delta:
                    line_index = 1
                    self.split_index += 1
                    self.separated_list.append(separated_str)
                    separated_str = ''
                line_index += 1
                separated_str += line
        self.separated_list.append(separated_str)

    def decodeJSON(self, data):
        import json
        json.load(data, 'utf-8')

    def getSOA(self, record, content):
        from datetime import date
        new_record = record.copy()

        if content.get('mname'):
            mname = content.get('mname')
        else:
            mname = record.get('content').split(' ')[0]

        if content.get('rname'):
            rname = content.get('rname')
        else:
            rname = record.get('content').split(' ')[1]

        if content.get('refresh'):
            self.refresh = str(content.get('refresh'))

        if content.get('retry'):
            self.retry = str(content.get('retry'))

        if content.get('expire'):
            self.expire = str(content.get('expire'))

        if content.get('minimum'):
            self.ttl = str(content.get('minimum'))

        today = date.strftime(date.today(), '%Y%m%d')
        cur_serial = record.get('content').split(' ')[2]
        if int(cur_serial[:-2]) < int(today):
            serial = today + '01'
        else:
            serial = str(int(cur_serial) + 1)

        new_record['content'] = (mname + ' ' + rname + ' ' +
            serial + ' ' + self.refresh + ' ' + self.retry + ' ' +
            self.expire + ' ' + str(self.ttl))
        return new_record
