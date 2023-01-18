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
# Translator object.
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
class IOTranslator(base_optimisation.BaseMOEA):

    def __init__(self):

        base_optimisation.BaseMOEA.__init__(self)

        # Required
        self.return_above = 'last'
        self.return_below = 'first'
        self.active_for   = None
        self.table_x      = None
        self.table_y      = None


    def load(self, item):
        """
        Loads a rate instance from a given entry.

        Inputs:
        item
            Object holding the rate entry.
        """

        self.active_for = util.safe_get_dict_item(item, "Active_for",
                                                  'Translator.load')
        self.table_x    = util.safe_get_dict_item(item, "Table_x",
                                                  'Translator.load')
        self.table_y    = util.safe_get_dict_item(item, "Table_y",
                                                  'Translator.load')

        if ('Return_below' in item):
            self.return_below = item['Return_below']

        if ('Return_above' in item):
            self.return_above = item['Return_above']


    def check(self):
        print("Translator.check: Not yet implemented")
        exit(255)


    def write(self, f):
        f.write('\n\n      - Translator:')
        f.write('\n        Active_for:   ' + self.active_for)

        if not (self.return_above is None):
            f.write('\n        Return_above: ' + self.return_above)

        if not (self.return_below is None):
            f.write('\n        Return_below: ' + self.return_below)

        f.write('\n        Table_x:      ' + str(self.table_x))
        f.write('\n        Table_y:      ' + str(self.table_y))

    def moea_gen_vectors(self, vec_debug):

        vec_var      = []
        vec_boundary = []
        vec_epsilon  = []

        # working on itself

        # deal with the two arrays:
        # no assumption for either one of them
        vec_var      += [self.table_x[0]]
        vec_boundary += [[vec_var[0] * 0.1, vec_var[0] * 10.0]]
        vec_epsilon  += [base_optimisation.get_epsilon_value()]

        for i in range(0, len(self.table_x) - 1):
            vec_var      += [self.table_x[i + 1] - self.table_x[i]]
            vec_boundary += [[vec_var[-1] * 0.1, vec_var[-1] * 10.0]]
            vec_epsilon  += [base_optimisation.get_epsilon_value()]

        #   _Val, assume first and last are always 0, then enter the rest
        for i in range(0, len(self.table_y)):
            vec_var      += [self.table_y[i]]
            vec_boundary += [[vec_var[-1] * 0.1, vec_var[-1] * 10.0]]
            vec_epsilon  += [base_optimisation.get_epsilon_value()]

        # set local data
        self.set_data_extend(len(vec_var))
        if (vec_debug):
            self.set_vec(vec_var)

        return vec_var, vec_boundary, vec_epsilon


    def moea_insert_vector(self, vec):

        num = 0  # number of data places already inserted

        # sanity bounds check
        self.moea_check_vec_bounds(vec, 'Translator')

        # working on itself

        # deal with the two arrays:
        self.table_x[0] = vec[0]
        num += 1

        for i in range(num - 1, (len(self.table_x) - 1)):
            self.table_x[i] = vec[i] + self.table_x[i - 1]
        num += len(self.table_x) - 1

        # y-coords
        for i in range(num, (num + len(self.table_x))):
            self.table_y[i - num] = vec[i]
        num += len(self.table_y)

        # sanity_check
        self.moea_check_vec_extend(num, 'translator', vec)

        return num


# 2. Functions =================================================================


# 3. Main Exec =================================================================
if __name__ == '__main__':
    print('Testing')