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
# 2019.01.31 - SBerendsen - Initial version
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
# Appliance data object.
#
# ------------------------------------------------------------------------------
#

# 0. Imports ===================================================================

# general
import os
import ruamel.yaml as YAML

# internal
from .util import utilities as util
from .elements import usage_pattern as usage_pattern
from .elements import common_parts as common_parts

# 1. Global vars ===============================================================


# 1.1 Classes ------------------------------------------------------------------
class IOAppliance(common_parts.CommonParts
                  ):  # class  to hold both settings and the model data itself

    def __init__(self):

        super().__init__()

        self.name = None  # the (unique) name of the appliance
        self.appliance_class = None  # the type of appliance
        self.block_length = None  # for how long using the appliance blocks the user
        self.block_user = False  # How long the user is being blocked
        self.usage_patterns = []  # list of usage patterns

    def load(self, fn, dir_root, zfile=None):
        """
        loads the room data file.

        Inputs:
        fn
            filename to load
        dir_root
            model data structure root directory
        zfile
            zipfile object, if loading from zip
        """

        # sanity check
        if zfile is None:
            exists = os.path.basename(
                os.path.normpath(os.path.dirname(os.path.join(dir_root, fn))))
            if not exists:
                print('')
                print('\nHUUM appliance file ' + dir_root + fn +
                      ' does not exist')
                print('Working dir: ' + str(os.getcwd()))
                exit(255)

            # get data
            f = open(os.path.join(dir_root, fn), 'r')
            appliance_data = YAML.YAML(typ='safe', pure=True).load(f)
            f.close()
        else:
            with zfile.open(f'{dir_root}{fn}') as f_obj:
                appliance_data = YAML.YAML(typ='safe', pure=True).load(f_obj)

        self.name = util.safe_get_dict_item(appliance_data, 'Name',
                                            'Appliance.load')
        self.appliance_class = util.get_dict_item_if_exists(
            appliance_data, 'Appliance_Class', self.name)
        self.block_length = util.safe_get_dict_item(appliance_data,
                                                    'Block_Length',
                                                    'Appliance.load')

        for pattern in appliance_data['Usage_Patterns']:
            usage = usage_pattern.IOUsagePattern()
            usage.load(pattern)
            self.usage_patterns.append(usage)

        # load optional stuff
        if ("Block_User" in appliance_data):
            self.block_user = util.safe_get_dict_item(appliance_data,
                                                      'Block_User',
                                                      'Appliance.load')

        # load common stuff
        self.load_common(appliance_data)

    def check(self):
        print("Room.check: Not yet implemented")
        exit(255)

    def write(self, dir_root, dir_file):

        # assure that the output directory exists
        dir_local = f'{dir_root}/{dir_file}'
        if not os.path.exists(dir_local):
            os.makedirs(dir_local)

        # write file
        f = open(f'{dir_local}{self.name}.yaml', 'w')

        # write header
        f.write("%YAML 1.2\n---\n")

        # General Data
        f.write('\nName:            ' + self.name)
        f.write('\nAppliance_Class: ' + self.appliance_class)
        f.write('\nBlock_Length:    ' + str(self.block_length))

        if (self.block_user):
            f.write('\nBlock_User:      ' + str(self.block_user))

        # Specific Data
        f.write('\n\nUsage_Patterns:')
        for pattern in self.usage_patterns:
            pattern.write(f)

        # Common Data
        self.write_common(f)

        f.write('\n')
        f.close()

    def moea_gen_vectors(self, vec_debug, timeseries_adjustment: bool = True):

        vec_var = []
        vec_boundary = []
        vec_epsilon = []

        # work on itself - .block_length is automatically adjusted

        # usage patterns
        if (timeseries_adjustment):
            for pattern in self.usage_patterns:
                triple = pattern.moea_gen_vectors(vec_debug)
                vec_var += triple[0]
                vec_boundary += triple[1]
                vec_epsilon += triple[2]

        # do the common items
        triple = self.gen_common_vectors(vec_debug)
        vec_var += triple[0]
        vec_boundary += triple[1]
        vec_epsilon += triple[2]

        # set local data
        self.set_data_extend(len(vec_var))
        if (vec_debug):
            self.set_vec(vec_var)

        return vec_var, vec_boundary, vec_epsilon

    def moea_insert_vector(self, vec, timeseries_adjustment: bool = True):

        num = 0  # number of data places already inserted

        # sanity bounds check
        self.moea_check_vec_bounds(vec, 'Appliance')

        # insert data for self - not needed as .block_length automaticall set

        # insert data - usage patterns
        if (timeseries_adjustment):
            for pattern in self.usage_patterns:
                num += pattern.moea_insert_vector(
                    vec[num:num + pattern.get_data_extend()])

        # insert data - common items
        num += self.common_insert_vector(vec[num:self.get_data_extend()])

        # sanity_check
        self.moea_check_vec_extend(num, 'appliance', vec)

        return num


# 2. Functions =================================================================

# 3. Main Exec =================================================================
if __name__ == '__main__':
    print('Testing')
