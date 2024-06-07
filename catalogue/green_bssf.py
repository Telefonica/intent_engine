# © 2024 Telefónica Innovación Digital

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
from intent_engine.catalogue.abstract_library import abstract_library
from intent_engine.core.ib_object import IB_object

logger = logging.getLogger(__name__)

class green_bssf(abstract_library):
    """
    Library for 6Green project
    """
    def __init__(self):
        params={}
        decision_tree={
           "green" : {
               "intent_id":{
                   "slice_intent_5ginduce":{
                       "deploy": "enif_slice"},
                    "Slice_Energy_Saving":"green_things", #mirar esto
                    }
                }
        }
        super().__init__(module_name="slice_5g",isILU=False,params=params,decision_tree=decision_tree)
        self.__params=params
    

    def generate_subintent(self,intent:IB_object) -> IB_object:
        """
        Return sub intents of a slice in a green context.
        """

        return intent