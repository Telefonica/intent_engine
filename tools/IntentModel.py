import json,yaml,os
import IntentExpectations
import IntentNrm
from devtools import pprint

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


# print(**(yaml_to_data("intent_engine/inputs/intent-energy-carbon-efficiency.yaml")))
# intentsingle = IntentExpectations.IntentSingle( **(yaml_to_data("intent_engine/inputs/intent-energy-carbon-efficiency.yaml")))
Intent = yaml_to_data("intent_engine/inputs/intent-energy-carbon-efficiency.yaml")
# print(Intent)
intent = IntentNrm.IntentSingle(**Intent['Intent'])
# intent=IntentNrm(**(yaml_to_data("intent_engine/inputs/intent-energy-carbon-efficiency.yaml")))
pprint(intent.dict(exclude_defaults=True))