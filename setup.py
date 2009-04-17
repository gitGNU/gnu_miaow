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

from distutils.core import setup

setup (
    name = 'miaowandpurr',
    version = '0.1',
    description = 'miaowandpurr is CAT (Computer Assited Translation) tool.',
    author = 'Manuel Ospina',
    author_email = 'mospina@redhat.com',
    packages = ['miaowandpurr', 
                'miaowandpurr.vcs', 'miaowandpurr.vcs.vcshandlers'],
                'miaowandpurr.kitten', 'miaowandpurr.kitten.l10nkithandlers'],
    data_files = [('share/miaowandpurr/',['README'])],
    )
    
