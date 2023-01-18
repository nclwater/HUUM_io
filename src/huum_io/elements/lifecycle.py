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
# 2019.12.13 - SBerendsen - Initial version
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
# Lifecycle status object.
#
# ------------------------------------------------------------------------------
#


# 0. Imports ===================================================================

# general

# internal
from ..events import event as event
from ..elements import alternative as alternative
from ..elements import probability as probability
from ..util import base_optimisation as base_optimisation
from ..util import utilities as util

# 1. Global vars ===============================================================


# 1.1 Classes ------------------------------------------------------------------
class IOLifeCycle(base_optimisation.BaseMOEA):
    def __init__(self):

        super().__init__()

        # Required
        self.name         = None
        self.habit_status = None
        self.next_default = None    # next default item
        self.next         = []      # list of alternatives for the next
        self.probability  = None    # Changeover time (probability object to determine the)

        # Optional
        self.min_duration = None    # [sec] minimum duration of lifecycle status
        self.events       = []      # associated events


    def load(self, item):
        """
        Loads a lifecycle instance from a given entry.

        Inputs:
        item
            Object holding the lifecycle entry.
        """

        # get main info --------------------------------------------------------
        self.name         = item["Name"].lower()
        self.habit_status = item["Habit_Status"].lower()

        # Next target(s) -------------------------------------------------------
        obj               = item["Next"]
        self.next_default = obj["Default"].lower()

        if ("Alternatives" in obj):
            alternatives = obj["Alternatives"]
            for alt in alternatives:
                entry = alternative.IOAlternative()
                entry.load(alt)
                self.next.append(entry)

        # Changeover time ------------------------------------------------------
        change = util.safe_get_dict_item(item, 'Changeover_Time',
                                         'LifeCycle.load')
        self.probability = probability.IOProbability()
        self.probability.load(change)

        # Optional data --------------------------------------------------------
        if ("Minimum_Duration" in item):
            self.min_duration = item["Minimum_Duration"]

        if ("Events" in item):
            events = item["Events"]
            for part in events:
                entry = event.IOEvent()
                entry.load(part)
                self.events.append(entry)

        return


    def check(self):
        print("lifecycle.check: Not yet implemented")
        exit(255)


    def write(self, f):
        f.write('\n\n  - Name:         ' + self.name)
        f.write('\n    Habit_Status: ' + self.habit_status)

        f.write('\n\n    Next:')
        f.write('\n      Default: ' + self.next_default)
        if (len(self.next) > 0):
            f.write('\n\n      Alternatives:')
            for choice in self.next:
                choice.write(f)

        f.write('\n\n    Changeover_Time:')
        self.probability.write(f, '    ')

        if (len(self.events) > 0):
            f.write('\n\n    Events:')
            for occurance in self.events:
                occurance.write(f, '    ')


    def moea_gen_vectors(self, vec_debug):

        vec_var      = []
        vec_boundary = []
        vec_epsilon  = []

        # work on itself

        # mininum duration
        if not (self.min_duration is None):
            vec_var += [self.min_duration]
            vec_boundary += [[
                self.min_duration * 0.1, self.min_duration * 10.0
            ]]
            vec_epsilon += [base_optimisation.get_epsilon_value()]

        # change over probability
        triple = self.probability.moea_gen_vectors(vec_debug)
        vec_var += triple[0]
        vec_boundary += triple[1]
        vec_epsilon += triple[2]

        # do the events
        for e in self.events:
            triple = e.moea_gen_vectors(vec_debug)
            vec_var += triple[0]
            vec_boundary += triple[1]
            vec_epsilon += triple[2]

        # set local data
        self.set_data_extend(len(vec_var))
        if (vec_debug):
            self.set_vec(vec_var)

        return vec_var, vec_boundary, vec_epsilon


    def moea_insert_vector(self, vec):

        num = 0  # number of data places already inserted

        # sanity bounds check
        self.moea_check_vec_bounds(vec, 'Lifecycle')

        # insert data for self
        if not (self.min_duration is None):
            self.min_duration = vec[num]
            num += 1

        # insert data - probability
        num += self.probability.moea_insert_vector(
            vec[num:num + self.probability.get_data_extend()])

        # insert data - events
        for e in self.events:
            num += e.moea_insert_vector(vec[num:num + e.get_data_extend()])

        # sanity_check
        self.moea_check_vec_extend(num, 'lifecycle', vec)

        return num


# 2. Functions =================================================================

# 3. Main Exec =================================================================
if __name__ == '__main__':
    print('Testing')