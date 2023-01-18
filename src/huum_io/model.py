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
# Main model object.
#
# ------------------------------------------------------------------------------
#

# 0. Imports ===================================================================

# general
import os
import ruamel.yaml as YAML

# internal
from . import holding
from .elements import common_parts as common_parts

# 1. Global vars ===============================================================


# 1.1 Classes ------------------------------------------------------------------
class IOModel(common_parts.CommonParts
              ):  # class to hold data above holdings level

    def __init__(self):

        common_parts.CommonParts.__init__(self)

        self.holdings = []

    @classmethod
    def load(cls, fn, dir_root, only_model=False):
        """
        loads the model file and (optionally) it's holding constituents.

        Inputs:
        fn
            filename to load
        dir_root
            model data structure root directory
        only_model
            whether only the model file should be loaded or the parts as well (default:False)
        """

        # sanity check
        input_file = os.path.join(os.path.normcase(dir_root), fn)
        exists = os.path.isfile(input_file)
        if not exists:
            print('')
            print('\nHUUM model file ' + input_file + ' does not exist')
            print('Working dir: ' + str(os.getcwd()))
            exit(255)

        # get data
        f = open(input_file, 'r')
        cls = IOModel.from_fileobject(f, dir_root)
        f.close()

        return cls

    @classmethod
    def from_zip(cls, fn: str, zfile, base_dir):

        with zfile.open(f'{base_dir}{fn}') as f_obj:
            cls = IOModel.from_fileobject(f_obj, base_dir, zfile)

        return cls

    @classmethod
    def from_fileobject(cls, f_obj, dir_root, zfile=None):

        cls = IOModel()

        model_data = YAML.YAML(typ='safe', pure=True).load(f_obj)
        for hold in model_data['Holdings']:
            unit = holding.IOHolding()
            unit.load(hold, dir_root, zfile)
            cls.holdings.append(unit)

        # load common stuff
        cls.load_common(model_data)

        return cls

    def check(self):
        print("model.check: Not yet implemented")
        exit(255)

    def write(self, dir_out, fn):

        # assure that the output directory exists
        if not os.path.exists(dir_out):
            os.makedirs(dir_out)

        # write file
        f = open(os.path.join(dir_out, fn), 'w')

        # write header
        f.write("%YAML 1.2\n---\n")

        f.write('\nHoldings:\n')
        for unit in self.holdings:
            f.write('- ' + unit.id + '/holding.yaml\n')
            unit.write(dir_out, unit.id)

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
        for hold in self.holdings:
            triple = hold.moea_gen_vectors(vec_debug, timeseries_adjustment)
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

        # safety checks
        # for boundary, both bounds are not allowed to be zero
        flag = False
        for i, item in enumerate(vec_boundary):

            # if identical, shift by a tiny amount
            if (item[0] == item[1]):
                vec_boundary[i] = [0.0, 0.1e-13]

            # check for wrong way around
            if (item[0] > item[1]):
                print('IOModel.moea_gen_vectors: Error')
                print(
                    'Generated boundary pair has the lower bound bigger than upper'
                )
                print('LowerBound:', item[0])
                print('UpperBound:', item[1])
                flag = True

            if (flag):
                exit(255)

        return vec_var, vec_boundary, vec_epsilon

    def moea_insert_vector(self,
                           vec: list,
                           timeseries_adjustment: bool = True):

        num = 0  # number of data places already inserted

        # sanity bounds check
        self.moea_check_vec_bounds(vec, 'Model')

        # insert data - nothing to do for self

        # insert data - holdings
        for hold in self.holdings:
            num += hold.moea_insert_vector(
                vec[num:num + hold.get_data_extend()], timeseries_adjustment)

        # insert data - common items
        num += self.common_insert_vector(vec[num:], timeseries_adjustment)

        # sanity_check
        self.moea_check_vec_extend(num, 'model', vec)


# 2. Functions =================================================================

# 3. Main Exec =================================================================
if __name__ == '__main__':
    print('Testing')