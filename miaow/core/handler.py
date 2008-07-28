### Copyright (C) 2006-2008 Manuel Ospina <mospina@redhat.com>

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

class Handler:
    
    """Factory interface."""
    
    def __init__(self, data):
        self.data = data

    def read(self, file_path): pass

    def write(self, file_path): pass

from mimetypes import MimeTypes
from miaow.core.xlfhandler import XlfHandler
from miaow.core.pohandler import PoHandler
        
class HandlerStore: 

    """This class deliver the proper handler for the requested file format."""
    
    def __init__(self):
        self.mimetype = self._mimetypes_()

    def _mimetypes_(self):
        mimetype = MimeTypes()
        mimetype.add_type("xlf", ".xlf")
        mimetype.add_type("po", ".po")
        return mimetype

    def get_type(self, file_path):
        type = self.mimetype.guess_type(file_path)
        file_format = type[0]
        if file_format:
            return file_format
        else:
            raise NotImplementedError  

    def handler(self, handler_name):
        """Load the data handler."""
        handler = None
        if handler_name == "xlf":
            handler = XlfHandler(self)
        elif handler_name == "po":
            handler = PoHandler(self)
        else:
            raise NotImplementedError
        return handler

if __name__ == '__main__': pass