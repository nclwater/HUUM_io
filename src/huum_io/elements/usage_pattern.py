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
# Usage Pattern object.
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
class IOUsagePattern(base_optimisation.BaseMOEA):

    def __init__(self):

        base_optimisation.BaseMOEA.__init__(self)

        self.name         = None  # name of pattern
        self.demand_type  = None  # id of demand type
        self.usage_length = None  # how long this usage lasts
        self.usage_t      = None  # timesteps of the usage graph
        self.usage_value  = None  # corresponding values of the usage graph


    def load(self, item):
        """
        Loads the usage pattern info from the given object.

        Inputs:

        item
            Object holding the usage pattern info entry.
        """
        # get general data
        self.name         = util.safe_get_dict_item(item, 'Name', 
                                                    'UsagePattern.load')
        self.demand_type  = util.safe_get_dict_item(item, 'Type',
                                                    'UsagePattern.load')
        self.usage_length = util.safe_get_dict_item(item, 'Usage_Length',
                                                    'UsagePattern.load')
        self.usage_t      = util.safe_get_dict_item(item, 'Usage_t',
                                                    'UsagePattern.load')
        self.usage_value  = util.safe_get_dict_item(item, 'Usage_val',
                                                    'UsagePattern.load')

    def check(self):
        print("UsagePattern.check: Not yet implemented")
        exit(255)


    def write(self, f, prefix='', no_list_item=False):
        """
        Writes the object in YAML style to a file.

        Inputs:
        f
            file object
        prefix
            (Optional) extra spaces to enter 
        no_list_item
            Whether it is a list item (needs a dash) or not
        """
        if (no_list_item):
            f.write('\n\n' + prefix + '  Pattern:')
        else:
            f.write('\n\n' + prefix + '  - Pattern:')

        f.write('\n' + prefix + '    Name:         ' + self.name)
        f.write('\n' + prefix + '    Type:         ' + self.demand_type)
        f.write('\n' + prefix + '    Usage_Length: ' + str(self.usage_length))
        f.write('\n' + prefix + '    Usage_t:      ' + str(self.usage_t))
        f.write('\n' + prefix + '    Usage_val:    ' + str(self.usage_value))


    def moea_gen_vectors(self, vec_debug):

        vec_var      = []
        vec_boundary = []
        vec_epsilon  = []

        # working on itself

        # deal with the two arrays:
        #   _t, work as t0 + deltas
        vec_var      += [self.usage_t[0]]
        vec_boundary += [[self.usage_t[0] * 0.1, self.usage_t[0] * 10.0]]
        vec_epsilon  += [base_optimisation.get_epsilon_value()]
        for i in range(0, (len(self.usage_t) - 1)):
            vec_var      += [self.usage_t[i + 1] - self.usage_t[i]]
            vec_boundary += [[vec_var[-1] * 0.1, vec_var[-1] * 10.0]]
            vec_epsilon  += [base_optimisation.get_epsilon_value()]

        #   _Val, assume first and last are always 0, then enter the rest
        for i in range(1, (len(self.usage_value) - 1)):
            vec_var      += [self.usage_value[i]]
            vec_boundary += [[vec_var[-1] * 0.1, vec_var[-1] * 10.0]]
            vec_epsilon  += [base_optimisation.get_epsilon_value()]

        # duration = delta last time entry and given duration
        # added last for easier back conversion
        vec_var      += [self.usage_length - self.usage_t[-1]]
        vec_boundary += [[vec_var[0] * 0.1, vec_var[0] * 10.0]]
        vec_epsilon  += [base_optimisation.get_epsilon_value()]

        # set local data
        self.set_data_extend(len(vec_var))
        if (vec_debug):
            self.set_vec(vec_var)

        return vec_var, vec_boundary, vec_epsilon


    def moea_insert_vector(self, vec):

        num = 0  # number of data places already inserted

        # sanity bounds check
        self.moea_check_vec_bounds(vec, 'UsagePattern')

        # working on itself

        # deal with the two arrays:
        #   _t, work as t0 + deltas
        self.usage_t[0] = vec[0]
        for i in range(num + 1, (num + len(self.usage_t) - 1)):
            self.usage_t[i] = max(vec[i] + self.usage_t[i - 1], 1.0)
        num += len(self.usage_t)

        #   _Val, assume first and last are always 0, then enter the rest
        for i in range(num, (num + len(self.usage_value) - 2)):
            self.usage_value[i - num + 1] = vec[i]
        num += max(len(self.usage_value) - 2, 0)

        # duration = delta last time entry and given duration
        # added last for easier back conversion
        self.usage_length = self.usage_t[-1] + vec[num]
        num += 1

        # sanity_check
        self.moea_check_vec_extend(num, 'usage_pattern', vec)

        return num


# 2. Functions =================================================================


# 3. Main Exec =================================================================
if __name__ == '__main__':
    print('Testing')