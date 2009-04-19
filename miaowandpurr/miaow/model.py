### Copyright (C) 2006-2008 Manuel Ospina <mospina@redhat.com>

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

import os.path
from miaowandpurr.catus.data import Document
from miaowandpurr.catus.datastore import DataStore 

# [NOTE]
# MiaowModel doesn't need to inherit Document.
class MiaowModel(Document):
    
    observers = []
    
    def __init__(self):
        Document.__init__(self)
        self.filename = ''
        self.data_store = DataStore() 
        self.data_handler = None
        
    def open(self, filename):
        self.filename = filename
        file_format = os.path.splitext(self.filename)[1]
        self.data_handler = self.data_store.handler(file_format, self) 
        self.notify_states_change()
        # FIX ME
        # Go to the first translation unit (here or in the controller?)
        
    # Observer Pattern:    
    def register(self, observer):
        self.observers.append(observer)

    def remove(self, observer):
        self.observers.delete(observer)

    def notify(self):
        for observer in self.observers:
            if hasattr(observer, "update"):
                observer.update()
                
    def notify_states_change(self):
        for observer in self.observers:
            if hasattr(observer, "set_states"):
                observer.set_states()
                
if __name__ == "__main__": pass
