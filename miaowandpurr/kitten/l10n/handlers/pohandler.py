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

from miaowandpurr.catus.handler import HandlerBase
from miaowandpurr.catus.data import File, TransUnit
   
class PoHandler(HandlerBase):
    
    file_format = '.po'
    entry_states = ['translated', 'fuzzy', 'untranslated']

    def read(self, file_path):
        """Read file_path to self.data."""
        po = polib.pofile(file_path)
        miaow_file = File()
        miaow_file.head.attributes = po.metadata
        for entry in po:
            tu = TransUnit()
            tu.source.content = entry.msgid
            tu.target.content = entry.msgstr
            miaow_file.body.append(tu)
        self.data.append(miaow_file)

    def write(self, file_path):
        """Write self.data to file_path as Po."""
        po = polib.POFile()
        miaow_file = self.data[0]
        po.metadata = miaow_file.head.attributes
        for unit in miaow_file.body:
            entry = polib.POEntry(msgid=unit.source.content,
                                  msgstr=unit.target.content)
        po.append(entry)
        po.save_as_pofile(filename)
