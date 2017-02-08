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

"""The DUB plugin can be used for D language projects that can be built
with the command `dub build`.

Since the DUB package/build manager does not currently have an `install`
option, some manual work may be necessary to ensure snapcraft correctly
packages the executables and libraries that have been built.  By default
the plugin will copy the contents of the entire project build directory,
including both built files and the source of the project being built;
these files can be filtered in the usual way using the `snap:` config
option in `snapcraft.yaml`.

If the DUB build target includes a `targetPath` in the DUB config file,
then this can be specified in `snapcraft.yaml` using the corresponding
`target-path` plugin config option.  In this case, the plugin will copy
only files placed in that directory.

The complete list of plugin-specific keywords is as follows:

    - build-flags:
      (array)
      List of flags to pass to the `dub build` command, such as
      `--build=release` or `--compiler=ldc2`.

    - build-target:
      (string)
      The specific target to build, of those defined in `dub.json`.
      Optional, since many projects do not define multiple targets.

    - target-path:
      (string)
      Directory (relative to the base directory of the project)
      where DUB is expected to write built files; corresponds to
      the `targetPath` variable in `dub.json`.  This can be used
      to filter the files that the plugin will attempt to install
      as part of the snap.  Optional, since many projects will
      not define any `targetPath`.
"""

import os
import shutil
import snapcraft

class DubPlugin(snapcraft.BasePlugin):

    @classmethod
    def schema(cls):
        schema = super().schema()
        # flags to pass to the `dub build` command
        # (e.g. --build=release, --compiler=ldc2)
        schema['properties']['build-flags'] = {
            'type': 'array',
            'minitems': 1,
            'uniqueItems': True,
            'items': {
                'type': 'string',
            },
            'default': [],
        }
        # the dub target to build (optional)
        schema['properties']['build-target'] = {
            'type': 'string',
            'default': ''
        }
        # the target path where dub will place files
        # that have been built, relative to the root
        # of the dub package's source tree
        schema['properties']['target-path'] = {
            'type': 'string',
            'default': ''
        }
        return schema

    def __init__(self, name, options, project):
        super().__init__(name, options, project)
        self.build_packages.append('dub')

    def build(self):
        super().build()

        # Handle the build type and config, and run the
        # corresponding `dub` command
        self.run(['dub', 'build', self.options.build_target]
                 + self.options.build_flags)

        # Copy files from the build dir to the install dir
        # (necessary since dub has no `install` command of
        # its own)
        dub_target_dir = os.path.join(self.partdir, 'build',
                                      self.options.target_path)
        for entry in os.scandir(dub_target_dir):
            if entry.is_file() or entry.is_dir():
                entry_path = os.path.join(dub_target_dir, entry.name)
                shutil.copy2(entry_path, self.installdir)
