## How to: Create a new library to translate Intents

The Intent paradigm lies in its potential scalability for new intents as the technology changes. The isolated perspective it offers enables seamless integration of new network connectivity adaptors through the addition of a library in the intent catalogue within the Intent-Engine. This concept nicely follows the same potential that micro-kernel architectures have.

### New library

The Intent-Engine can be understood as a translator with libraries installed as plugins. At the end, the plugins are nothing but a Python class that the Intent Core will use to process the intents coming as inputs to the northbound interface. The new libraries located at the Intent Catalogue must follow the general abstract class.

The general class defines functions, parameters, and objects necessary for all the libraries in the Intent Catalogue. There are two main functionalities that a new library must have:

- Decision tree for classification: decision tree that is traversed and compared to the different keywords inside the intent. The leaf of the decision points to the library in charge of generating the subintent.
- Subintent generation: given an intent that has been classified, the library generates an intent that a less abstracted library (closer to the technology) can understand as its own. The classifier will iterate over an intent until the library is marked as ILU (intent logic unit). Then, the classification step is finished and passes to the translation.
- Translation: Once the intent is an ILU, it means that there is a one-to-one relation with a network action. In this step, the library is in charge of taking all the different intent parameters and generating the necessary actions.

There are other functionalities that a new library could have depending on the complexity of the technology itself, such as requesting information from a database or a machine learning-based translation. But as long as all these functions are enclosed in the abstract definitions, the Intent Core will work.

It is necessary for the importer module in the Intent-Engine that the libraries' paths are written in the *intent_catalogue.in* file. This enables the whole project to use the libraries' functions.

### Workflow

This are some recomended definition steps that could facilitate the process of creating a new library.
*New library:*
- Define what attributes, targets, and contexts are supported. New ones? Already existing ones?
- Make the decision tree so the classifier can recognize the new network technology.
- New interface from the Intent-engine system to the technology? New executioner?

### Using the integrated data model

The internal object model in Python is generated automatically from the OpenAPI specification (unofficial repository that can serve as an example: [5GC_APIs/TS28312_IntentNrm.yaml at Rel-18 · jdegre/5GC_APIs](https://github.com/jdegre/5GC_APIs/blob/Rel-18/TS28312_IntentNrm.yaml)). If any change to the model is required in the Python object "*IntentNrm.IntentNrmg*", the following command will do the work:

```bash
datamodel-codegen --input intent_engine/tools/intent_openapi/NrmgIntent.yaml --output intent_engine/core/IntentNrm.py --enum-field-as-literal all --collapse-root-models
```

> [!NOTE]
> Datamodel-codegen is an external python package that must be installed.

Thanks to the automatic datamodel generation, its posible to use directly the python objects to easily traverse the intent. The full definition can be found in the file "*Repos/intent-based-system/intent_engine/core/IntentNrm.py*" but here are some useful examples (in pseudo-code):

```python
# Get expecation list of the intent
for exp in intent.intentExpectations:
# Get the expectation verb
exp_verb=exp.expectationVerb
# Get expectaion object
exp_obj=exp.expectationObject
# Get expectation type
exp_type=exp_obj.objectType
# Get object contexts
for obj_ctx in exp_obj.objectContexts:
# Get context attribute
att=obj_ctx.contextAttribute
# Get targets in expectation
for trg_ctx in exp.expectationTargets:
# Get list of expectaion contexts
for exp_ctx in exp.expectationContexts:
```


### Example with code

```python
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
from intent_engine.core import IntentNrm
from intent_engine.core.ib_model import IntentModel, jsonable_model_encoder

logger = logging.getLogger(__name__)

class green(abstract_library):
    """
    Library as example of green slice. May not directly work.
    Notice that the class name has to be the same as the one defined in intent_catalogue.in 
    or in the manifest file as one of the libraries to import. Normally, either the library 
    generates a subintent or translates a subintent/intent to the underlaying technology interface. 
    """
    def __init__(self):
        params={}
        # Decision tree that will be used as decisor. The classifier will call this 
        # parameter at initialization.
        decision_tree={
           "green" : { # userLabel first key word to check
               "Slice_Energy_Saving":{ # expectationType second key word to check
                    "ENSURE":"green", # expectationVerb third
                    "DELIVER":"green"
                },
                "Slice":{
                    "ENSURE":"green",
                    "DELIVER":"green"
                }
           }
        }
        super().__init__(module_name="green",isILU=True/False,params=params,decision_tree=decision_tree)
        self.__params=params
    

    def generate_subintent(self,intent_model:IntentModel) -> list[IntentModel]:
        """
        Return sub intents of a slice in a green context.
        Also return library to porcess the subintent, as green is not ilu,
        this means have no final tranlation with a technology.
        Return: list
        """
        intent=intent_model.get_intent()
        logger.debug("Generating Green subintent...")
        intent_dict=intent.dict(exclude_defaults=True)
        green_expectations=[]
        slice_expectations=[]
        subintent_green={}
        subintent_slice={}

        for i,exp in enumerate(intent.intentExpectations):
            if exp.expectationVerb == 'ENSURE':
                intent_dict['intentExpectations'][i]['expectationObject']['objectType']='Slice_Energy_Saving'
                green_expectations.append(intent_dict['intentExpectations'][i])

            if exp.expectationVerb == 'DELIVER':
                intent_dict['intentExpectations'][i]['expectationObject']['objectType']='Slice'
                slice_expectations.append(intent_dict['intentExpectations'][i])

        # TODO: meter la nbi de TFS como parte del context para el subintent
        subintent_green['Intent']={'intentExpectations':green_expectations,
                                   'id':intent_dict['id'],
                                    'userLabel':'slice',
                                    'intentPriority':intent_dict['intentPriority']}
        # TODO:check intentPriority:  ,observationPeriod: , intentAdminState: ''? maintain?

        subintent_slice['Intent']={'intentExpectations':slice_expectations,
                                   'id':intent_dict['id'],
                                    'userLabel':'slice',
                                    'intentPriority':intent_dict['intentPriority']}
     
        return [IntentModel(subintent_green),IntentModel(subintent_slice)]

    def translator(self,subintent : IntentModel)-> tuple[list , str]:
	    """
        This functions translate an atomic intent into a format a specific software
        can understand. This function will decide which functionality (ENSURE , DEPLOY) 
        will be called.

        This decision can be done using the same idea of the decision tree or a more
        direct way.
        
        The function must return two dictionaries in a list format and a string. The first 
        dict is usually the information of the intent translated in a dict very close to
        the information model of the underlaying technology. The second one is usually
        related to the parameters that the executioner must need to make the connection, 
        for example, endpoint API url, connection type, credentials...
        Then, the string is the executioners names to be called separated by space.
        Usually, it is the executioner followed by the "sys_out" executioner which will
        output all the parameters to system outprint.
        
        Return: list[dict,dict] , string 
        """
        exec_params=[]
        self.__params={
            "Constrain type":"green"
        }
        logger.info("Translating green_bssf...")
        logger.debug("debug green_bssf...")
        exec_params=[]
        logger.info("Translating slice_5g...")
        logger.debug("debug slice_5g...")
        intent = subintent.get_intent()
        for exp in intent.intentExpectations:
            exp_verb=exp.expectationVerb
            logger.debug("expectation case %s",exp_verb)
            match exp_verb:
                case "CREATE":
                    exp_obj=exp.expectationObject
                    logger.debug("create case obj: %s",exp_obj)
                    exp_type=exp_obj.objectType
                    match exp_type:
                        case "SLICE":
                            # Possible list of ipv4 filters
                            ip4filters=[]
                            for obj_ctx in exp_obj.objectContexts:
                                # Loop ctx inside obj
                                # Filter
                                ipv4filter={}
                                logger.debug("objectctx case %s: ",obj_ctx)
                                att=obj_ctx.contextAttribute
                                # several filters have to be referenced so matching
                                # between ip,port,type
                                match att:
                                    case "ip4Address":
                                        logger.debug("ip4Address case %s",obj_ctx.contextValueRange)
                                        ipv4filter['ip4Address']=obj_ctx.contextValueRange
                                        logger.debug("params after %s",self.__params)
                                    case "type":
                                        logger.debug("type case")
                                        ipv4filter['type']=obj_ctx.contextValueRange
                                    case "portNumber":
                                        logger.debug("portNumber case")
                                        ipv4filter['portNumber']=obj_ctx.contextValueRange
                                    case "portType":
                                        logger.debug("portType case")
                                        ipv4filter['portType']=obj_ctx.contextValueRange
                                # append to ipv4 filters althoug functionality not jet #TODO
                                ip4filters.append(ipv4filter)
                            self.__params['ipv4filters']=ip4filters
                    for exp_trg in exp.expectationTargets:
                        # Loop trg inside exp
                        att=exp_trg.targetName
                        match att:
                            case "ulCapacity":
                                logger.debug("ulCapacity case")
                                self.__params['ulCapacity']=exp_trg.targetValueRange
                                exp_trg_ctx=exp_trg.targetContexts
                                if exp_trg_ctx:
                                    for ctx in exp_trg_ctx:
                                        # Loop ctx inside trg inside exp
                                        att=ctx.contextAttribute
                                        match att:
                                            case "profile":
                                                logger.debug("profile_exp_trg_ctx case")
                                                self.__params['profile']=ctx.contextValueRange
                                                self.__params['SUPI']=exp.expectationObject.objectInstance
                            case "dlCapacity":
                                logger.debug("dlCapacity case")
                                exp_trg_ctx=exp_trg.targetContexts
                                self.__params['dlCapacity']=exp_trg.targetValueRange
                                if exp_trg_ctx:
                                    for ctx in exp_trg_ctx:
                                        # Loop ctx inside trg inside exp
                                        att=ctx.contextAttribute
                                        match att:
                                            case "profile":
                                                logger.debug("profile_exp_trg_ctx case")

            # loop for all expectation contexts
            for exp_ctx in exp.expectationContexts:
                match exp_ctx.contextAttribute:
                    case "url":
                        logger.debug("intent context url case")
                        logger.debug("url: %s",exp_ctx.contextValueRange)


        # The output of this function will be the input for the execution step
        return [self.__params,exec_params],"sysout"
```
