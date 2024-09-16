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

from devtools import pprint
from pydantic import ValidationError
from intent_engine.catalogue.abstract_library import abstract_library
from intent_engine.core.ib_model import IntentModel, jsonable_model_encoder
from intent_engine.core import IntentNrm

logger = logging.getLogger(__name__)

class green_bssf(abstract_library):
    """
    Library for 6Green project
    """
    def __init__(self):
        params={}
        decision_tree={
           "green" : {
               "Slice_Energy_Saving":{
                    "ENSURE":"green_bssf",
                    "DELIVER":"green_bssf"
                },
                "Slice_5ginduce":{
                    "ENSURE":"green_bssf",
                    "DELIVER":"green_bssf"
                }
           }
        }
        super().__init__(module_name="green_bssf",isILU=False,params=params,decision_tree=decision_tree)
        self.__params=params
    

    def generate_subintent(self,intent:IntentModel) -> IntentModel:
        """
        Return sub intents of a slice in a green context.
        Also return library to porcess the subintent, as green_bssf is not ilu,
        this means have no final tranlation with a technology.
        """
        # subintent = intent.get_intent()
        subintents=[]
        logger.info("Generating subintent green_bssf...")
        logger.debug("debug green_bssf...")
        green_expectations=[]
        slice_expectations=[]
        green_expectation={}
        slice_expectation={}
        try:
            subintent=IntentNrm.IntentBssf(**(intent.get_dict()))
        except ValidationError as exc:
            logger.warning("Assurance error for IntentBssf:  %s", exc)
            return
        # separate green expectations from enif 5gslice
        # reclassify in such a way that enif understands
        for i,exp in enumerate(subintent.intentExpectations):
            if exp.expectationVerb.value == 'ENSURE':
                intent_dict=subintent.dict(exclude_defaults=True)
                green_expectation=intent_dict['intentExpectations'][i]
                green_expectations.append(green_expectation)

            if exp.expectationVerb.value == 'DELIVER':
                intent_dict=subintent.dict(exclude_defaults=True)
                slice_expectation=intent_dict['intentExpectations'][i]
                slice_expectations.append(slice_expectation)

        # join all the expectations
        slice_expectations={
                'Intent':
                    {'id':intent_dict['id'],
                     'userLabel':intent_dict['userLabel'],
                    'intentContexts': intent_dict['intentContexts'],
                    'intentExpectations': slice_expectations}
                }
        green_expectations={
            'Intent':
                    {'id':intent_dict['id'],
                     'userLabel':intent_dict['userLabel'],
                    'intentContexts': intent_dict['intentContexts'],
                    'intentExpectations': green_expectations}
                }
        # TODO: what to do with   intentPriority: 1
                                # observationPeriod: 60
                                # intentAdminState: 'ACTIVATED'
        # keep everithing except for the exp and ctx
        return [IntentModel(slice_expectations),
                IntentModel(green_expectations)]
    
    def translator(self,subintent : IntentModel)-> tuple[list , str]:
        exec_params=[]
        self.__params={
            "Constrain type":"green"
        }
        logger.info("Translating green_bssf...")
        logger.debug("debug green_bssf...")
        
        return [self.__params,exec_params],"sysout"