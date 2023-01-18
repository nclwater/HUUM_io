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
# 2019.02.14 - SBerendsen - Initial version
#
# ------------------------------------------------------------------------------
#
# Copyright 2020, Sven Berendsen
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
# Stuff needed for enabling different optimizer.
#
# ------------------------------------------------------------------------------
#
# ToDo
#   - integrate logging framework
#
# ------------------------------------------------------------------------------
#



# 0. Imports ===================================================================

# general

# internal

# 1. Global vars ===============================================================
_epsilon_value = 0.001     # Currently doing single objective optimization - value doesn't matter.


# 1.1 Classes ------------------------------------------------------------------
class BaseMOEA(object):
    # Extensible base class for generating an optimization vector of changeable variables.

    def __init__(self):
        self.__pos_data_extend = None   # length of this elements data part
        self.__vec             = None   # holds the data vector when debugging


    def set_data_extend(self, data_extend):
        self.__pos_data_extend = data_extend


    def get_data_extend(self):
        return self.__pos_data_extend


    def set_vec(self, vec):
        self.__vec = vec


    def get_vec(self):
        return self.__vec
        

    def moea_gen_vectors(self, vec_debug):
        """
        Generates the three vectors needed for MOEA-borg.

        Inputs:

        vec_debug
            Whether the method should save the generated vector for debug purposes.

        Returns:

        vec_var
            List of optimizeable values.
        vec_boundary
            List (same size as vec_var) with tuples of the limits to each variable.
        vec_epsilon
            List of assorted epsilon values (same size as vec_var).
        """
        print('BaseMOEA.moea_gen_vectors: Error')
        print('Not overriden in extending class.')
        exit(255)

        return None, None, None

    
    def moea_insert_vector(self, vec):
        """
        Inserts the changed variable vector back into the data structure.

        Arguments:

        vec
            Vector with the changed values.

        Returns:
            Length of inserted data.
        """
        print('BaseMOEA.moea_insert_vector: Error')
        print('Not overriden in extending class.')
        exit(255)

        num = 0     # number of variables pulled out

        return num


    def moea_check_vec_bounds(self, vec, orig_method):
        """
        Checks whether the given vector is within bounds.

        Arguments:

        vec
            Vector with the changed values.
        """

        flag   = True
        length = len(vec)
        
        if (self.__pos_data_extend > length):
            print(orig_method + '.moea_check_vec_bounds: Error')
            print('The data start point + data length is beyond the vector length.')
            print('pos_extend:', str(self.__pos_data_extend))
            print('Size vec:  ', str(len(vec)))
            flag = False

        if not (flag):
            exit(255)


    def moea_check_vec_extend(self, num, method_name, vec):
        """
        Checks whether the given vector is within bounds.

        Arguments:

        vec
            Vector with the changed values.
        method_name
            Name of method calling this function.
        num
            Number of inserts done within the calling function.
        """

        flag   = False      # if the data has an error
        
        # check for data equivalence
        if not (self.__vec is None):
            if (self.__vec != vec):
                print('\n' + method_name + '.moea_check_vec_extend: Error:')
                print("Given vector and remembered vector doesn't fit")
                print('Remembered:', self.__vec)
                print('Given:     ', vec)
                flag = True


        # check obtained number & extend
        if (num != self.__pos_data_extend):
            print('\n' + method_name + '.moea_check_vec_extend: Error:')
            print("Obtained num and vector length doesn't fit")
            print('Length vec:   ', len(vec))
            print('num:          ', num)
            print('gen_extend:   ', self.__pos_data_extend)
            if not (self.__vec is None):
                print('Generated vec:', self.__vec)
                print('Given vec:    ', vec)
            print('')
            flag = True

        if (flag):
            exit(255)


# 2. Functions =================================================================
def get_epsilon_value():
    return _epsilon_value


# 3. Main Exec =================================================================
if __name__ == '__main__':
    print('Testing')
