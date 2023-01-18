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
# 2019.12.09 - SBerendsen - Initial version
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
# Holding data object.
#
# ------------------------------------------------------------------------------
#

# 0. Imports ===================================================================

# general
import os
import ruamel.yaml as YAML

# internal
from . import consumer_unit
from .elements import common_parts as common_parts
from .util import utilities as util

# 1. Global vars ===============================================================


# 1.1 Classes ------------------------------------------------------------------
class IOHolding(common_parts.CommonParts
                ):  # class  to hold both settings and the model data itself

    def __init__(self):

        super().__init__()
        self.id = None
        self.cu = []

    def load(self, fn, dir_root, zfile=None, only_consumer_units=False):
        """
        loads the holdings file and (optionally) it's consumer_unit constituents.

        Inputs:
        fn
            filename to load
        dir_root
            model data structure root directory
        zfile
            zip file object when loading from a zip
        only_holdings
            whether only the holdings file should be loaded or the parts as well (default:False)
        """

        # sanity check
        if zfile is None:
            exists = os.path.isfile(dir_root + fn)
            if not exists:
                print('')
                print('\nHUUM holdings file ' + dir_root + fn +
                      ' does not exist')
                print('Working dir: ' + str(os.getcwd()))
                exit(255)

            # get data
            f = open(dir_root + fn, 'r')
            holding_data = YAML.YAML(typ='safe', pure=True).load(f)
            f.close()

        else:
            with zfile.open(f'{dir_root}{fn}') as f_obj:
                holding_data = YAML.YAML(typ='safe', pure=True).load(f_obj)

        # Get general data
        self.id = util.safe_get_dict_item(holding_data, 'Name', 'holding.load')

        for fn_cu in holding_data['Consumer_Units']:
            cu = consumer_unit.IOConsumerUnit()
            cu.load(fn_cu, dir_root, zfile)
            self.cu.append(cu)

        # load common stuff
        self.load_common(holding_data)

    def check(self):
        print("holding.check: Not yet implemented")
        exit(255)

    def write(self, dir_root, dir_file):

        # assure that the output directory exists
        dir_local = os.path.join(dir_root, dir_file)
        if not os.path.exists(dir_local):
            os.makedirs(dir_local)

        # write file
        f = open(os.path.join(dir_local, 'holding.yaml'), 'w')

        # write header
        f.write("%YAML 1.2\n---\n")

        # General Data
        f.write('\nName: ' + self.id)

        # Specific Data
        f.write('\nConsumer_Units:\n')
        for unit in self.cu:
            f.write('- ' + dir_file + '/' + unit.id + '/cu.yaml\n')
            unit.write(dir_root, dir_file + '/' + unit.id + '/')

        # Common Data
        self.write_common(f)

        f.close()

    def moea_gen_vectors(self,
                         vec_debug: bool,
                         timeseries_adjustment: bool = True):

        vec_var = []
        vec_boundary = []
        vec_epsilon = []

        # nothing to do for itself

        # get the holdings done
        for cu in self.cu:
            triple = cu.moea_gen_vectors(vec_debug, timeseries_adjustment)
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

    def moea_insert_vector(self,
                           vec: list,
                           timeseries_adjustment: bool = True):

        num = 0  # number of data places already inserted

        # sanity bounds check
        self.moea_check_vec_bounds(vec, 'Holding')

        # insert data - nothing to do for self

        # insert data - holdings
        for cu in self.cu:
            num += cu.moea_insert_vector(vec[num:num + cu.get_data_extend()],
                                         timeseries_adjustment)

        # insert data - common items
        num += self.common_insert_vector(vec[num:self.get_data_extend()])

        # sanity_check
        self.moea_check_vec_extend(num, 'holding', vec)

        return num


# 2. Functions =================================================================

# 3. Main Exec =================================================================
if __name__ == '__main__':
    print('Testing')