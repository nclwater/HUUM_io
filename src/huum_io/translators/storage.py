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
# Storage object.
#
# ------------------------------------------------------------------------------
#



# 0. Imports ===================================================================

# general

# internal
from ..translators import rate as rate
from ..translators import translator as translator
from ..util import base_optimisation as base_optimisation
from ..util import utilities as util

# 1. Global vars ===============================================================


# 1.1 Classes ------------------------------------------------------------------
class IOStorage(base_optimisation.BaseMOEA):

    def __init__(self):

        base_optimisation.BaseMOEA.__init__(self)

        # Required
        self.name           = None
        self.rates          = []
        self.translators    = []
        self.initial_volume = 0.0


    def load(self, item):
        """
        Loads a storage instance from a given entry.

        Inputs:
        item
            Object holding the storage entry.
        """

        # get main info --------------------------------------------------------
        self.name = util.safe_get_dict_item(item, "Name", 'storage.load')
        if ('Initial_Volume' in item):
            self.initial_volume = util.safe_get_dict_item(item, 'Initial_Volume', 'storage.load')

        # Rates ----------------------------------------------------------------
        if ('Rates' in item):
            obj = item["Rates"]

            for rate_obj in obj:
                set_rate = rate.IORate()
                set_rate.load(rate_obj)
                self.rates.append(set_rate)

        # Translators ----------------------------------------------------------
        if ('Translators' in item):
            obj = item["Translators"]

            for tranlate_obj in obj:
                set_translator = translator.IOTranslator()
                set_translator.load(tranlate_obj)
                self.translators.append(set_translator)


    def check(self):
        print("Storage.check: Not yet implemented")
        exit(255)


    def write(self, f):
        f.write('\n\n  - Storage:')
        f.write('\n    Name:           ' + self.name)
        f.write('\n    Initial_Volume: ' + str(self.initial_volume))

        if (len(self.rates) > 0):
            f.write('\n\n    Rates:')
            for item in self.rates:
                item.write(f)

        if (len(self.translators) > 0):
            f.write('\n\n    Translators:')
            for item in self.translators:
                item.write(f)


    def moea_gen_vectors(self, vec_debug):

        vec_var      = []
        vec_boundary = []
        vec_epsilon  = []

        # work on itself
        vec_var      = [self.initial_volume]
        vec_boundary = [[
            self.initial_volume * 0.1, self.initial_volume * 10.0
        ]]
        vec_epsilon  = [base_optimisation.get_epsilon_value()]

        # work on the rates
        for increase in self.rates:
            triple = increase.moea_gen_vectors(vec_debug)
            vec_var      += triple[0]
            vec_boundary += triple[1]
            vec_epsilon  += triple[2]

        # work on the translators
        for changer in self.translators:
            triple = changer.moea_gen_vectors(vec_debug)
            vec_var      += triple[0]
            vec_boundary += triple[1]
            vec_epsilon  += triple[2]

        # set local data
        self.set_data_extend(len(vec_var))
        if (vec_debug):
            self.set_vec(vec_var)

        return vec_var, vec_boundary, vec_epsilon


    def moea_insert_vector(self, vec):

        num = 0  # number of data places already inserted

        # sanity bounds check
        self.moea_check_vec_bounds(vec, 'Storage')

        # insert local data
        self.initial_volume = vec[0]
        num += 1

        # work on the rates
        for incrase in self.rates:
            num += rate.moea_insert_vector(vec[num:num +
                                               rate.get_data_extend()])

        # work on the translators
        for changer in self.translators:
            num += changer.moea_insert_vector(vec[num:num +
                                                  changer.get_data_extend()])

        # sanity_check
        self.moea_check_vec_extend(num, 'storage', vec)

        return num

# 2. Functions =================================================================


# 3. Main Exec =================================================================
if __name__ == '__main__':
    print('Testing')