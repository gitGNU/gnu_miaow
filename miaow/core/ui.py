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

"""
This module loads the editor's main window, connect to callbacks, etc.
"""

try:
    import pygtk
    pygtk.require('2.0')
except:
    pass
try:
    import gtk
    import gtk.glade
    import pango
except:
    print "GTK is not installed"
    sys.exit(1)
    
import os.path
from miaow.core.l10ndata import L10nDocument

class MiaowModel(L10nDocument):
    
    observers = []
    
    def __init__(self):
        L10nDocument.__init__(self)
        self.file_cursor = 0
        self.transunit_cursor = 0
        self.modified = False
        self.current_document = None
        self.transunit = None
        
    def _size_(self, array):
        return len(array) - 1
    
    def _set_transunit_(self):
        self.transunit = self[self.file_cursor][self.transunit_cursor]
        self.notify()
        
    def read(self, file_path):
        L10nDocument.read(self, file_path)
        self.current_document = file_path
        self._set_transunit_() 
    
    def write(self, file_path, file_format=None):
        L10nDocument.write(self, file_path, file_format)
        # There are no modification as the document has been just saved.
        self.modified = False
        # But if document's path is different to the current path, 
        # update data and notify observers 
        if file_path != self.current_document:
            self.current_document = file_path
            self.notify()
    
    def update(self):
        """Update the current translation unit."""
        self[self.file_cursor][self.transunit_cursor] = self.transunit      
            
    def previous(self):
        if self.cursor > 0:
            self.cursor -= 1
            self._set_transunit_()
            return True
        else:
            if self.file_cursor > 0:
                self.file_cursor -= 1
                self.cursor = self._size_(self[self.L_cursor])
                self._set_transunit_()
                return True
        return False
    
    def next(self):
        # get size of this list
        document_size = self._size_(self)
        # get size of the inner list
        file_size = self._size_(self[self.file_cursor])
        # if the cursor is smaller than the list's size
        # increment inner cursor and return 
        if self.cursor < file_size:
            self.cursor += 1
            self._set_transunit_()
            return True
        else:
            # If we are here is because we are already in the last element of
            # the inner list. We try to go to the next list
            # if the cursor is smaller than the list's size
            # increment cursor, and reset inner cursor to the first element of
            # the new list.
            if self.file_cursor < document_size:
                self.file_cursor += 1
                self.cursor = 0
                self._set_transunit_()
                return True
            # If we are still here, it is because we are in the last element of
            # the last list.
        return False

    # Observer Pattern:    
    def register(self, observer):
        self.observers.append(observer)

    def remove(self, observer):
        self.observers.delete(observer)

    def notify(self):
        for observer in self.observers:
            observer.update()

class MiaowView:

    def __init__(self, controller, model, glade_file):
        self.controller = controller
        self.model = model
        # Register the view as an observer
        self.model.register(self)
        # Create the main window and connect signals.
        self.window = gtk.glade.XML(glade_file, "miaow_editor")
        dic = {"on_miaow_editor_destroy": self.controller.quit,
               "on_open_activate": self.controller.open,
               "on_save_activate": self.controller.save,
               "on_save_as_activate": self.controller.save_as,
               "on_quit_activate": self.controller.quit,
               "on_cut_activate": self.controller._not_implemented_,
               "on_copy_activate": self.controller._not_implemented_,
               "on_paste_activate": self.controller._not_implemented_,
               "on_delete_activate": self.controller._not_implemented_,
               "on_up_activate": self.controller.previous_entry,
               "on_down_activate": self.controller.next_entry,
               "on_about_activate": self.controller.about,
               "on_open_button_clicked": self.controller.open,
               "on_save_button_clicked": self.controller.save,
               "on_save_as_button_clicked": self.controller.save_as,
               "on_quit_button_clicked": self.controller.quit,
               "on_up_button_clicked": self.controller.previous_entry,
               "on_down_button_clicked": self.controller.next_entry
              }
        self.window.signal_autoconnect(dic)

    def update(self):    
        transunit = self.model.transunit
        source_view = self.window.get_widget('source_view')
        source_buffer = source_view.get_buffer()
        source_start = source_buffer.get_start_iter()
        source_end = source_buffer.get_end_iter()
        # Clean previous entry
        source_buffer.delete(source_start, source_end)
        # Display new entry
        source_buffer.insert(source_end, transunit.source)
        # For target:
        target_view = self.window.get_widget('target_view')
        target_buffer = target_view.get_buffer()
        target_start = target_buffer.get_start_iter()
        target_end = target_buffer.get_end_iter()
        # Clean previous entry
        target_buffer.delete(target_start, target_end)
        # Display new entry if it exist.
        if transunit.target:
            target_buffer.insert(target_end, transunit.target)    

class MiaowController:
    
    def __init__(self, glade_file, file_path=None):
        """Load glade file, map signals with callbacks."""
        self.model = MiaowModel() 
        self.view = MiaowView(self, self.model, glade_file)        
        # Start data model
        if file_path:
            self._read_file_(file_path)          
        
    def _not_implemented_(self, obj):
        # [NOTE] This method should be part of the View!
        txt = "This feature has not been implemented yet"
        msg = gtk.MessageDialog(None, 0, gtk.MESSAGE_ERROR, gtk.BUTTONS_OK, txt)
        msg.run()  
        msg.destroy()
        
    def _not_saved_dialog_(self):
        txt = "The current file has not been saved.\rWould you like to save it?"
        msg_label = gtk.Label(txt)
        msg = gtk.Dialog("Save file?", None, gtk.DIALOG_MODAL,
                         (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, 
                          gtk.STOCK_OK, gtk.RESPONSE_OK))
        msg.resize(350, 250)
        msg.vbox.pack_start(msg_label)
        msg.show_all()
        result = msg.run()
        if result == gtk.RESPONSE_OK:
            self.save(self.window)
        msg.destroy()
        
    def _read_file_(self, file_path):
        """Load the file."""
        # check whether the file exist!
        assert os.path.isfile(file_path)
        # check if the current data has been save
        if self.model.modified:
            self._not_saved_dialog_()
        # Read new document
        self.model.read(file_path)
        
    def _update_model_(self):
        target_view = self.view.window.get_widget('target_view')
        target_buffer = target_view.get_buffer()
        target_start = target_buffer.get_start_iter()
        target_end = target_buffer.get_end_iter()
        target_text = target_buffer.get_text(target_start, target_end)
        self.model.transunit.target = target_text
        self.model.update()
             
    def quit(self, obj):
        """Destroy window an leave GTK loop."""
        if self.model.modified:
            self._not_saved_dialog_()
        window = obj.get_toplevel()
        window.destroy()
        gtk.main_quit()

    def open(self, obj): 
        chooser = gtk.FileChooserDialog('Open...', None, 
                                        gtk.FILE_CHOOSER_ACTION_OPEN,
                                        (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, 
                                         gtk.STOCK_OPEN, gtk.RESPONSE_OK))    
        ret = chooser.run()
        if ret == gtk.RESPONSE_OK:
            file_path = chooser.get_filename()
            # _read_file_() does all the work
            self._read_file_(file_path)
        chooser.destroy()

    def save(self, obj): 
        # [NOTE] Are we going to update the data every time the cursor moves?
        self._update_model_()
        self.model.write(self.model.current_document)

    def save_as(self, obj):
        """Save document using a different path and/or type."""
        #chooser = gtk.FileChooserDialog('Save as...', None, 
        #                                gtk.FILE_CHOOSER_ACTION_SAVE,
        #                                (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, 
        #                                 gtk.STOCK_OPEN, gtk.RESPONSE_OK))        
        # [TODO] Add filters.
        #ret = chooser.run()
        #if ret == gtk.RESPONSE_OK:
        #    file_path = chooser.get_filename()
        #    file_filter = chooser.get_filter()
        #    [TODO] Read mime-type of filter into file_path
        #    self.model.write(file_path, file_filter)
        #chooser.destroy() 
        self._not_implemented_(obj)

    def previous_entry(self, obj):
        # [NOTE] Are we going to update the data every time the cursor moves?
        self._update_model_() 
        self.model.previous()

    def next_entry(self, obj):
        # [NOTE] Are we going to update the data every time the cursor moves?
        self._update_model_() 
        self.model.next()

    def about(self, obj): 
        """Show minimal information about this application."""
        # [NOTE] about() should be on the view!
        # This should be also in the view as it doesn't interact with the model.
        txt = "miaow is a CAT (Computer Assisted Translation) suite"
        msg = gtk.MessageDialog(None, 0, gtk.MESSAGE_INFO, gtk.BUTTONS_OK, txt)
        msg.run()  
        msg.destroy()
        
if __name__ == "__main__":
    glade_file = "/home/mospina/programacion/miaow-git/data/miaow-editor.glade"
    MiaowController(glade_file)
    gtk.main()
