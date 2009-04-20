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
               "on_cut_activate": self._not_implemented_,
               "on_copy_activate": self._not_implemented_,
               "on_paste_activate": self._not_implemented_,
               "on_delete_activate": self._not_implemented_,
               "on_previous_activate": self.controller.previous,
               "on_next_activate": self.controller.next,
               "on_about_activate": self.controller.about,
               "on_open_button_clicked": self.controller.open,
               "on_save_button_clicked": self.controller.save,
               "on_save_as_button_clicked": self.controller.save_as,
               "on_quit_button_clicked": self.controller.quit,
               "on_previous_button_clicked": self.controller.previous,
               "on_next_button_clicked": self.controller.next
              }
        self.window.signal_autoconnect(dic)

    def _not_implemented_(self, obj):
        error_dialog("This feature has not been implemented yet") 
        
    def set_states(self):
        store = gtk.ListStore(str)
        store.append(['All states'])
        for handler in self.model.get_states():
            store.append([handler])
        states = self.window.get_widget("states_boxentry")
        states.set_model(store)
        states.set_text_column(0)
        states.set_active(0)

    def get_state(self):
        states = self.window.get_widget("states_boxentry")
        model = states.get_model()
        index = states.get_active()
        state = model[index][0]
        if state == 'All states':
            return self.model.get_states()
        else:
            return [state]
    
    def update(self): 
        transunit = self.model.data[self.model.cursor]
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
        
if __name__ == "__main__": pass
