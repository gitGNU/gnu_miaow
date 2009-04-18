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
    
import os.path

def dialog(message, txt):
    msg = gtk.MessageDialog(None, 0, message, gtk.BUTTONS_OK, txt)
    msg.run()  
    msg.destroy()

def error_dialog(txt):
    dialog(gtk.MESSAGE_ERROR, txt)
    
def info_dialog(txt): 
    dialog(gtk.MESSAGE_INFO, txt)
    
def file_chooser(txt, action):
    filename = ''
    chooser = gtk.FileChooserDialog(txt, None, action,
                                    (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, 
                                     gtk.STOCK_OPEN, gtk.RESPONSE_OK))
    ret = chooser.run()
    if ret == gtk.RESPONSE_OK:
        filename = chooser.get_filename()
    chooser.destroy()
    return filename

