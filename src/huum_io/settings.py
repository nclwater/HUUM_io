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
# 2019.12.07 - SBerendsen - Initial version
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
# Holds any and all settings data.
#
# ------------------------------------------------------------------------------
#

# 0. Imports ===================================================================

# general
import logging
import os
import ruamel.yaml as YAML

# internal
from .util import utilities as util

# 1. Global vars ===============================================================
mod_logger = logging.getLogger(__name__)


# 1.1 Classes ------------------------------------------------------------------
class IOSettings(object
                 ):  # class  to hold both settings and the model data itself

    def __init__(self):

        self.title = None

        self.fn_model = None
        self.dir_modelRoot = None
        self.dir_output = None

        self.time_start = None
        self.time_end = None

        self.t_step_min = None
        self.t_step_max = None

        # logging stuff
        self.headless = False  # (runtime only) Switch for running HUUM headless. NO IO, code only!
        self.logging_type = "complex"  # default type of logging.
        self.log_as_single = False  # Switch wether the output should be single file per info-type.

        self.log_events = False
        self.log_passedTime = False
        self.log_storage = False
        self.log_appliances = False
        self.log_activation = False
        self.log_blocking = False
        self.log_lifecycle = False
        self.log_wants = False
        self.log_probability = False
        self.log_TS_outputs = True

        self.seed = None

    @classmethod
    def load(cls, fn):

        # sanity check
        exists = os.path.isfile(fn)
        if not exists:
            mod_logger.critical('HUUM model settings file ' + fn +
                                ' does not exist')
            exit(255)

        # get data
        f = open(fn, 'r')
        cls = IOSettings.from_fileobject(f)
        f.close()

        return cls

    @classmethod
    def from_fileobject(cls, f_obj):

        settings = YAML.YAML(typ='safe', pure=True).load(f_obj)

        cls = IOSettings()

        # transfer data
        if ('Title' in settings):
            cls.title = settings['Title']
        cls.fn_model = settings['File_Model']
        cls.dir_modelRoot = settings['Dir_ModelRoot']
        cls.dir_output = settings['Dir_Output']
        cls.time_start = settings['Time_Start']
        cls.time_end = settings['Time_End']
        cls.t_step_min = settings['t_step_min']
        cls.t_step_max = settings['t_step_max']
        if ('Seed' in settings):
            cls.seed = settings['Seed']

        # logging & output stuff
        cls.logging_type = util.get_dict_item_if_exists(
            settings, item="logging_Type", default=cls.logging_type)
        cls.log_as_single = util.get_dict_item_if_exists(
            settings, item="log_as_Single", default=cls.log_as_single)
        cls.log_events = util.get_dict_item_if_exists(settings,
                                                      item="log_Events",
                                                      default=cls.log_events)
        cls.log_passedTime = util.get_dict_item_if_exists(
            settings, item="log_PassedTime", default=cls.log_passedTime)
        cls.log_storage = util.get_dict_item_if_exists(settings,
                                                       item="log_Storage",
                                                       default=cls.log_storage)
        cls.log_appliances = util.get_dict_item_if_exists(
            settings, item="log_Appliances", default=cls.log_appliances)
        cls.log_activation = util.get_dict_item_if_exists(
            settings, item="log_Activation", default=cls.log_activation)
        cls.log_blocking = util.get_dict_item_if_exists(
            settings, item="log_Blocking", default=cls.log_blocking)
        cls.log_lifecycle = util.get_dict_item_if_exists(
            settings, item="log_Lifecycle", default=cls.log_lifecycle)
        cls.log_wants = util.get_dict_item_if_exists(settings,
                                                     item="log_Wants",
                                                     default=cls.log_wants)
        cls.log_probability = util.get_dict_item_if_exists(
            settings, item="log_Probability", default=cls.log_probability)
        cls.log_TS_outputs = util.get_dict_item_if_exists(
            settings, item="log_TS_Outputs", default=cls.log_TS_outputs)

        return cls

    def check(self):
        mod_logger.critical('settings.check: Not yet implemented')
        exit(255)

    def write(self, filename):

        # filename check
        directory = os.path.dirname(filename)
        if not os.path.exists(directory):
            os.makedirs(directory)

        f = open(filename, 'w')

        # self.check()

        # write header
        f.write("%YAML 1.2\n---\n")

        # title stuff
        if not (self.title is None):
            f.write("\nTitle:           " + self.title)

        # directory stuff
        f.write('\n\n# File and Folder Settings')
        f.write('\nFile_Model:      ' + self.fn_model)
        f.write('\nDir_ModelRoot:   ' + self.dir_modelRoot)
        f.write('\nDir_Output:      ' + self.dir_output)

        # time stuff
        f.write('\n\n# Date and Time related Settings')
        f.write('\nTime_Start:      ' + self.time_start)
        f.write('\nTime_End:        ' + self.time_end)
        f.write('\nt_step_min:      ' + str(self.t_step_min))
        f.write('\nt_step_max:      ' + str(self.t_step_max))

        # time stuff
        f.write('\n\n# Logging')
        f.write("\nlog_as_Single:   " + str(self.log_as_single))
        f.write("\nlogging_Type:    " + str(self.logging_type))
        f.write("\nlog_Events:      " + str(self.log_events))
        f.write("\nlog_PassedTime:  " + str(self.log_passedTime))
        f.write("\nlog_Storage:     " + str(self.log_storage))
        f.write("\nlog_Appliances:  " + str(self.log_appliances))
        f.write("\nlog_Activation:  " + str(self.log_activation))
        f.write("\nlog_Blocking:    " + str(self.log_blocking))
        f.write("\nlog_Lifecycle:   " + str(self.log_lifecycle))
        f.write("\nlog_Wants:       " + str(self.log_wants))
        f.write("\nlog_Probability: " + str(self.log_probability))
        f.write("\nlog_TS_Outputs:  " + str(self.log_TS_outputs))

        # anything else
        f.write('\n\n# Misc Settings')
        if not (self.seed is None):
            f.write('\nSeed:            ' + self.seed)

        f.close()


# 2. Functions =================================================================

# 3. Main Exec =================================================================
if __name__ == '__main__':
    print('Testing wrong')
