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
from intent_engine.core.ib_model import IntentModel

logger = logging.getLogger(__name__)

class nemo():
    """
    This class works as a library for the Intent Engine. The structure is 
    defined in such way that the Intent Engine is capable of parse a
    NEMO deployment intent. The principal functionality is to translate a 
    general NEMO deployment intent to an atomic intent. This atomic
    intent will be processed by its own library. 

    Functions: 
        -
    
    Attributes:
        - Module name
        - isILU: this library refer to other libraries to create
                an atomic intent. This means that when an intent is 
                process as part of a nemo deployment the classification 
                will return a more specific tecnology (library or libraries) that 
                the intent will process. 
        - executioners: for the moment, a nemo intent is not passed directly to
                        any specific tecnology. 

    Relations: l2sm, (in future versions also vpn, sdnc)
    """
    def __init__(self):
        self.__module_name="nemo"
        self.__isILU=False
        self.__executioners=[]
        self.__parser={}
        self.__checker={}
        self.__interface={}
        self.__functions=["deploy"]
        self.__decision_tree={"cloud_continuum":{
                    "DELIVER":{"K8S_L2_NETWORK":"nemo",
                               "5G_NETWORK_SLICE":"nemo",
                               "L2_VPN":"l2vpn"}
                        }
                    }

    def get_name(self):
        return self.__module_name
    def check_import(self):
        print("NEMO imported")

    def isILU(self):
        return self.__isILU
    
    def generate_subintent(self,intent_model:IntentModel):
        
        intent=intent_model.get_intent()
        logger.debug("Generating NEMO subintent...")
        intent_dict=intent.dict(exclude_defaults=True)
        intent_expectations=[]
        subintent={}

        for i,exp in enumerate(intent.intentExpectations):
            if exp.expectationVerb == 'DELIVER':
                # Check which adaptor
                logger.debug("Deliver case NEMO subintent %s", exp.expectationObject.objectType)
                if exp.expectationObject.objectType =='5G_NETWORK_SLICE':
                    logger.debug("5g_slice case NEMO subintent")
                    intent_dict['intentExpectations'][i]['expectationObject']['objectType']='5G_SLICE_FLOW'
                    intent_dict['intentExpectations'][i]['expectationVerb']='CREATE'
                    intent_expectations.append(intent_dict['intentExpectations'][i])
                
                if exp.expectationObject.objectType =='K8S_L2_NETWORK':
                    logger.debug("l2sm_network case NEMO subintent")
                    intent_dict['intentExpectations'][i]['expectationObject']['objectType']='L2SM_NETWORK'
                    intent_expectations.append(intent_dict['intentExpectations'][i])

        subintent['Intent']={'intentExpectations':intent_expectations,
                                    'id':intent_dict['id'],
                                    'userLabel':'cloud_continuum',
                                    'intentPriority':intent_dict['intentPriority']}
        logger.debug("NEMO subintent: ")
        pprint(subintent)
        return [IntentModel(subintent)]

    def checker(self,intent:IntentModel):
        print("checker intent get name: ",intent.get_context().get_name())
        if intent.get_context().get_name() == "nemo_deployment":
            print("is NEMO")
            # return self.__classifier tree para que la decisón esté fuera
            return True
        return False
    
    def executioner(self):
        
        return
    # def classifier(self,intent : IB_object):
    #     ill=[]
    #     self.find_in_tree(intent.get_keywords(),self.__classifier,ill)
    #     sub_intents=[intent]
    #     return sub_intents,ill
    
    def get_decision_tree(self):
        return self.__decision_tree