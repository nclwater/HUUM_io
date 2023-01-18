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
# 2019.12.11 - SBerendsen - Initial version
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
# Agent data object.
#
# ------------------------------------------------------------------------------
#

# 0. Imports ===================================================================

# general
import os
import ruamel.yaml as YAML

# internal
from .elements import lifecycle as lifecycle
from .elements import usage_habit as usage_habit
from .elements import usage_template as usage_template
from .elements import common_parts as common_parts

# 1. Global vars ===============================================================


# 1.1 Classes ------------------------------------------------------------------
class IOAgent(common_parts.CommonParts
              ):  # class to hold both settings and the model data itself

    def __init__(self):

        super().__init__()

        self.id = None  # obvious
        self.lifecycle = []  # list of lifecycle objects
        self.usage_habits = []  # list of set usage habits
        self.habit_templates = []  # list of situational usage habits

    def load(self, fn, dir_root, zfile=None):
        """
        loads the holdings file and (optionally) it's consumer_unit constituents.

        Inputs:
        fn
            filename to load
        dir_root
            model data structure root directory
        zfile
            zipfile object, if loading from zip
        """

        # sanity check
        if zfile is None:
            exists = os.path.isfile(dir_root + fn)
            if not exists:
                print('')
                print('\nHUUM agent file ' + dir_root + fn + ' does not exist')
                print('Working dir: ' + str(os.getcwd()))
                exit(255)

            # get data
            f = open(dir_root + fn, 'r')
            agent_data = YAML.YAML(typ='safe', pure=True).load(f)
            f.close()

        else:
            with zfile.open(f'{dir_root}{fn}') as f_obj:
                agent_data = YAML.YAML(typ='safe', pure=True).load(f_obj)

        self.id = agent_data['Name']

        # get lifecycle
        list_lifecycle = agent_data['Lifecycle']

        for item in list_lifecycle:
            lifecycle_entry = lifecycle.IOLifeCycle()
            lifecycle_entry.load(item)
            self.lifecycle.append(lifecycle_entry)

        # get set usage habits
        if ('Usage_Habits' in agent_data):
            habits = agent_data['Usage_Habits']
            if not (habits is None):
                for habit in habits:
                    usage = usage_habit.IOUsageHabit()
                    usage.load(habit)
                    self.usage_habits.append(usage)

            else:
                self.usage_habits = []

        # get situational usage habits
        if ('Usage_Templates' in agent_data):
            habits = agent_data['Usage_Templates']
            if not (habits is None):
                for habit in habits:
                    usage = usage_template.IOUsageTemplate()
                    usage.load(habit)
                    self.habit_templates.append(usage)

            else:
                self.habit_templates = []

        # load common stuff
        self.load_common(agent_data)

        return

    def check(self):
        print("holding.check: Not yet implemented")
        exit(255)

    def write(self, dir_root, dir_file):

        # assure that the output directory exists
        dir_local = os.path.join(dir_root, dir_file)
        if not os.path.exists(dir_local):
            os.makedirs(dir_local)

        # write file
        f = open(os.path.join(dir_local, self.id + '.yaml'), 'w')

        # write header
        f.write("%YAML 1.2\n---\n")

        f.write('\nName: ' + self.id + '\n')
        f.write('\nLifecycle:')
        for lc in self.lifecycle:
            lc.write(f)

        if (len(self.usage_habits) > 0):
            f.write('\n\nUsage_Habits:')
            for habit in self.usage_habits:
                habit.write(f)

        if (len(self.habit_templates) > 0):
            f.write('\n\nUsage_Templates:')
            for habit in self.habit_templates:
                habit.write(f)

        # Common Data
        self.write_common(f)

        f.write('\n')

        f.close()

    def moea_gen_vectors(self, vec_debug):

        vec_var = []
        vec_boundary = []
        vec_epsilon = []

        # nothing to do for itself

        # get the holdings done
        for lf in self.lifecycle:
            triple = lf.moea_gen_vectors(vec_debug)
            vec_var += triple[0]
            vec_boundary += triple[1]
            vec_epsilon += triple[2]

        # get the holdings done
        for uh in self.usage_habits:
            triple = uh.moea_gen_vectors(vec_debug)
            vec_var += triple[0]
            vec_boundary += triple[1]
            vec_epsilon += triple[2]

        # get the holdings done
        for ht in self.habit_templates:
            triple = ht.moea_gen_vectors(vec_debug)
            vec_var += triple[0]
            vec_boundary += triple[1]
            vec_epsilon += triple[2]

        # do the common items
        triple = self.gen_common_vectors(vec_debug)
        vec_var += triple[0]
        vec_boundary += triple[1]
        vec_epsilon += triple[2]

        # set local data
        self.set_data_extend(len(vec_var))
        if (vec_debug):
            self.set_vec(vec_var)

        return vec_var, vec_boundary, vec_epsilon

    def moea_insert_vector(self, vec):

        num = 0  # number of data places already inserted

        # sanity bounds check
        self.moea_check_vec_bounds(vec, 'Agent')

        # insert data - nothing to do for self

        # insert data - lifecycle
        for lc in self.lifecycle:
            num += lc.moea_insert_vector(vec[num:num + lc.get_data_extend()])

        # insert data - usage habits
        for uh in self.usage_habits:
            num += uh.moea_insert_vector(vec[num:num + uh.get_data_extend()])

        # insert data - habit templates
        for ut in self.habit_templates:
            num += ut.moea_insert_vector(vec[num:num + ut.get_data_extend()])

        # insert data - common items
        num += self.common_insert_vector(vec[num:self.get_data_extend()])

        # sanity_check
        self.moea_check_vec_extend(num, 'agent', vec)

        return num


# 2. Functions =================================================================

# 3. Main Exec =================================================================
if __name__ == '__main__':
    print('Testing')