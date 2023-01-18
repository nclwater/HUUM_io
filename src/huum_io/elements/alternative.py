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
# Alternative objects.
#
# ------------------------------------------------------------------------------
#


# 0. Imports ===================================================================

# general

# internal
from ..elements import condition_expression as condition_expression
from ..util import utilities as util

# 1. Global vars ===============================================================


# 1.1 Classes ------------------------------------------------------------------
class IOAlternative(object):
    def __init__(self):

        self.target    = None
        self.condition = None


    def load(self, item):
        """
        Loads the alternative info from the given object.

        Inputs:

        item
            Object holding the alternative info entry.
        """
        self.target    = util.safe_get_dict_item(item, "Target",
                                                 'Alternative.load').lower()

        string         = util.safe_get_dict_item(item, "Condition_Expression",
                                                 'Alternative.load').lower()
        self.condition = condition_expression.IOConditionExpression()
        self.condition.load(string)

        return


    def check(self):
        print("alternative.check: Not yet implemented")
        exit(255)


    def write(self, f):
        f.write('\n        - alternate:')
        self.condition.write(f)
        f.write('\n          Target:               ' + self.target + '\n')


# 2. Functions =================================================================

# 3. Main Exec =================================================================
if __name__ == '__main__':
    print('Testing')