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
# * The target content is not showing.!
# * Fix previous() and next() to avoid the methods to return a None object
# * (OPTIONAL) The MiaowModel could have an attribute page that store the data
#   for each document that is loaded (when miaow implement a nootbook widget).
# Go to the first translation unit (here or in the controller?)

class MiaowModel:
    
    observers = []
    
    def __init__(self):
        self.filename = ''
        self.l10n_store = L10NStore() 
        self.document = Document()
        self.iter = None
        self.current = None
        
    def open(self, filename):
        self.filename = filename
        self.document = self.l10n_store.read(filename, self.document) 
        self.iter = CompositeIterator(self.document)
        self.notify_states_change()

    def save(self, filename):
        pass
    
    def get_states(self):
        return self.l10n_store.get_states(self.filename)

    def previous(self):
        print self.current.source.content
        while self.iter.has_previous():
            composite = self.iter.previous()
            if composite.name == 'TransUnit':
                if composite.segmented:
                    continue
                else:
                    break
            if composite.name == 'Segment':
                break
        if composite.name not in ['TransUnit', 'Segment']:
            self.next()
            return
        self.current = composite
        self.notify()

    def next(self):
        composite = None
        while self.iter.has_next():
            composite = self.iter.next()
            if composite.name == 'TransUnit':
                if composite.segmented:
                    continue
                else:
                    break
            if composite.name == 'Segment':
                break
        self.current = composite
        self.notify()

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
