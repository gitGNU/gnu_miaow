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

from miaowandpurr.kitten.vcs.handler import VCSHandlerBase
from miaowandpurr.kitten.vcs.vcshandlers import *

class VCSStore(object):

    handlers = [handler.vcs for handler in VCSHandlerBase.plugins]

    def handler(self, name, url, path, branch=None):
        if not name in self.handlers:
            raise NotImplementedError
        for handler in VCSHandlerBase.plugins:
            if handler.vcs == name:
                return handler(url, path, branch)
            
if __name__ == '__main__':
    store = VCSStore()
    print store.handlers
    handler = store.handler('svn',
    'https://svn.devel.redhat.com/repos/ecs/l10n/L10n-Knowledgebase/Technical-Translator-Handbook',
    './TEST')
    print handler.vcs
    #handler.check_out()
    #handler.update()
    handler.commit('ignore')
