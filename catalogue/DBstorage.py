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
from typing import List

from devtools import pprint
from intent_engine.catalogue.abstract_library import abstract_library
from intent_engine.core import IntentNrm
from intent_engine.core.ib_model import IntentModel, jsonable_model_encoder
from intent_engine.core.database_utils import create_intent_graph, get_intent_from_userLabel, store_graph_in_graphdb

logger = logging.getLogger(__name__)

class DBstorage(abstract_library):
    """
    Library for 6Green project
    """
    def __init__(self):
        params={
        }
        decision_tree={
        }
        super().__init__(module_name="DBstorage",isILU=False,params=params,decision_tree=decision_tree)
        self.__params=params
    

    def generate_subintent(self,intent_model:IntentModel) -> list[IntentModel]:
        """
        """
        subintent=intent_model
        logger.debug("Generate subintent model type: %s",type(subintent))
        return subintent
    
    def translator(self,subintent : IntentModel)-> tuple[list , str]:
        """
        Store the intent directly in the database
        """
        logger.debug("Intent model type: %s",type(subintent))
        intent = subintent.get_intent()
        params={
            "DBfunction":"store_graph",
            "endpoint_url":"http://192.168.159.253:7200",
            "repository":"6green"
        }
        logger.info("Translating DBstorage...")
        logger.debug("debug DBstorage...")
        
        return [subintent,params],"DBconnector"