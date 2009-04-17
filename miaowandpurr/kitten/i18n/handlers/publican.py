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

import sys
import os.path
import re
import popen2

from miaowandpurr.kitten.i18n.handler import HandlerBase
from miaowandpurr.catus.models import Kit

def parse(filename):
    dic = {}
    var = re.compile(r'\$\((?P<variable>[\w\d\_\-]+)\)')
    fh = open(filename)
    lines = fh.readlines()
    fh.close()

    for line in lines:
        if line.startswith('#') or line == '\n':
            continue
        try:
            name, value = line.split('=')
        except:
            continue
        else:
            name = name.strip()
            value = value.strip()
            result = var.findall(value)
            for v in result:
                value = value.replace('$(%s)' % v, dic[v])
        dic[name] = value
    return dic

class PublicanHandler(HandlerBase):

    name = 'publican'
    # [NOTE]
    # Deprecated
    formats = ['html', 'pdf', 'html-single']
    # [END NOTE]
    
    def __init__(self, path):
        HandlerBase.__init__(self, path)
        self.languages = self._get_languages_()
    
    def extract(self): 
        # Create POT files
        cmd = 'make update-pot'
        self._execute_(cmd)
        
    def merge(self):
        raise NotImplementedError
    
    def update_po_all(self):
        cmd = 'make update-po-all'
        self._execute_(cmd)

    def get_kit(self, language, update=False):
        if update:
            cmd = 'make update-po-' + language
            self._execute_(cmd)
        result = L10nKit(language, 'po')
        path = os.path.join(self.path, language)
        files = os.listdir(path)
        for i in files:
            if i.endswith('.po'):
                result.append(i)
        return result
    
    # [DEPRECATED]
    #def build(self): 
    #    self.languages = self._get_languages_()
    #    result = interactive_dialog(self.formats, self.languages)
    #    if result:
    #        self._execute_(result[0], result[1])
    #
            
    def _get_languages_(self):
        makefile = os.path.join(self.path, 'Makefile')
        assert os.path.isfile(makefile)
        dic = parse(makefile)
        languages = dic['OTHER_LANGS']
        return languages.split()
    
    def _execute_(self, cmd): 
        os.chdir(self.path)
        # cmd = 'make %s-%s' % (format, language)
        i, o ,e = os.popen3(cmd)
        # [TODO]
        # Log results!
        errors = e.readlines()
        outputs = o.readlines()
        # 
        i.close()
        o.close()
        e.close()
             
if __name__ == '__main__':
    test_dir = '/NotBackedUp/mospina/svn/Red_Hat_Enterprise_Linux/5.3/Global_Network_Block_Device/'
    publican = PublicanHandler(test_dir)
    publican.build()
