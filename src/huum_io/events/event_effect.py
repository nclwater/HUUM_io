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
# 2020.02.04 - SBerendsen - Initial version
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
# Event effects object.
#
# ------------------------------------------------------------------------------
#


# 0. Imports ===================================================================

# general

# internal
from ..elements import probability as probability
from ..elements import usage_pattern as usage_pattern
from ..elements import usage_template as usage_template
from ..util import base_optimisation as base_optimisation
from ..util import utilities as util

# 1. Global vars ===============================================================


# 1.1 Classes ------------------------------------------------------------------
class IOEventEffect(base_optimisation.BaseMOEA):

    def __init__(self):

        base_optimisation.BaseMOEA.__init__(self)

        # Main Data
        self.target = None
        self.action = None
        self.effect_type = None
        self.effect_data = None


    def load(self, item):
        """
        Loads a lifecycle instance from a given entry.

        Inputs:
        item
            Object holding the event effect entry.
        """

        self.target      = util.safe_get_dict_item(item, 'Target',
                                                   'EventEffect.load')
        self.action      = util.safe_get_dict_item(item, 'Action',
                                                   'EventEffect.load')
        self.effect_type = util.safe_get_dict_item(item, 'Effect_Type',
                                                   'EventEffect.load')

        # deal with effect specific data
        if (self.effect_type == 'Target'):
            self.effect_data = util.safe_get_dict_item(item, 'Target_Data',
                                                       'EventEffect.load')

        elif (self.effect_type == 'Event_Usage_Habit_Template'):
            self.effect_data = usage_template.IOUsageTemplate()
            obj = util.safe_get_dict_item(item, 'Habit', 'EventEffect.load')
            self.effect_data.load(obj)

        elif (self.effect_type == 'Usage_Pattern'):
            self.effect_data = usage_pattern.IOUsagePattern()
            obj = util.safe_get_dict_item(item, 'Pattern', 'EventEffect.load')
            self.effect_data.load(obj)

        elif (self.effect_type == 'Probability'):
            self.effect_data = probability.IOProbability()
            obj = util.safe_get_dict_item(item, 'Probability',
                                          'EventEffect.load')
            self.effect_data.load(obj)

        elif (self.effect_type == 'Value_Function'):
            self.effect_data = util.safe_get_dict_item(item, 'Target_Data',
                                                       'EventEffect.load')

        elif (self.effect_type == 'None'):
            self.effect_data = None

        else:
            print('\nEventEffect.load: Error:')
            print('Unknown/Unsupported effect type:', self.effect_type)
            print(item)
            exit()

        return


    def check(self):
        print("event.check: Not yet implemented")
        exit(255)


    def write(self, f, prefix):
        f.write('\n\n' + prefix + '      - Target:      ' + self.target)
        f.write('\n'   + prefix + '        Action:      ' + self.action)
        f.write('\n'   + prefix + '        Effect_Type: ' + self.effect_type)

        if (self.effect_type == 'Target'):
            f.write('\n' + prefix + '        Target_Data: ' + self.effect_data)

        elif (self.effect_type == 'Event_Usage_Habit_Template'):
            self.effect_data.write(f,
                                   prefix=prefix + '      ',
                                   no_list_item=True)

        elif (self.effect_type == 'Usage_Pattern'):
            self.effect_data.write(f,
                                   prefix=prefix + '      ',
                                   no_list_item=True)

        elif (self.effect_type == 'Probability'):
            f.write('\n' + prefix + '        Probability:')
            self.effect_data.write(f, prefix=prefix + '        ')

        elif (self.effect_type == 'Value_Function'):
            f.write('\n' + prefix + '        Target_Data: ' + self.effect_data)

        elif (self.effect_type == 'None'):
            pass

        else:
            print('\nEventEffect.write: Error:')
            print('Unknown/Unsupported effect type:', self.effect_type)
            exit()


    def moea_gen_vectors(self,
                         vec_debug: bool,
                         timeseries_adjustment: bool = True):

        vec_var      = []
        vec_boundary = []
        vec_epsilon  = []

        # working on it's data
        if (self.effect_type == 'Target' or self.effect_type == 'Value_Function'):
            pass

        elif (self.effect_type == 'Event_Usage_Habit_Template'):
            triple = self.effect_data.moea_gen_vectors(vec_debug)
            vec_var      += triple[0]
            vec_boundary += triple[1]
            vec_epsilon  += triple[2]

        elif (self.effect_type == 'Usage_Pattern'):
            if (timeseries_adjustment):
                triple = self.effect_data.moea_gen_vectors(vec_debug)
                vec_var      += triple[0]
                vec_boundary += triple[1]
                vec_epsilon  += triple[2]

        elif (self.effect_type == 'Probability'):
            triple = self.effect_data.moea_gen_vectors(vec_debug)
            vec_var      += triple[0]
            vec_boundary += triple[1]
            vec_epsilon  += triple[2]

        elif (self.effect_type == 'None'):
            pass

        else:
            print('\nEventEffect.moea_gen_vectors: Error:')
            print('Unknown/Unsupported effect type:', self.effect_type)
            exit()

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
        self.moea_check_vec_bounds(vec, 'EventEffect')

        # insert data
        if (self.effect_type == 'Target' or self.effect_type == 'Value_Function'):
            pass

        elif (self.effect_type == 'Event_Usage_Habit_Template'):
            num += self.effect_data.moea_insert_vector(
                vec[num:num + self.effect_data.get_data_extend()])

        elif (self.effect_type == 'Usage_Pattern'):
            if (timeseries_adjustment):
                num += self.effect_data.moea_insert_vector(
                    vec[num:num + self.effect_data.get_data_extend()])

        elif (self.effect_type == 'Probability'):
            num += self.effect_data.moea_insert_vector(
                vec[num:num + self.effect_data.get_data_extend()])

        elif (self.effect_type == 'None'):
            pass

        else:
            print('\nEventEffect.moea_insert_vector: Error:')
            print('Unknown/Unsupported effect type:', self.effect_type)
            exit()

        # sanity_check
        self.moea_check_vec_extend(num, 'event_effect', vec)

        return num


# 2. Functions =================================================================


# 3. Main Exec =================================================================
if __name__ == '__main__':
    print('Testing')