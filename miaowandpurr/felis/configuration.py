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

import os

"""
USAGE:

from configuration import options

value = options[key]
"""

RC_FILE = '/etc/miaowandpurr.cfg'
RC_LOCAL = os.path.join(os.environ.get('HOME'), '.miaowandpurr.cfg')
options = {}

def _read_configuration_(filename):
    """Read configuration file and set options."""
    fh = open(filename)
    for line in fh.readlines():
        if line in ("\n", ""):
            continue
        if line.startswith("#"):
            continue
        key, value = line.split("=")
        if value.strip():
            options[key.strip()] = value.strip()
    fh.close()

for RC in (RC_FILE, RC_LOCAL):
    if os.path.isfile(RC):
        _read_configuration_(RC)
