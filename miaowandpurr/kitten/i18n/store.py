### Copyright (C) 2009 Manuel Ospina <mospina@redhat.com>

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

from miaowandpurr.kitten.i18n.handler import HandlerBase
from miaowandpurr.kitten.i18n.handlers import *

class I18NStore(object):

    handlers = [handler.name for handler in HandlerBase.plugins]

    def handler(self, name, path):

        if not name in self.handlers:
            raise NotImplementedError

        for handler in HandlerBase.plugins:
            if handler.name == name:
                return handler(path)
          
if __name__ == '__main__':
    store = I18NStore()
    print store.handlers
    handler = store.handler('publican', '.')
    print handler.name
