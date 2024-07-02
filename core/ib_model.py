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
from typing import List
import logging
from intent_engine.core import IntentNrm
logger = logging.getLogger(__name__)

class IntentModel():
    def __init__(self,intent_dict: dict = {}) -> None:
        self.__intent : IntentNrm.IntentMncc = IntentNrm.IntentMncc(**intent_dict['Intent'])
        logger.debug("Schema Type: %s",type(self.__intent.intentExpectations[0]))
    
    def __str__(self):
        return str(self.__intent)
    
    def get_dict(self):
        return self.__intent.dict(exclude_defaults=True)
    
    def get_keywords(self):
        
        keywords=[]
        keywords.append(self.__intent.userLabel)
        # intent_expectations: List[IntentNrm.IntentExpectation] = self.__intent.intentExpectations
        for exp in iter(self.__intent.intentExpectations):
            keywords.append(exp.expectationVerb.value)
            keywords.append(exp.expectationObject.objectType.value)
            # keywords.extend([trg.targetName for trg in exp.expectationTargets])

        return keywords

    def get_intent(self):
        return self.__intent
    