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
# 2020.02.05 - SBerendsen - Initial version
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
# Rate object.
#
# ------------------------------------------------------------------------------
#
# ToDo:
#   - add ability to set start & end time
#   - support other rate generation types
#
# ------------------------------------------------------------------------------
#

# 0. Imports ===================================================================

# general

# internal
from ..util import base_optimisation as base_optimisation
from ..util import utilities as util

# 1. Global vars ===============================================================


# 1.1 Classes ------------------------------------------------------------------
class IORate(base_optimisation.BaseMOEA):
    
    def __init__(self):

        base_optimisation.BaseMOEA.__init__(self)

        # Required
        self.name      = None
        self.type      = None
        self.const_val = None


    def load(self, item):
        """
        Loads a rate instance from a given entry.

        Inputs:
        item
            Object holding the rate entry.
        """

        self.name = util.safe_get_dict_item(item, "Name", 'Rate.load')
        self.type = util.safe_get_dict_item(item, "Type", 'Rate.load')

        if (self.type == 'constant'):
            self.const_val = util.safe_get_dict_item(item, "Const_Val",
                                                     'Rate.load')

        else:
            print('Rate.load: Error:')
            print('Unsupported rate type:', self.type)
            exit(255)


    def check(self):
        print("Rate.check: Not yet implemented")
        exit(255)


    def write(self, f):
        f.write('\n\n      - Rate:')
        f.write('\n        Name:      ' + self.name)
        f.write('\n        Type:      ' + self.type)

        if (self.type == 'constant'):
            f.write('\n        Const_Val: ' + str(self.const_val))

        else:
            print('Rate.write: Error:')
            print('Unsupported rate type:', self.type)
            exit(255)


    def moea_gen_vectors(self, vec_debug):

        vec_var      = []
        vec_boundary = []
        vec_epsilon  = []

        # working on itself
        if (self.type == 'constant'):
            vec_var      += [self.const_val]
            vec_boundary += [[self.const_val * 0.1, self.const_val * 10.0]]
            vec_epsilon  += [base_optimisation.get_epsilon_value()]

        else:
            print('Rate.moea_gen_vectors: Error:')
            print('Unsupported rate type:', self.type)
            exit(255)

        # set local data
        self.set_data_extend(len(vec_var))
        if (vec_debug):
            self.set_vec(vec_var)

        return vec_var, vec_boundary, vec_epsilon


    def moea_insert_vector(self, vec):

        num = 0  # number of data places already inserted

        # sanity bounds check
        self.moea_check_vec_bounds(vec, 'Rate')

        # insert data
        if (self.type == 'constant'):
            self.const_val = vec[0]
            num = 1

        else:
            print('Rate.moea_gen_vectors: Error:')
            print('Unsupported rate type:', self.type)
            exit(255)

        # sanity_check
        self.moea_check_vec_extend(num, 'rate', vec)

        return num


# 2. Functions =================================================================


# 3. Main Exec =================================================================
if __name__ == '__main__':
    print('Testing')