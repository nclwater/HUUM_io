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
# 2020.01.31 - SBerendsen - Initial version
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
# Event object.
#
# ------------------------------------------------------------------------------
#


# 0. Imports ===================================================================

# general

# internal
from . import event_effect as event_effect
from ..elements import probability as probability
from ..util import base_optimisation as base_optimisation
from ..util import utilities as util

# 1. Global vars ===============================================================


# 1.1 Classes ------------------------------------------------------------------
class IOEvent(base_optimisation.BaseMOEA):

    def __init__(self):

        base_optimisation.BaseMOEA.__init__(self)

        # Required
        self.name = None
        self.type = None
        self.switch = False
        self.probability = None
        self.active = True
        self.effects = []


    def load(self, item):
        """
        Loads a event instance from a given entry.

        Inputs:
        item
            Object holding the event entry.
        """

        self.name = util.safe_get_dict_item(item, 'Name', 'Event.load')
        self.type = util.safe_get_dict_item(item, 'Type', 'Event.load')

        if ('Switch' in item):
            self.switch = item['Switch']
        if ('Probability' in item):
            self.probability = probability.IOProbability()
            self.probability.load(item['Probability'])
        if ('Active' in item):
            self.active = item['Active']

        # read effects
        effect_list = util.safe_get_dict_item(item, 'Effects', 'Event.load')

        for entry in effect_list:
            obj = event_effect.IOEventEffect()
            obj.load(entry)
            self.effects.append(obj)


    def check(self):
        print("event.check: Not yet implemented")
        exit(255)


    def write(self, f, prefix=''):
        f.write('\n\n' + prefix + '  - Event:')
        f.write('\n'   + prefix + '    Name:   ' + self.name)
        f.write('\n'   + prefix + '    Type:   ' + self.type)
        f.write('\n'   + prefix + '    Switch: ' + str(self.switch))
        f.write('\n'   + prefix + '    Active: ' + str(self.active))
        if not (self.probability is None):
            f.write('\n' + prefix + '    Probability:')
            self.probability.write(f, prefix + '    ')

        f.write('\n\n' + prefix + '    Effects:')
        for effect in self.effects:
            effect.write(f, prefix)


    def moea_gen_vectors(self,
                         vec_debug: bool,
                         timeseries_adjustment: bool = True):

        vec_var      = []
        vec_boundary = []
        vec_epsilon  = []

        # work on itself
        if not (self.probability is None):
            triple = self.probability.moea_gen_vectors(vec_debug)
            vec_var      += triple[0]
            vec_boundary += triple[1]
            vec_epsilon  += triple[2]

        # get the event effects done
        for effect in self.effects:
            triple = effect.moea_gen_vectors(vec_debug, timeseries_adjustment)
            vec_var      += triple[0]
            vec_boundary += triple[1]
            vec_epsilon  += triple[2]

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
        self.moea_check_vec_bounds(vec, 'Event')

        # work on itself
        if not (self.probability is None):
            num += self.probability.moea_insert_vector(
                vec[num:num + self.probability.get_data_extend()])

        # get the event effects done
        for effect in self.effects:
            num += effect.moea_insert_vector(
                vec[num:num + effect.get_data_extend()], timeseries_adjustment)

        # sanity_check
        self.moea_check_vec_extend(num, 'event', vec)

        return num


# 2. Functions =================================================================


# 3. Main Exec =================================================================
if __name__ == '__main__':
    print('Testing')