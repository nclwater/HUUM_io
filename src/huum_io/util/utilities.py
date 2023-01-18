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
# Useful methods.
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

# 1.1 Classes ------------------------------------------------------------------


# 2. Functions =================================================================
def safe_get_dict_item(dict, item, source):
    """
    Method to safely load an item from a dictionary with an error msg if not present.

    Inputs:

    dict
        (dictionary) Dictionary to load from.
    item
        (string) Name of requested dictionary item.
    source
        (string) Source function calling this one (for error msg - get logging working!).
    """

    # check for occurrence
    if not (item in dict):
        print('\nutilities.safe_get_dict_item: Error:')
        print('Required keyword ' + item + ' not found in given dictionary.')
        print('Called from ' + source)
        print('Source object:')
        print(dict)
        exit(255)

    return dict[item]


def get_dict_item_if_exists(dict, item: str, default: str):
    """
    Method to load item from dictionary if that item key exists. Otherwise returns
    the given default.

    Inputs:

    dict
        (dictionary) Dictionary to load from.
    item
        (string) Name of requested dictionary item.
    default
        (string) Default value if not present
    """

    # check for occurrence
    if (item in dict):
        return dict[item]
    
    else:
        return default


# 3. Main Exec =================================================================
if __name__ == '__main__':
    print('Testing')
