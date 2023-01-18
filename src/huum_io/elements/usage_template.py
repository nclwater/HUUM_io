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
# 2019.01.29 - SBerendsen - Initial version
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
# Usage Habit Template objects.
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
class IOUsageTemplate(base_optimisation.BaseMOEA):

    def __init__(self):

        base_optimisation.BaseMOEA.__init__(self)

        self.name              = None   # name of habit
        self.appliance         = None   # name of target appliance
        self.valid_when        = None   # during which lifecycle habit group it is active
        self.template_type     = None   # where the template attaches
        self.duration          = None   # [sec] how long the template instance is active for
        self.buffer            = 0      # [sec] how long should the buffer between the target time and the given timeslot
        self.computation_type  = 'add'  # what kind of habit it is, additive or multiplicative
        self.probability_t     = None   # [sec] probability curve data, time
        self.probability_value = None   # probability curve data, y data for each timepoint


    def load(self, item):
        """
        Loads the usage habit template info from the given object.

        Inputs:

        item
            Object holding the usage habit template info entry.
        """
        # get general data
        self.name = util.safe_get_dict_item(item, "Name", 'UsageTemplate.load')
        self.appliance = util.safe_get_dict_item(item, "Appliance",
                                                 'UsageTemplate.load')
        self.valid_when = util.safe_get_dict_item(item, "Valid_When",
                                                  'UsageTemplate.load')
        self.template_type = util.safe_get_dict_item(item, "Type",
                                                     'UsageTemplate.load')
        self.duration = util.safe_get_dict_item(item, "Duration",
                                                'UsageTemplate.load')
        self.buffer = util.get_dict_item_if_exists(item, "Buffer", 0)
        self.computation_type = util.safe_get_dict_item(
            item, "Computation_Type", 'UsageTemplate.load')
        self.probability_t = util.safe_get_dict_item(item, "Probability_t",
                                                     'UsageTemplate.load')
        self.probability_value = util.safe_get_dict_item(
            item, "Probability_Value", 'UsageTemplate.load')


    def check(self):
        print("UsageTemplate.check: Not yet implemented")
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
            f.write('\n\n' + prefix + '  Habit:')
        else:
            f.write('\n\n' + prefix + '  - Habit:')

        f.write('\n' + prefix + '    Name:              ' + self.name)
        f.write('\n' + prefix + '    Appliance:         ' + self.appliance)
        f.write('\n' + prefix + '    Valid_When:        ' + self.valid_when)
        f.write('\n' + prefix + '    Type:              ' + self.template_type)
        f.write('\n' + prefix + '    Duration:          ' + str(self.duration))
        f.write('\n' + prefix + '    Buffer:            ' + str(self.buffer))
        f.write('\n' + prefix + '    Computation_Type:  ' +
                self.computation_type)
        f.write('\n' + prefix + '    Probability_t:     ' +
                str(self.probability_t))
        f.write('\n' + prefix + '    Probability_Value: ' +
                str(self.probability_value))


    def moea_gen_vectors(self, vec_debug):

        vec_var      = []
        vec_boundary = []
        vec_epsilon  = []

        # working on itself

        # deal with the two arrays:
        #   _t, work as t0 + deltas
        vec_var      += [self.probability_t[0]]
        vec_boundary += [[
            self.probability_t[0] * 0.1, self.probability_t[0] * 10.0
        ]]
        vec_epsilon  += [base_optimisation.get_epsilon_value()]

        for i in range(0, len(self.probability_t) - 1):
            vec_var      += [self.probability_t[i + 1] - self.probability_t[i]]
            vec_boundary += [[vec_var[-1] * 0.1, vec_var[-1] * 10.0]]
            vec_epsilon  += [base_optimisation.get_epsilon_value()]

        #   _Val, assume first and last are always 0, then enter the rest
        for i in range(1, (len(self.probability_value) - 1)):
            vec_var      += [self.probability_value[i]]
            vec_boundary += [[vec_var[-1] * 0.1, vec_var[-1] * 10.0]]
            vec_epsilon  += [base_optimisation.get_epsilon_value()]

        # duration = delta last time entry and given duration
        # added last for easier back conversion
        vec_var      += [self.duration - self.probability_t[-1]]
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
        self.moea_check_vec_bounds(vec, 'UsageTemplate')

        # working on itself

        # deal with the two arrays:
        #   _t, work as t0 + deltas
        self.probability_t[0] = vec[0]
        for i in range(num + 1, (num + len(self.probability_t) - 1)):
            self.probability_t[i] = vec[i] + self.probability_t[i - 1]
        num += len(self.probability_t)

        #   _Val, assume first and last are always 0, then enter the rest
        for i in range(num, (num + len(self.probability_t) - 2)):
            self.probability_value[i - num + 1] = vec[i]
        num += max(len(self.probability_value) - 2, 0)

        # duration = delta last time entry and given duration
        # added last for easier back conversion
        self.duration = self.probability_t[-1] + vec[num]
        num += 1

        # sanity_check
        self.moea_check_vec_extend(num, 'usage_template', vec)

        return num


# 2. Functions =================================================================


# 3. Main Exec =================================================================
if __name__ == '__main__':
    print('Testing')