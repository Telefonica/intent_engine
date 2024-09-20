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
from abc import ABC, abstractmethod

from intent_engine.core.ib_model import IntentModel

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
        Functions:

        Attributes:
        
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
    def translator(self,subintent : IntentModel)-> tuple[list , str]:
        pass

    @abstractmethod
    def generate_subintent(self,subintent : IntentModel) -> list[IntentModel]:
        pass