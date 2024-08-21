#
# ------------------------------------------------------------------------------
# HUUM - Household Utilities Usage Model (Prototype)
# Demonstrator for the full model
# ------------------------------------------------------------------------------
#
# Author: Sven Berendsen
#
# Changelog:
#
# 2019.12.05 - SBerendsen - Initial version
#
# ------------------------------------------------------------------------------
#
# Copyright 2019, Sven Berendsen
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# ------------------------------------------------------------------------------
#
# Main entry function(s) for reading & writing HUUM models
#
# ------------------------------------------------------------------------------
#

# 0. Imports ===================================================================

# general
import logging
import os
import zipfile

# internal
from . import model
from . import settings

# 1. Global vars ===============================================================
mod_logger = logging.getLogger(__name__)


# 1.1 Classes ------------------------------------------------------------------
class IOModelHUUM(object
                  ):  # class  to hold both settings and the model data itself

    def __init__(self):
        self.settings = None  # Model settings
        self.model = None  # Model data

    @classmethod
    def load(cls,
             filename,
             force_modelroot: str = '',
             add_modelroot: str = ''):

        if zipfile.is_zipfile(filename):
            cls = IOModelHUUM.load_zip(filename)
        else:
            cls = IOModelHUUM()
            cls.load_settings(filename)

            if add_modelroot != '':
                if cls.settings.dir_modelRoot is None:
                    cls.settings.dir_modelRoot = add_modelroot
                else:
                    cls.settings.dir_modelRoot = add_modelroot + '/' + cls.settings.dir_modelRoot

            if force_modelroot is None:
                force_modelroot = ''

            cls.load_model(force_modelroot)

        return cls

    @classmethod
    def load_zip(cls, fn: str):
        """
        Loads a zipped full model.
        """

        # checks
        if not zipfile.is_zipfile(fn):
            raise TypeError(f'Given file {fn} is not a zip archive.')

        # check for structure
        zf = zipfile.ZipFile(fn, 'r')

        # get numer of top level domains
        top = list({item.split('/')[0] for item in zf.namelist()})
        if len(top) != 1:
            raise RuntimeError('Archive has more than one top-level directory')

        dir_top = top[0]

        # get settings file
        files_first_level = []
        for item in zf.namelist():
            tail, head = os.path.split(item)
            if '.yaml' in head and tail == dir_top:
                files_first_level.append(item)
        if len(files_first_level) != 1:
            raise RuntimeError(
                'Number of .yaml files in the top directory is unequal 1.')

        cls = IOModelHUUM()

        # load settings
        with zf.open(files_first_level[0]) as f_obj:
            cls.settings = settings.IOSettings.from_fileobject(f_obj)

        # and the rest
        cls.model = model.IOModel.from_zip(
            cls.settings.fn_model,
            zfile=zf,
            base_dir=f'{dir_top}/{cls.settings.dir_modelRoot}')

        return cls

    def load_settings(self, filename):
        self.settings = settings.IOSettings.load(filename)

    def load_model(self, force_modelroot: str, add_modelroot: str = ''):

        # sanity check
        if (self.settings is None):
            mod_logger.critical(
                'model_io: Trying to read model without set settings.')
            exit(255)

        if force_modelroot != '':
            modelroot = force_modelroot
        else:
            modelroot = self.settings.dir_modelRoot

        self.model = model.IOModel.load(self.settings.fn_model, modelroot)

    def write_settings(self, filename):

        # sanity check
        if (self.settings is None):
            mod_logger.critical(
                'model_io.write_settings: writing model without set settings.')
            exit(255)

        self.settings.write(filename)

    def write_model(self):

        # sanity check
        if (self.settings is None):
            mod_logger.critical(
                'model_io.write_model: writing model without set settings.')
            exit(255)

        self.model.write(self.settings.dir_modelRoot, self.settings.fn_model)

    def write(self, filename, root_dir=None, manual_data_dir=''):

        # sanity checks
        flag = False
        if (self.settings is None):
            mod_logger.critical(
                'model_io.write: writing model without set settings.')
            flag = True
        if (self.model is None):
            mod_logger.critical(
                'model_io.write: writing model without a model given.')
            flag = True
        if (flag):
            exit(255)

        if not (root_dir is None) or (self.settings.dir_modelRoot is None):
            self.settings.dir_modelRoot = root_dir

        # TODO This is inelegant...massively so
        if manual_data_dir != '':
            tmp = self.settings.dir_modelRoot
            self.settings.dir_modelRoot = manual_data_dir
            self.write_settings(filename)
            self.settings.dir_modelRoot = tmp
        else:
            self.write_settings(filename)

        self.write_model()


# 2. Functions =================================================================

# 3. Main Exec =================================================================
if __name__ == '__main__':
    print('Testing')
