### Copyright (C) 2006-2007 Manuel Ospina <mospina@redhat.com>

# This file is part of miaow.
#
# miaow is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# miaow is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with miaow; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

"""
Localization Data 

This module contains and manages the localization data of one or more files.
These files can be separate documents or files contained in XLIFF document.
"""

from miaow.core.handler import HandlerStore

class TransUnit(object):
    
    """
    Container for a translation unit data.
    
    alt_trans is a list of AltTrans objects. 
    """
    
    def __init__(self, id=None, source=u"", target=u"", state="", alt_trans=None):
        self.id = id
        self.source = source
        self.target = target
        self.state = state
        self.alt_trans = alt_trans

class AltTrans(object):
    
    """Container for an alternative translation."""

    def __init__(self, source=u"", target=u"", quality=None):
        self.source = source
        self.target = target
        self.quality = quality

class L10nFile(list):

    """
    Container for the localization file data.
    
    A file is a list of trans_units.
    """
    
    def __init__(self, fpath="", original="", slang="", tlang="", dtype=""):
        list.__init__(self)
        self.filepath = fpath
        self.original = original
        self.source_language = slang
        self.target_language = tlang
        self.datatype = dtype

class L10nDocument(list):

    """Handle the localization data in general."""
    
    def __init__(self):
        list.__init__(self)
        self.handler = HandlerStore()
        
    def read(self, file_path):
        file_format = self.handler.get_type(file_path)
        handler = self.handler.handler(file_format)
        handler.read(file_path)

    def write(self, file_path, file_format=None):
        if not file_format:
            file_format = self.handler.get_type(file_path)
        handler = self.handler.handler(file_format)
        handler.read(file_path)

if __name__ == '__main__': pass
