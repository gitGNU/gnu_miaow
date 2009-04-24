### Copyright (C) 2006-2009 Manuel Ospina <mospina@redhat.com>

# This file is part of miaowandpurr.
#
# miaowandpurr is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# miaowandpurr is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with miaowandpurr; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import polib

from miaowandpurr.kitten.l10n.handler import HandlerBase
from miaowandpurr.catus.map import File, TransUnit
   
class PoHandler(HandlerBase):
    
    file_format = '.po'
    entry_states = ['translated', 'fuzzy', 'untranslated']

    def read(self, filename, document):
        """Read file_path to self.data."""
        po = polib.pofile(filename)
        miaow_file = File()
        miaow_file.head.attributes = po.metadata
        for entry in po:
            tu = TransUnit()
            tu.source.content = entry.msgid
            tu.target.content = entry.msgstr
            if tu.target.content:
                tu.state = 'translated'
            else:
                tu.state = 'untranslated'        
            if 'fuzzy' in entry.flags:
                tu.state = 'fuzzy'
            miaow_file.body.append(tu)
        document.append(miaow_file)
        return document

    def write(self, filename, document):
        """Write self.data to file_path as Po."""
        po = polib.POFile()
        miaow_file = document[0]
        po.metadata = miaow_file.head.attributes
        for unit in miaow_file.body:
            entry = polib.POEntry(msgid=unit.source.content,
                                  msgstr=unit.target.content)
            po.append(entry)
        po.save_as_pofile(filename)

if __name__ == '__main__':
    from miaowandpurr.catus.map import Document, CompositeIterator
    map_h = PoHandler()
    d = map_h.read('/home/mospina/Documents/RedHat/Red_Hat_Enterprise_Linux/5.2/Global_File_System_2/es-ES/Getting_Started.po',
    Document()) 
    iter = CompositeIterator(d)
    while iter.has_next():
        composite = iter.next()
        if composite.name == 'Source':
            print composite.content
        print composite.name
