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
# Deals with common parts, i.e. events and translators.
#
# ------------------------------------------------------------------------------
#


# 0. Imports ===================================================================

# general

# internal
from ..events import event as event
from ..translators import storage as storage
from ..translators import timed_storage as timed_storage
from ..util import base_optimisation as base_optimisation

# 1. Global vars ===============================================================


# 1.1 Classes ------------------------------------------------------------------
class CommonParts(base_optimisation.BaseMOEA):
    
    def __init__(self):

        base_optimisation.BaseMOEA.__init__(self)

        self.events         = []
        self.storages       = []
        self.timed_storages = []
        self.time_series    = []


    def load_common(self, data):
        """
        Loads the common stuff across elements (events & translators).

        Inputs:

        data
            Object holding the data.
        """

        if ('Events' in data):
            for item in data['Events']:
                obj = event.IOEvent()
                obj.load(item)
                self.events.append(obj)

        if ('Storages' in data):
            for item in data['Storages']:
                obj = storage.IOStorage()
                obj.load(item)
                self.storages.append(obj)

        if ('Timed_Storages' in data):
            for item in data['Timed_Storages']:
                obj = timed_storage.IOTimedStorage()
                obj.load(item)
                self.timed_storages.append(obj)

        if ('Time_Series' in data):
            print('common_parts.load_common: Error:')
            print('Time Series not yet supported')
            exit(255)

            # for item in data['Timed_Storages']:
            #     obj = time_series.IOTimeSeries()
            #     obj.load(item)
            #     self.time_series.append(obj)

    def check(self):
        print("alternative.check: Not yet implemented")
        exit(255)


    def write_common(self, f):

        if (len(self.events) > 0):
            f.write('\n\nEvents:')
            for occurance in self.events:
                occurance.write(f)

        if (len(self.storages) > 0):
            f.write('\n\nStorages:')
            for depot in self.storages:
                depot.write(f)

        if (len(self.timed_storages) > 0):
            f.write('\n\nTimed_Storages:')
            for timed_depot in self.timed_storages:
                timed_depot.write(f)

        f.write('')


    def gen_common_vectors(self,
                           vec_debug: bool,
                           timeseries_adjustment: bool = True):

        vec_var      = []
        vec_boundary = []
        vec_epsilon  = []

        if (len(self.events) > 0):
            for e in self.events:
                triple = e.moea_gen_vectors(vec_debug, timeseries_adjustment)
                vec_var      += triple[0]
                vec_boundary += triple[1]
                vec_epsilon  += triple[2]

        if (len(self.storages) > 0):
            for depot in self.storages:
                triple = depot.moea_gen_vectors(vec_debug)
                vec_var      += triple[0]
                vec_boundary += triple[1]
                vec_epsilon  += triple[2]

        if (len(self.timed_storages) > 0):
            for timed_depot in self.timed_storages:
                triple = timed_depot.moea_gen_vectors(vec_debug)
                vec_var += triple[0]
                vec_boundary += triple[1]
                vec_epsilon += triple[2]

        return vec_var, vec_boundary, vec_epsilon


    def common_insert_vector(self,
                             vec: list,
                             timeseries_adjustment: bool = True):

        num = 0  # number of data places already inserted

        if (len(self.events) > 0):
            for occurance in self.events:
                num += occurance.moea_insert_vector(
                    vec[num:num + event.get_data_extend()],
                    timeseries_adjustment)

        if (len(self.storages) > 0):
            for depot in self.storages:
                num += depot.moea_insert_vector(
                    vec[num:num + storage.get_data_extend()])

        if (len(self.timed_storages) > 0):
            for timed_depot in self.timed_storages:
                num += timed_depot.moea_insert_vector(
                    vec[num:num + timed_storage.get_data_extend()])

        return num


# 2. Functions =================================================================

# 3. Main Exec =================================================================
if __name__ == '__main__':
    print('Testing')