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

class JSONConvert:
    '''
    Read text file
    '''
    def readFile(self):
        import os.path, sys
        self.filename = sys.argv[1]

        if os.path.isfile(self.filename):
            self.domain = os.path.basename(self.filename).split('.txt')[0]
            self.f = open(self.filename, 'r')

    '''
    Read record
    '''
    def readRecords(self):
        import re
        self.records = []
        for line in self.f:
            # Ignore number(#) at begining of a line.
            if not re.search('^#', line):
                self.generateDict(line)

    '''
    Generate dictionary
    '''
    def generateDict(self,line):
        import re
        self.records.append({
            "name" : self.checkkey(line, 0),
            "type" : self.checkkey(line, 1),
            "content" : self.checkkey(line, 2),
            "ttl": self.checkkey(line, 3),
            "priority" : self.checkkey(line, 4)
            })

    '''
    Check input key
    '''
    def checkkey(self, key, index):
        import re
        length = len(re.split('\s*', key[:-1]))
        if length > index:
            v = re.split('\s*', key[:-1])[index]
        else:
            v = None
        return v
        
    '''
    Serialize JSON
    '''
    def serializeJSON(self):
        import json
        self.build_records = json.JSONEncoder().encode({
                "name": self.domain,
                "records": self.records
                })


''' Main '''
o = JSONConvert()
o.readFile()
o.readRecords()
o.serializeJSON()
print o.build_records
