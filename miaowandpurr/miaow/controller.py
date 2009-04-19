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

from miaowandpurr.felis import widgets
from miaowandpurr.miaow import view, model

class MiaowController:

    def __init__(self, glade_file, file_path=None):
        """Load glade file, map signals with callbacks."""
        self.model = model.MiaowModel() 
        self.view = view.MiaowView(self, self.model, glade_file)
        if file_path:
            self.model.open(file_path)        

    def quit(self, obj):
        window = obj.get_toplevel()
        window.destroy()
        gtk.main_quit()

    def open(self, obj):
        filename = widgets.file_chooser('Open...', gtk.FILE_CHOOSER_ACTION_OPEN)
        self.model.open(filename)

    def save(self, obj):
        widgets.error_dialog("This feature has not been implemented yet") 

    def save_as(self, obj):
        widgets.error_dialog("This feature has not been implemented yet") 

    def previous(self, obj):
        widgets.error_dialog("This feature has not been implemented yet") 

    def next(self, obj):
        widgets.error_dialog("This feature has not been implemented yet") 

    def about(self, obj):
        txt = "miaowandpurr is a CAT (Computer Assisted Translation) suite"
        widgets.info_dialog(txt) 
            
if __name__ == "__main__":
    from miaowandpurr.glade import MIAOW_GLADE_FILE 
    # FIX ME!
    #file_path = "/NotBackedUp/mospina/svn/Red_Hat_Enterprise_Linux/5.2/Virtualization_Guide/es-ES/Preface.po"
    glade_file = MIAOW_GLADE_FILE
    MiaowController(glade_file) # file_path
    gtk.main()
