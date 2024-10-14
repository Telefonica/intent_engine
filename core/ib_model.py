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
from devtools import pprint
from fastapi.encoders import jsonable_encoder
from intent_engine.core import IntentNrm
from pydantic import ValidationError
logger = logging.getLogger(__name__)

class IntentModel():
    def __init__(self,intent_dict: dict = {}) -> None:
        try:
            # pprint(intent_dict)
            self.__intent : IntentNrm.IntentNrmg = IntentNrm.IntentNrmg(**intent_dict).Intent
            logger.debug("Schema Type Expectation: %s",type(self.__intent.intentExpectations[0]))
        except ValidationError as exc:
            logger.warning("Assurance error %s", exc)
            raise
        
    
    def __str__(self):
        return str(self.__intent)
    
    def get_dict(self):
        return self.__intent.dict(exclude_defaults=True)
    
    def get_keywords(self):
        
        keywords=[]
        keywords.append(self.__intent.userLabel)
        # intent_expectations: List[IntentNrm.IntentExpectation] = self.__intent.intentExpectations
        for exp in iter(self.__intent.intentExpectations):
            keywords.append(exp.expectationVerb)
            keywords.append(exp.expectationObject.objectType)
            # keywords.extend([trg.targetName for trg in exp.expectationTargets])

        return keywords

    def get_intent(self):
        return self.__intent
    def set_intent(self,intent):
        self.__intent=intent

def jsonable_model_encoder(intent : IntentModel | dict) -> dict:
    """
    Given a model or a dict with enum values as type enum class, 
    returns the same model or dict with all literal values.
    This enables the posibility to parse againt the model as IntentMncc
    without attributes as custom classes.
    """
    return jsonable_encoder(intent)