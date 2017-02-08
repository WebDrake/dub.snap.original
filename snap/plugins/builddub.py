# -*- Mode:Python; indent-tabs-mode:nil; tab-width:4 -*-
#
# Copyright (c) 2016 Joseph Rushton Wakeling
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""This plugin is intended solely for the purposes of building DUB, and
is not for general purpose usage.  It simply invokes the build script
`build.sh`, using the specified D compiler.

There is one plugin-specific keyword:

    - d-compiler:
     (string)
     The D compiler to use: dmd, gdc, gdmd or ldmd2.
"""

import os
import shutil
import snapcraft

class BuildDubPlugin(snapcraft.BasePlugin):

    @classmethod
    def schema(cls):
        schema = super().schema()
        # the D compiler to use: dmd, gdc, gdmd
        # or ldmd2
        schema['properties']['d-compiler'] = {
            'type': 'string',
            'default': ''
        }
        return schema

    def __init__(self, name, options, project):
        super().__init__(name, options, project)

    def build(self):
        super().build()

        env=self._build_environment()

        build_script = './build.sh'

        if self.options.d_compiler == 'gdc':
            build_script = './build-gdc.sh'

        # Handle the build type and config, and run the
        # corresponding `dub` command
        self.run([build_script], env=env)

        # Copy `dub` executable into the install directory
        dub_install_path = os.path.join(self.installdir, 'bin')
        os.mkdir(dub_install_path)
        dub_path = os.path.join(self.partdir, 'build', 'bin', 'dub')
        shutil.copy2(os.path.join(self.partdir, 'build', 'bin', 'dub'),
                     dub_install_path)

    def _build_environment(self):
        env = os.environ.copy()
        env['DMD'] = self.options.d_compiler
        return env
