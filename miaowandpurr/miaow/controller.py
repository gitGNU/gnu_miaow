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
    
# [NOTE]
# I don't want to have the controller making any call to gtk methods so we can
# implement an ncurses view if necessary.
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
#.

from miaowandpurr.felis import widgets
from miaowandpurr.miaow import view, model

class MiaowController:

    def __init__(self, glade_file, file_path=None):
        """Load glade file, map signals with callbacks."""
        self.model = model.MiaowModel() 
        self.view = view.MiaowView(self, self.model, glade_file)
        if file_path:
            self.model.open(file_path)        

    def _update_model_(self):
        transunit = self.model.data[self.model.cursor]
        target_view = self.view.window.get_widget('target_view')
        target_buffer = target_view.get_buffer()
        # [TODO]
        # Check if the entry has been modified.
        #   modified = target_buffer.get_modified()
        # 1. We need to set set_modified(False) when the TextView go to the next
        # entry.
        # 2. As we are updating the model everytime we move up/down the entry
        # list, the exit() method always warn the user for a unsave file (even
        # when the file has been saved). Fix.
        #.
        target_start = target_buffer.get_start_iter()
        target_end = target_buffer.get_end_iter()
        target_text = target_buffer.get_text(target_start, target_end)
        transunit.target = target_text
        # [TODO]
        # There are no way to set the state of the entry.
        # transunit.state = ?
        #.
        self.model.update_entry(transunit)

    def quit(self, obj):
        # [TODO]
        # The main window is closing before the dialog. FIX IT
        if self.model.modified:
            txt = 'The current file has not been saved.\rWould you like to save it?'
            if widgets.request_dialog('Save File?', txt):
                self.save(obj)
        window = obj.get_toplevel()
        window.destroy()
        gtk.main_quit()
        # .

    def open(self, obj):
        filename = widgets.file_chooser('Open...', gtk.FILE_CHOOSER_ACTION_OPEN)
        self.model.open(filename)

    def save(self, obj):
        self._update_model_()
        self.model.save(self.model.filename)

    def save_as(self, obj):
        widgets.error_dialog("This feature has not been implemented yet") 

    def previous(self, obj):
        self._update_model_()
        state = self.view.get_state()
        self.model.previous(state)

    def next(self, obj):
        self._update_model_()
        state = self.view.get_state()
        self.model.next(state)

    def about(self, obj):
        txt = "miaowandpurr is a CAT (Computer Assisted Translation) suite"
        widgets.info_dialog(txt) 
            
if __name__ == "__main__":
    from miaowandpurr.miaow.glade import MIAOW_GLADE_FILE 
    # FIX ME!
    #file_path = "/NotBackedUp/mospina/svn/Red_Hat_Enterprise_Linux/5.2/Virtualization_Guide/es-ES/Preface.po"
    glade_file = MIAOW_GLADE_FILE
    MiaowController(glade_file) # file_path
    gtk.main()
