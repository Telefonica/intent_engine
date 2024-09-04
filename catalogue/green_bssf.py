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
from intent_engine.core.ib_model import IntentModel

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
                    "Slice_Energy_Saving":{
                        "ENSURE":"green_bssf"
                        } #mirar esto
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
        subintent=IntentModel()
        ilu=""
        subintent.set_name(intent.get_name())
        subintent.set_context(intent.get_context())
        for exp in intent.get_expectations():
            match exp.get_verb():
                case "ensure":
                    # Maybe ilu in not needed as next
                    # library will detect the intent as own
                    logger.debug("Generating sub intent green->ENIF...")
                    ilu="enif_slice"
                    # create new object from existing intent
                    logger.debug("Context to generate new: ")
                    ctxs=[ctx.get_dict() for ctx in exp.get_object().get_contexts()]
                    logger.debug("ctxs: %s",ctxs)
                    new_obj=Object_expectation('slice_intent_5ginduce','6Green_slice_1',ctxs)
                    # change type so ENIF library understands
                    exp.set_object(new_obj)
                    logger.debug("new expectation for subint: %s",exp)
                    subintent.set_expectations([exp])
                    logger.debug("generated subintent green->ENIF:%s",subintent)
        return subintent
    
    def translator(self,subintent : IntentModel)-> tuple[list , str]:
        exec_params=[]
        self.__params={
            "Constrain type":"green"
        }
        logger.info("Translating green_bssf...")
        logger.debug("debug green_bssf...")
        
        return [self.__params,exec_params],"sysout"