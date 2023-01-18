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
from ..translators import translator as translator
from ..util import base_optimisation as base_optimisation
from ..util import utilities as util

# 1. Global vars ===============================================================


# 1.1 Classes ------------------------------------------------------------------
class IOTimedStorage(base_optimisation.BaseMOEA):

    def __init__(self):

        base_optimisation.BaseMOEA.__init__(self)

        # Required
        self.name        = None
        self.start_t     = None     # start datum
        self.translators = []


    def load(self, item):
        """
        Loads a storage instance from a given entry.

        Inputs:
        item
            Object holding the storage entry.
        """

        # get main info --------------------------------------------------------
        self.name    = util.safe_get_dict_item(item, "Name", 'TimedStorage.load')
        self.start_t = util.safe_get_dict_item(item, "Start_t", 'TimedStorage.load')


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
        f.write('\n    Name:    ' + self.name)
        f.write('\n    Start_t: ' + self.name)

        if (len(self.translators) > 0):
            f.write('\n\n    Translators:')
            for item in self.translators:
                item.write(f)


    def moea_gen_vectors(self, vec_debug):

        vec_var      = []
        vec_boundary = []
        vec_epsilon  = []

        # Nothing to do for itself (adjusting t_start is for later)

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
        self.moea_check_vec_bounds(vec, 'TimedStorage')

        # Nothing to be done for itself - leave t_start for later

        # work on the translators
        for changer in self.translators:
            num += changer.moea_insert_vector(vec[num:num +
                                                  changer.get_data_extend()])

        # sanity_check
        self.moea_check_vec_extend(num, 'timed_storage', vec)

        return num


# 2. Functions =================================================================


# 3. Main Exec =================================================================
if __name__ == '__main__':
    print('Testing')