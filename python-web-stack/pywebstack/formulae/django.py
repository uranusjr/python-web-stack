#!/usr/bin/env python
# -*- coding: utf-8

import os
from ..utils import chdir
from . import Formula


class Django(Formula):
    """Django formula"""

    def get_wsgi_script(self):
        return os.path.join(self.project_root, self.project_name, 'wsgi.py')

    def install(self):
        self.pip('install', 'django')

    def create_project(self):
        with chdir(self.containing_dir):
            os.system('django-admin.py startproject {name}'.format(
                name=self.project_name
            ))

    def configure_server(self):
        pass

    def deconfigure_server(self):
        pass
