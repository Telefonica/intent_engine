import json
from schema import Schema, And, Use, Optional, SchemaError
from .ib_object import IB_object
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

    def classify(self,intent : IB_object):
        """
        When an intent is recived in the intent_core .
        TODO: get intent blueprint to create subintents
        """
        ill=[]
        sub_intents=[]
        for tree in self.__trees:
            self.find_in_tree(intent.get_keywords(),tree,ill)
            sub_intents.append(intent)
            logger.info("Ill: %s || Subintent: %s",ill[:],intent)
        # Necesito que sea uniq ill, pero cada ill su subintent?
        # problema si un ill tiene dos subintents? 
        return list(set(sub_intents)),list(set(ill))
    
    def check(self,conf_schema, conf):
        try:
            conf_schema.validate(conf)
            return True
        except SchemaError:
            return False
    
    def filter(self, intent :IB_object):

        return intent