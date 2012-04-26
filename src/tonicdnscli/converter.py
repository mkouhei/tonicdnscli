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

    def readRecords(self, listitems):
        import re
        for line in listitems:
            # Ignore number(#) at begining of a line.
            if not re.search('^#', line):
                self.generateDict(line)

    def generateDict(self, line):
        if self.checkkey(line, 4):
            self.records.append({
                    "name": self.checkkey(line, 0),
                    "type": self.checkkey(line, 1),
                    "content": self.checkkey(line, 2),
                    "ttl": self.checkkey(line, 3),
                    "priority": self.checkkey(line, 4)
                    })
        else:
            self.records.append({
                    "name": self.checkkey(line, 0),
                    "type": self.checkkey(line, 1),
                    "content": self.checkkey(line, 2),
                    "ttl": self.checkkey(line, 3)
                    })

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
            if not re.search('^#', line):
                if line_index > delta:
                    line_index = 1
                    self.split_index += 1
                    self.separated_list.append(separated_str)
                    separated_str = ''
                line_index += 1
                separated_str += line
        self.separated_list.append(separated_str)
