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
from miaowandpurr.catus.map import Document, CompositeIterator
from miaowandpurr.kitten.l10n.store import L10NStore 

# [TO DO]
# * The l10n_handler.write should return True on success
#       def write(filename, document)
#           ....
#           return True
# * (OPTIONAL) The MiaowModel could have an attribute page that store the data
#   for each document that is loaded (when miaow implement a nootbook widget).

(
    TRANSUNIT,
    SOURCE,
    TARGET,
    STATE
) = range(4)

class Data:

    def __init__(self, node, source, target, state):
        self.node = node
        self.source = source
        self.target = target
        self.state = state

class MiaowModel:
    
    observers = []
    
    def __init__(self):
        self.filename = ''
        self.l10n_store = L10NStore() 
        self.document = Document()
        self.data = []
        self.cursor = 0
    
    def _load_data_(self, iter):
        while iter.has_next():
            composite = iter.next()
            if composite.name == 'TransUnit':
                tu = Data(composite, 
                          composite.source.content, 
                          composite.target.content,
                          composite.state)
                self.data.append(tu)
 
    def open(self, filename):
        self.filename = filename
        self.document = self.l10n_store.read(filename, self.document) 
        iter = CompositeIterator(self.document)
        self._load_data_(iter)
        self.notify_states_change()
        self.notify()

    def save(self, filename):
        pass
    
    def get_states(self):
        return self.l10n_store.get_states(self.filename)

    def previous(self, state): 
        cursor = self.cursor
        while cursor > 0:
            cursor -= 1
            if self.data[cursor].state in state:
                self.cursor = cursor
                self.notify()
                return

    def next(self, state):
        cursor = self.cursor
        while cursor < (len(self.data) - 1):
            cursor += 1
            if self.data[cursor].state in state:
                self.cursor = cursor
                self.notify()
                return

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
