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
# Probability object.
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
class IOProbability(base_optimisation.BaseMOEA):    

    def __init__(self):

        base_optimisation.BaseMOEA.__init__(self)

        self.type         = None    # sets the changeover time type definition
        self.constant     = None    # info for a constant changeover time
        self.range_from   = None    # info for uniform distribution - range start
        self.range_to     = None    # info for uniform distribution - range to
        self.function     = None    # function target key 
        self.mu           = None    # (normal / gauss) mean value
        self.sigma        = None    # (normal / gauss) standard deviation


    def load(self, item):
        """
        Loads a probability instance from a given entry.

        Inputs:
        item
            Object holding the probability entry.
        """

        self.type = util.safe_get_dict_item(item, 'Type', 'Probability.load')

        if (self.type == 'Constant'):
            self.constant = util.safe_get_dict_item(item, 'Val_const', 'Probability.load-Constant')
        
        elif (self.type == 'Uniform'):
            self.range_from = util.safe_get_dict_item(item, 'Val_from', 'Probability.load-Uniform')
            self.range_to   = util.safe_get_dict_item(item, 'Val_to', 'Probability.load-Uniform')
        
        elif (self.type == 'Gauss'):
            self.mu     = util.safe_get_dict_item(item, 'Mu', 'Probability.load-Gauss')
            self.sigma  = util.safe_get_dict_item(item, 'Sigma', 'Probability.load-Gauss')

        elif (self.type == 'Function'):
            self.function = util.safe_get_dict_item(item, 'Function', 'Probability.load-Function')

        else:
            print('\nProbability.load: Error:')
            print('Unsupported probability type: ' + str(self.type))
            print(item)
            exit(255)
        
        return


    def check(self):
        print("Probability.check: Not yet implemented")
        exit(255)


    def write(self, f, prefix):

        f.write('\n' + prefix + '  Type:      ' + self.type)
        if (self.type == 'Constant'):
            f.write('\n' + prefix + '  Val_const: ' + str(self.constant))
        
        elif (self.type == 'Uniform'):
            f.write('\n' + prefix + '  Val_from:  ' + str(self.range_from))
            f.write('\n' + prefix + '  Val_to:    ' + str(self.range_to))

        elif (self.type == 'Gauss'):
            f.write('\n' + prefix + '  Mu:        ' + str(self.mu))
            f.write('\n' + prefix + '  Sigma:     ' + str(self.sigma))

        elif (self.type == 'Function'):
            f.write('\n' + prefix + '  Function:  ' + str(self.function))

        else:
            print('\nError: Probability.write:')
            print('Unknown/Unsupported type value:', self.type)
            exit(255)


    def moea_gen_vectors(self, vec_debug):

        vec_var      = []
        vec_boundary = []
        vec_epsilon  = []

        # dealing with itself
        if (self.type == 'Constant'):
            vec_var      = [self.constant]
            vec_boundary = [[min(0.0, self.constant * 0.01), max(1.0, self.constant * 100.0)]]
            vec_epsilon  = [base_optimisation.get_epsilon_value()]
        
        elif (self.type == 'Uniform'):
            vec_var      = [self.range_from, self.range_to]
            vec_boundary = [[min(0.0, self.range_from * 0.01), max(1.0, self.range_from * 100.0)], 
                            [min(0.0, self.range_to * 0.01), max(1.0, self.range_to * 100.0)]]
            vec_epsilon  = [base_optimisation.get_epsilon_value(), base_optimisation.get_epsilon_value()]
        
        elif (self.type == 'Gauss'):
            vec_var      = [self.mu, self.sigma]
            vec_boundary = [[min(0.0, self.mu * 0.01), max(1.0, self.mu * 100.0)], 
                            [min(0.0, self.sigma * 0.01), max(1.0, self.sigma * 100.0)]]
            vec_epsilon  = [base_optimisation.get_epsilon_value(), base_optimisation.get_epsilon_value()]

        elif (self.type == 'Function'):
            pass

        else:
            print('\nError: Probability.moea_gen_vectors:')
            print('Unknown/Unsupported type value:', self.type)
            exit(255)

        # set local data
        self.set_data_extend(len(vec_var))
        if (vec_debug):
            self.set_vec(vec_var)

        return vec_var, vec_boundary, vec_epsilon


    def moea_insert_vector(self, vec):

        # dealing with itself
        if (self.type == 'Constant'):
            self.constant = vec[0]
            num           = 1

        elif (self.type == 'Uniform'):
            self.range_from = vec[0]
            self.range_to   = vec[1]
            num             = 2

        elif (self.type == 'Gauss'):
            self.mu    = vec[0]
            self.sigma = vec[1]
            num        = 2

        elif (self.type == 'Function'):
            num = 0

        else:
            print('\nError: Probability.moea_insert_vector:')
            print('Unknown/Unsupported type value:', self.type)
            exit(255)

        # sanity_check
        self.moea_check_vec_extend(num, 'probability', vec)

        return num


# 2. Functions =================================================================


# 3. Main Exec =================================================================
if __name__ == '__main__':
    print('Testing')