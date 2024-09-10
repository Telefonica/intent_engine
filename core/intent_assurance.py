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
from typing import List, get_args
import logging
from fastapi.encoders import jsonable_encoder
from intent_engine.core import IntentNrm
from intent_engine.core.ib_model import IntentModel
from pydantic import ValidationError
logger = logging.getLogger(__name__)

class IntentAssurance():
    def __init__(self):
        self.__load_models=1
        self.loop=True

    def assure_intent(self, subintent :IntentModel):
        logger.debug("Assurance possible expectations %s %s",
                     IntentNrm.IntentMncc.__annotations__['intentExpectations'],
                     IntentNrm.IntentBssf.__annotations__['intentExpectations'])
        # logger.debug("Assurance possible fields %s",
        #              IntentNrm.IntentMncc.__fields__['intentExpectations'].type_)
        intent = subintent.get_intent()
        intent_dict = subintent.get_dict()
        min_error=[]
        schema_type=[]
        # For all different main componets, this could be programed 
        # schema_type.extend(get_args(IntentNrm.IntentMncc.__fields__['intentExpectations'].type_))
        # schema_type.extend(get_args(IntentNrm.IntentBssf.__fields__['intentExpectations'].type_))
        # logger.debug("intent.expectaions: %s",intent.intentExpectations)
        logger.debug("Fields in IntentNrmg %s",get_args(IntentNrm.IntentNrmg.__fields__['Intent'].type_))
        schema_type=get_args(IntentNrm.IntentNrmg.__fields__['Intent'].type_)
        # for exp in intent.intentExpectations:
        for schema in schema_type:
            try:
                exp_class=schema(**(intent_dict))
            except ValidationError as exc:
                logger.warning("Assurance error for %s",schema)
                logger.warning("Number of errors %s", len(exc.errors()))
                if len(min_error)==0:
                    min_error=exc.errors()
                elif len(exc.errors()) < len(min_error):
                    min_error=exc.errors()
                
                o=[logger.debug("Possible location of error %s", loc['loc']) for loc in min_error]
                deepness=0
                for loc in min_error:
                    if len(loc['loc'])>deepness:
                        deepness=len( loc['loc'] )
                errors_in=[]
                for loc in min_error:
                    error_loc=loc['loc']
                    if len(error_loc)==deepness:
                        # logger.debug("Error_location %s", error_loc)
                        for i,err in enumerate(error_loc):
                            # logger.debug("Error_location possition i: %s", i)
                            if i==0:
                                error_in=getattr(exp, error_loc[i])
                            else:
                                if isinstance(error_loc[i],int):
                                    error_in=error_in[error_loc[i]]
                                else:
                                    error_in=getattr(error_in, error_loc[i])

                        # logger.debug("Error in: %s", error_in)
                        errors_in.append(error_in)
                unique_errors=list(set(errors_in))
                o=[logger.debug("Attribute error in %s", err) for err in unique_errors]
                raise exc
            else:
                if not isinstance(exp_class,IntentNrm.IntentExpectation):
                    logger.warning("Assure for %s",schema)
                    # return True
                else:
                    logger.warning("General intentExpectaion assurance %s",schema)
                    # return True
                return True

    
    def format_error_handler(self, exception):

        logger.warning("Error in basic Intent format.")

    def attribute_error_handler(self, exception):
        # TODO: send intent report error handling
        logger.warning("Error in local library Intent format.")