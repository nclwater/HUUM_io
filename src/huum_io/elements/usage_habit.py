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
# Usage Habit objects.
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
class IOUsageHabit(base_optimisation.BaseMOEA):

    def __init__(self):

        base_optimisation.BaseMOEA.__init__(self)

        self.name             = None    # name of habit
        self.appliance        = None    # name of target appliance
        self.valid_when       = None    # during which lifecycle habit group it is active
        self.valid_t_start    = None    # starting timepoint for time-limiting
        self.valid_t_end      = None    # ending timepoint for time-limiting
        self.computation_type = 'add'   # what kind of habit it is, additive or multiplicative
        self.data_type        = None    # data graph: what kind of

        self.data_value       = None    # data graph: needed value(s)
        self.data_function    = None    # uuid-model-internal-path to function


    def load(self, item):
        """
        Loads the usage habit info from the given object.

        Inputs:

        item
            Object holding the usage habit info entry.
        """
        # get general data
        self.name             = util.safe_get_dict_item(item, "Name", 'UsageHabit.load')
        self.appliance        = util.safe_get_dict_item(item, "Appliance", 'UsageHabit.load')
        if ('Valid_When' in item):
            self.valid_when   = util.safe_get_dict_item(item, "Valid_When", 'UsageHabit.load')
        self.valid_t_start    = util.safe_get_dict_item(item, "Valid_t_Start", 'UsageHabit.load')
        self.valid_t_end      = util.safe_get_dict_item(item, "Valid_t_End", 'UsageHabit.load')
        self.computation_type = util.safe_get_dict_item(item, "Computation_Type", 'UsageHabit.load')

        # get data definition
        obj = util.safe_get_dict_item(item, "Data", 'UsageHabit.load')
        self.data_type = util.safe_get_dict_item(obj, 'Type', 'UsageHabit.load')

        if (self.data_type == 'Constant'):
            self.data_value = util.safe_get_dict_item(obj, "Value", 'UsageHabit.load')
        
        elif (self.data_type == 'Function'):
            self.data_function = util.safe_get_dict_item(obj, "Function", 'UsageHabit.load')

        else:
            print('\nError: UsageHabit.load:')
            print('Unknown/Unsupported Data.Type value:', self.data_value)
            print('Object:', obj)
            exit(255)


    def check(self):
        print("UsageHabit.check: Not yet implemented")
        exit(255)


    def write(self, f):
        f.write('\n\n  - Habit:')
        f.write('\n    Name:             ' + self.name)
        f.write('\n    Appliance:        ' + self.appliance)
        if not (self.valid_when is None):
            f.write('\n    Valid_When:       ' + self.valid_when)
        f.write('\n    Valid_t_Start:    ' + self.valid_t_start)
        f.write('\n    Valid_t_End:      ' + self.valid_t_end)
        f.write('\n    Computation_Type: ' + self.computation_type)
        f.write('\n    Data:')
        f.write('\n      Type:           ' + self.data_type)
        
        if (self.data_type == 'Constant'):
            f.write('\n      Value:          ' + str(self.data_value))

        elif (self.data_type == 'Function'):
            f.write('\n      Function:       ' + str(self.data_function))
        
        else:
            print('\nError: UsageHabit.write:')
            print('Unknown/Unsupported Data.Type value:', self.data_value)
            exit(255)


    def moea_gen_vectors(self, vec_debug):

        vec_var      = []
        vec_boundary = []
        vec_epsilon  = []

        # working on itself
        if (self.data_type == 'Constant'):
            vec_var      = [self.data_value]
            vec_boundary = [[self.data_value * 0.1, self.data_value * 10.0]]
            vec_epsilon  = [base_optimisation.get_epsilon_value()]
        
        elif (self.data_type == 'Function'):
            pass

        else:
            print('\nError: UsageHabit.moea_gen_vectors:')
            print('Unknown/Unsupported Data.Type value:', self.data_value)
            exit(255)

        # set local data
        self.set_data_extend(len(vec_var))
        if (vec_debug):
            self.set_vec(vec_var)

        return vec_var, vec_boundary, vec_epsilon


    def moea_insert_vector(self, vec):

        num = 0  # number of data places already inserted

        # sanity bounds check
        self.moea_check_vec_bounds(vec, 'UsageHabit')

        # working on itself
        if (self.data_type == 'Constant'):
            self.data_value = vec[num]
            num += 1
        
        elif (self.data_type == 'Function'):
            pass

        else:
            print('\nError: UsageHabit.moea_gen_vectors:')
            print('Unknown/Unsupported Data.Type value:', self.data_value)
            exit(255)

        # sanity_check
        self.moea_check_vec_extend(num, 'usage_pattern', vec)

        return num


# 2. Functions =================================================================


# 3. Main Exec =================================================================
if __name__ == '__main__':
    print('Testing')