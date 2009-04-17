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

import pysvn
import sys
   
from miaowandpurr.kitten.vcs.handler import VCSHandlerBase
   
class SVNHandler(VCSHandlerBase):
    
    vcs = "svn"
    
    def __init__(self, url, path, branch=None):
        """
        INPUT:
        * url - repository address
        * path - directory where the check-outs are done
        * branch - branch. SVN doesn't really have branches.
        """
        VCSHandlerBase.__init__(self, url, path, branch)
        self.client = pysvn.Client()
        self.client.callback_ssl_server_trust_prompt = self._ssl_server_trust_prompt_

    def _ssl_server_trust_prompt_(trust_dict):
        return False, 1, True
        
    def set_authentication(self, username, password):
        username = str(username)
        password = str(password)
        self.client.set_default_username(username)
        self.client.set_default_password(password)

    def check_out(self):
        self.client.checkout(self.url, self.path)

    def update(self):
        self.client.update(self.path)

    def commit(self, message):
        self.client.checkin([self.path], message) 
        
if __name__ == '__main__': pass
