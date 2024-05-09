import logging
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)

class abstract_library(ABC):
    """
    Abstract class created as 
    """
    def __init__(self,module_name,isILU,decision_tree,params):
        self.__module_name=module_name
        self.__isILU=isILU
        self.__decision_tree=decision_tree
        self.__params=params
        pass
    
    def get_decision_tree(self):
        """
        How to construct a tree:
        1. Leaves (references to other libraries) are lists
        2. exp->ctx->target ? TODO
        """
        return self.__decision_tree
    
    def get_name(self):
        return self.__module_name
    
    def check_import(self):
        print(f"{self.__module_name} imported")
    
    def isILU(self):
        """
        Return true if this library is able to procces atomic
        intetns.
        """
        return self.__isILU
    
    @abstractmethod
    def translator(self)-> tuple[list , str]:
        pass