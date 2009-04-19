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
from miaowandpurr.catus.map import Document
from miaowandpurr.kitten.l10n.store import L10NStore 

# [TODO]
# * the l10n_handler should be only a filter
# * the l10n_handler.read should return a Document():
#       def read(filename, document=Document())
#           map = document
#           ....
#           return map
# * The l10n_handler.write should return True on success
#       def write(filename, document)
#           ....
#           return True
# * The MiaowModel should have the following attributes: 
#       * filename
#       * l10n_store
# * (OPTIONAL) The MiaowModel could have an attribute page that store the data
#   for each document that is loaded (when miaow implement a nootbook widget).
# Go to the first translation unit (here or in the controller?)

class MiaowModel:
    
    observers = []
    
    def __init__(self):
        self.filename = ''
        self.data_store = L10NStore() 
        self.data_handler = None
        
    def open(self, filename):
        self.filename = filename
        file_format = os.path.splitext(self.filename)[1]
        self.data_handler = self.data_store.handler(file_format, Document()) 

        self.notify_states_change()

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
