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
           },
           "green_nest" : {
                "NEST":{
                      "ENSURE":"green_bssf",
                      "DELIVER":"green_bssf"
                 }
              }
        }
        super().__init__(module_name="green_bssf",isILU=False,params=params,decision_tree=decision_tree)
        self.__params=params
    

    def generate_subintent(self,intent_model:IntentModel) -> list[IntentModel]:
        """
        Return sub intents of a slice in a green context.
        Also return library to porcess the subintent, as green_bssf is not ilu,
        this means have no final tranlation with a technology.
        """
        intent=intent_model.get_intent()
        logger.debug("Generating Green subintent...")
        intent_dict=intent.dict(exclude_defaults=True)
        green_expectations=[]
        slice_expectations=[]
        subintent_green={}
        subintent_slice={}
        if intent.userLabel == 'green_nest':
            nest_expectations=[]
            logger.debug("Green NEST subintent")
            for i,exp in enumerate(intent.intentExpectations):
                if exp.expectationVerb == 'DELIVER':
                    if exp.expectationObject.objectType=='NEST':
                        for obj_ctx in exp.expectationObject.objectContexts:
                            logger.debug("look for NEST type: %s",obj_ctx)
                            if obj_ctx.contextAttribute=='ServiceType':
                                if obj_ctx.contextValueRange=='eMBB':
                                    intent_dict['intentExpectations'][i]['expectationObject']['objectType']='NEST_eMBB'
                                    nest_expectations.append(intent_dict['intentExpectations'][i])
                                    logger.debug("NEST for eMBB")
            

            subintent_green['Intent']={'intentExpectations':nest_expectations,
                                    'id':intent_dict['id'],
                                        'userLabel':'enif_slice',
                                        'intentPriority':intent_dict['intentPriority']}
        
            store_graph_in_graphdb(create_intent_graph(intent_model), "http://192.168.159.253:7200", "6green")
            get_intent_from_userLabel("green_nest","http://192.168.159.253:7200", "6green")
            return [IntentModel(subintent_green)]

        else:
            for i,exp in enumerate(intent.intentExpectations):
                if exp.expectationVerb == 'ENSURE':
                    
                    intent_dict['intentExpectations'][i]['expectationObject']['objectType']='Slice_Energy_Saving'
                    green_expectations.append(intent_dict['intentExpectations'][i])
                    # pprint(intent_dict)
                    

                if exp.expectationVerb == 'DELIVER':

                    intent_dict['intentExpectations'][i]['expectationObject']['objectType']='Slice_5ginduce'
                    slice_expectations.append(intent_dict['intentExpectations'][i])

            # TODO: meter la nbi de TFS como parte del context para el subintent
            subintent_green['Intent']={'intentExpectations':green_expectations,
                                    'id':intent_dict['id'],
                                        'userLabel':'enif_slice',
                                        'intentPriority':intent_dict['intentPriority']}
            # TODO:check intentPriority:  ,observationPeriod: , intentAdminState: ''? maintain?

            subintent_slice['Intent']={'intentExpectations':slice_expectations,
                                    'id':intent_dict['id'],
                                        'userLabel':'enif_slice',
                                        'intentPriority':intent_dict['intentPriority']}
        # logger.debug("Green subintent : %s",subintent)
        # intent_model.set_intent(subintent)
            # store_graph_in_graphdb(create_intent_graph(intent_model), "http://localhost:7200", "6green")
            return [IntentModel(subintent_green),IntentModel(subintent_slice)]
    
    def translator(self,subintent : IntentModel)-> tuple[list , str]:
        exec_params=[]
        self.__params={
            "Constrain type":"green"
        }
        logger.info("Translating green_bssf...")
        logger.debug("debug green_bssf...")
        
        return [self.__params,exec_params],"sysout"