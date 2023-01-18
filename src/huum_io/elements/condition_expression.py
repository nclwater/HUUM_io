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
# 2019.01.22 - SBerendsen - Initial version
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
# Condition Expressions objects.
#
# ------------------------------------------------------------------------------
#


# 0. Imports ===================================================================

# general

# internal

# 1. Global vars ===============================================================


# 1.1 Classes ------------------------------------------------------------------
class IOConditionExpression(object):

    def __init__(self):

        self.what  = None  # what is being compared
        self.type  = None  # how it is being compared
        self.value = None  # what it is compared to

    def load(self, expression):
        """
        Reads and saves the expression from a string.

        Inputs:

        expression
            To be loaded expression
        """

        string = expression.lower()
        parts  = string.split(' ')

        if (len(parts) != 3):
            print('ConditionExpression.load: Error:')
            print('Expression needs three parts, but has', len(parts))
            exit('')

        self.what  = parts[0]
        self.type  = parts[1]
        self.value = parts[2]

        return


    def check(self):
        print("condition_expression.check: Not yet implemented")
        exit(255)


    def write(self, f):
        f.write('\n          Condition_Expression: ' + self.what + ' ' +
                self.type + ' ' + self.value)


# 2. Functions =================================================================


# 3. Main Exec =================================================================
if __name__ == '__main__':
    print('Testing')
