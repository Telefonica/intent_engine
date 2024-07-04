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
import json
from typing import List
from schema import Schema, And, Use, Optional, SchemaError
from .ib_model import IntentModel
import jsonpickle
import logging
logger = logging.getLogger(__name__)

class Classifier():
    
    def __init__(self, module_instances) -> None:
        self.__modules=module_instances
        self.__trees=[mod.get_decision_tree()
                    for mod in module_instances]
        self.__ILUs=[ilu.get_name()
                    for ilu in module_instances
                    if ilu.isILU()]

    def find_in_tree(self,keywords,obj,leaves: list):
        if isinstance(obj, dict):
            for key, value in obj.items():
                logger.info("%s : %s",key, value)
                if key in keywords:
                    self.find_in_tree(keywords,value,leaves)
        elif isinstance(obj, list):
            for item in obj:
                self.find_in_tree(keywords,item,leaves)
        else:
            print("is leave :",obj)
            leaves.append(obj)

    def classify(self,intent_model : IntentModel) -> tuple[list[IntentModel],list]:
        """
        When an intent is recived in the intent_core .
        TODO: get intent blueprint to create subintents
        """
        ill=[]
        sub_intents:list[IntentModel]=[]
        translators=[]
        intent=intent_model
        for tree in self.__trees:
            # get all libraries capable of translate the intent
            self.find_in_tree(intent_model.get_keywords(),tree,ill)
        # unique list in case of duplicities
        unique_ill=list(set(ill))
        logger.debug("unique list: %s",unique_ill)
        for ilu in unique_ill:
            # for every unique ill and intent
            logger.debug("new iter subintent module: %s",ilu)
            for module in self.__modules:
                # for every module installed, recognise intent
                if module.get_name() == ilu:
                    # if ill has direct translator to executioner is ilu
                    if module.isILU():
                        # get translator
                        # the subintent is for having the same ordering or some minor checks
                        logger.debug("Module is ilu: %s",module)
                        sub_intent=module.generate_subintent(intent)
                        sub_intents.append(sub_intent)
                        translators.append(module.get_name())
                        logger.debug("translators iteration ILU: %s",translators)
                    else:
                        # this means it has no direct translator
                        # it generates another subintent to be classified by other ill/ilu
                        # this loops until ilu
                        logger.debug("reclassify...")
                        sub_intent=module.generate_subintent(intent)
                        # TODO: classify for each subintent?
                        logger.debug("sub_intent iteration noILU: %s",sub_intent)
                        sub_intent,sub_ilu=self.classify(sub_intent)
                        translators.extend(sub_ilu)
                        sub_intents.extend(sub_intent)
                        logger.debug("translators iteration noILU: %s",translators)
                    
        # if translators:
            # logger.debug("Translators: %s || Subintent: %s",translators[:],sub_intent)

        # Necesito que sea uniq ill, pero cada ill su subintent?
        # problema si un ill tiene dos subintents?
        # return list(set(sub_intents)),list(set(ill))
        return sub_intents,translators
    
    def check(self,conf_schema, conf):
        try:
            conf_schema.validate(conf)
            return True
        except SchemaError:
            return False
    
    def filter(self, intent :IntentModel):

        return intent