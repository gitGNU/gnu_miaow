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

"""
Localization Data 

This module contains and manages the localization data. The data is organized 
in a tree structure:
    
            +----------+
            | document |
            +----------+
                  |
     -------------------------
     |            |          |
  +-----+      +-----+     +-----+
  |file |      |file |     |file |
  +-----+      +-----+     +-----+
                  \
          ---------------- 
          |               |
      +------+       +------+
      | head |       | body |  
      +------+       +------+
                         |
        ---------------------------------
        |                |              |
   +-----------+   +-----------+  +-----------+
   | transunit |   | transunit |  | transunit |
   +-----------+   +-----------+  +-----------+
                         |
          --------------------------------
          |            |                 |              
      +--------+  +--------+       +-----------+  
      | source |  | target |       | alt-trans |  
      +--------+  +--------+       +-----------+ 
          |                              |
      -------------               -----------------
      |           |               |               |
+---------+  +---------+   +-------------+ +--------------+
| segment |  | segment |   | alternative | | alternatives |
+---------+  +---------+   +-------------+ +--------------+
                 |
     ---------------------------
     |            |            |
+--------+  +--------+  +-----------+ 
| source |  | target |  | alt-trans |
+--------+  +--------+  +-----------+
                           
"""

class Iterator(object):
    
    """
    Iterator Base class.

    Usage: 

    iter = Iterator(item_list)
    while iter.has_previous():
        item = iter.next()

    """
    
    def __init__(self, items):
        self.items = items
        self.position = 0
    
    def __str__(self):
        return '%s[%d]' % (self.items.name, self.position)

    def has_previous(self):
        """Return True if there are previous items in the iterator."""
        if self.position <= 0:
            return False
        else:
            return True
    
    def previous(self):
        """Return the previous item in the iterator."""
        item = self.items[self.position]
        self.position -= 1
        return item

    def has_next(self):
        """Return True if there are more items in the iterator after the
        current item."""
        if self.position >= len(self.items):
            return False
        else:
            return True

    def next(self):
        """Return the next item in the iterator."""
        item = self.items[self.position]
        self.position += 1
        return item

# [NOTE]
# Previous doesn't really work. FIX IT!
class CompositeIterator(Iterator):

    """
    Iterator to walk a data tree.

    Usage:

    iter = CompositeIterator(component)
    while iter.has_next():
        item = iter.next()

    component should have a create_iterator() method
    """

    def __init__(self, component):
        """Initialize stack with top level component."""
        self.stack = []
        self.stack.append(component.create_iterator())
        
    def previous(self):
        if self.has_previous():
            iterator = self.stack[-1]
            component = iterator.previous()
            if component.has_iterator():
                self.stack.append(component.create_iterator())
            return component
        else:
            return None

    def has_previous(self):
        if not self.stack:
            return False
        else:
            iterator = self.stack[-1]
            if not iterator.has_previous():
                self.stack.pop()
                return self.has_previous()
            else:
                return True

    def next(self):
        if self.has_next():
            iterator = self.stack[-1]
            component = iterator.next()
            if component.has_iterator():
                self.stack.append(component.create_iterator())
            return component
        else:
            return None

    def has_next(self):
        if not self.stack:
            return False
        else:
            iterator = self.stack[-1]
            if not iterator.has_next():
                self.stack.pop()
                return self.has_next()
            else:
                return True

class Component(list):
    
    def __init__(self, attributes={}, content=""):
        list.__init__(self)
        self.name = self.__class__.__name__
        self.attributes = attributes
        self.content = content
    
    def _reset_(self):
        n = len(self)
        for i in range(n):
            self.pop()

    def has_iterator(self):
        if not len(self):
            return False
        else:
            return True
            
    def create_iterator(self):
        return Iterator(self)
        
class Document(Component):
    
    def __init__(self, attributes={}, content=""):
        Component.__init__(self, attributes, content)
             
class File(Component):
        
    def __init__(self, attributes={}, content=""):
        Component.__init__(self, attributes, content)
        self.head = Head()
        self.body = Body()
        
    def has_iterator(self):
        return True
            
    def create_iterator(self):
        self._reset_()
        iter = [self.head, self.body]
        self.extend(iter)
        return Iterator(self)

class Head(Component):
    
    def __init__(self, attributes={}, content=""):
        Component.__init__(self, attributes, content)     

class Body(Component):
    
    def __init__(self, attributes={}, content=""):
        Component.__init__(self, attributes, content)     

class TransUnit(Component):
    
    def __init__(self, attributes={}, content=""):
        Component.__init__(self, attributes, content)
        self.source = Source()
        self.target = Target()
        self.alt_trans = AltTrans()
        self.state = ''
        
    def has_iterator(self):
        return True
    
    def create_iterator(self):
        self._reset_()
        iter = [self.source, self.target, self.alt_trans]
        self.extend(iter)
        return Iterator(self)

class Source(Component):
    
    def __init__(self, attributes={}, content=""):
        Component.__init__(self, attributes, content)     

class Target(Component):
    
    def __init__(self, attributes={}, content=""):
        Component.__init__(self, attributes, content)
        
    def append(self, element): pass
        
class AltTrans(Component):
    
    def __init__(self, attributes={}, content=""):
        Component.__init__(self, attributes, content)
        
class Alternative(TransUnit):
    
    def __init__(self, attributes={}, content=""):
        TransUnit.__init__(self, attributes, content)
    
    def create_iterator(self):
        self._reset_()
        iter = [self.source, self.target]
        self.extend(iter)
        return Iterator(self)

class Segment(TransUnit):
    
    def __init__(self, attributes={}, content=""):
        TransUnit.__init__(self, attributes, content)

if __name__ == '__main__':
    document = Document()
    file_1 = File()
    head = Head()
    body = Body()
    tu = TransUnit()
    tu2 = TransUnit()
    body.append(tu)
    body.append(tu2)
    s = Source(content="Hello world")
    at = AltTrans()
    at.source = Source(content="Hello")
    at.target = Target(content="Hola")
    tu.source = s 
    tu.append(at)
    file_1.head = head
    file_1.body = body
    file_2 = File()
    head_2 = Head()
    body_2 = Body()
    tu3 = TransUnit()
    body_2.append(tu3)
    file_2.body = body_2
    file_2.head = head_2
    document.append(file_1)
    document.append(file_2)
    iter = CompositeIterator(document)
    while iter.has_next():
        composite = iter.next()
        print composite.name
    print iter.has_previous()
    while iter.has_previous():
        composite = iter.previous()
        print composite.name
    print len(iter.stack)
