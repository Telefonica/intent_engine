import json,yaml,os
from typing import get_args
import IntentNrm
from devtools import pprint
from fastapi.encoders import jsonable_encoder
def yaml_to_data(relative_path):

    # Get the current working directory
    current_directory = os.getcwd()
    # Combine the current working directory and the relative path
    yaml_file_path = os.path.join(current_directory, relative_path)
    # Open the file and load the YAML data
    data={}
    with open(yaml_file_path, 'r') as yaml_file:
        data = yaml.safe_load(yaml_file)

    return data
def jsonable_model_encoder(intentin) -> dict:
    """
    Given a model or a dict with enum values as type enum class, 
    returns the same model or dict with all literal values.
    This enables the posibility to parse againt the model as IntentMncc
    without attributes as custom classes.
    """
    return jsonable_encoder(intentin)

def get_literal_value(data_model, attr_name):
    return get_args(data_model.model_fields[attr_name].annotation)
# print(**(yaml_to_data("intent_engine/inputs/intent-energy-carbon-efficiency.yaml")))
# intentsingle = IntentExpectations.IntentSingle( **(yaml_to_data("intent_engine/inputs/intent-energy-carbon-efficiency.yaml")))
Intent = yaml_to_data("intent_engine/inputs/green.yaml")
# Intent = yaml_to_data("intent_engine/inputs/intent-energy-carbon-efficiency.yaml")
# pprint(Intent)
intent = IntentNrm.IntentNrmg(**Intent['Intent'])
# intent=IntentNrm(**(yaml_to_data("intent_engine/inputs/intent-energy-carbon-efficiency.yaml")))
print(type(intent.intentExpectations[0]))
# print(intent)
pprint(intent.dict(exclude_defaults=True))
keywords=[]
keywords.append(intent.userLabel)
# intent_expectations: List[IntentNrm.IntentExpectation] = self.__intent.intentExpectations
for exp in intent.intentExpectations:
    print(type(exp))
    keywords.append(exp.expectationVerb.value)
    keywords.append(exp.expectationObject.objectType.value)
    # keywords.extend([trg.targetName for trg in exp.expectationTargets])
    # pprint(exp)
    print(list(IntentNrm.ExpectationVerb1.__members__.keys()))
    print(type(exp.expectationVerb)._member_names_)
    # print(exp.expectationVerb)
    # print(get_literal_value(IntentNrm.IntentSingle,exp.expectationVerb))
    print(exp.dict())
    
    try:
        IntentNrm.NewNetworkExpectation(**(exp.dict()))
        isinstance(exp,IntentNrm.NewNetworkExpectation)
    except:
        pass
    try:
        IntentNrm.New5GFlowExpectation(**(exp.dict()))
        isinstance(exp,IntentNrm.New5GFlowExpectation)
    except:
        pass
print(keywords)
print("Ctx: %s",type(intent.intentContexts[0]))
pprint(jsonable_model_encoder(intent))

