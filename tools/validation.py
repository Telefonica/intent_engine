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
import yaml
from schema import Optional, Schema, SchemaError,Or,And

def load_validation_schema(schema_file):
    with open(schema_file, 'r') as file:
        schema = yaml.safe_load(file)
    return schema

def validate_yaml_2(yaml_data, schema):
    try:
        data = yaml.safe_load(yaml_data)
        # Validate against the schema
        validate_nested(data, schema)
    
    except Exception as e:
        print("Validation error:", e)
        return False
    return True

def validate_nested(data, schema):
    # para cada clave-valor check (if data[key] in schema[key])
    # necesito poder extraer una estructura
    for key, value in schema.items():
        if key not in data:
            raise ValueError(f"Key '{key}' is missing")
        if not data[key] in value:
            raise ValueError(f"Key '{key}' has invalid type")

        # Recursively validate nested structures
        if isinstance(value, dict):
            validate_nested(data[key], value)
        elif isinstance(value, list):
            for item in data[key]:
                if not isinstance(item, type(value[0])):
                    raise ValueError(f"Invalid type in list for key '{key}'")

def validate_yaml(yaml_data):
    # Define the expected schema
    expected_schema = Schema({
        "Intent": {
            "AttributeName": ['cloud_continuum'],
            "Expectations": [{
                "Verb": str,
                "Object": {
                    "Type": str,
                    "Instance": str,
                    "Contexts": [{
                        "AttributeName":Or(str,None),
                        "Attribute": str,
                        "Condition": str,
                        "ValueRange": str
                    }]
                },
                "Targets": [{
                    "AttributeName":Or(str,None),
                    "Attribute": str,
                    "Condition": str,
                    "ValueRange": float                  
                }],
                "Contexts": [{
                    "AttributeName":Or(str,None),
                    "Attribute": str,
                    "Condition": str,
                    "ValueRange": str
                }]
            }],
            "Context": {
                "AttributeName":Or(str,None),
                "Attribute": str,
                "Condition": str,
                "ValueRange": str
            }
        }
    })
    
    try:
        expected_schema.validate(yaml_data)
        print("Configuration is valid.")
    except SchemaError as se:
        raise se
    return True


# YAML string from your example
yaml_data = """
Intent:
  AttributeName: 'cloud_continuum'
  Expectations:
    - Verb: 'request'
      Object :
       Type : 'l2vpn'
       Instance: 'l2vpn-tfs-name'
       Contexts:
        - AttributeName : 'node'
          Attribute : 'node_src'
          Condition : 'IS_EQUAL_TO'
          ValueRange : '3.3.3.3'
        - AttributeName : 'node'
          Attribute : 'node_dst'
          Condition : 'IS_EQUAL_TO'
          ValueRange : '5.5.5.5'
        - AttributeName : 'interface'
          Attribute : 'endpoint_src'
          Condition : 'IS_EQUAL_TO'
          ValueRange : 'GigabitEthernet0/0/0/1'
        - AttributeName : 'interface'
          Attribute : 'endpoint_dst'
          Condition : 'IS_EQUAL_TO'
          ValueRange : 'GigabitEthernet0/0/0/1'
        - AttributeName : 'vlan'
          Attribute : 'vlan_id'
          Condition : 'IS_EQUAL_TO'
          ValueRange : '999'
        - AttributeName : 'vlan'
          Attribute : 'ni_name'
          Condition : 'IS_EQUAL_TO'
          ValueRange : 'ninametfs'
      Targets:
        - AttributeName :
          Attribute : 'bandwith'
          Condition : 'IS_EQUAL_TO_OR_GREATER_THAN'
          ValueRange : 10.0
        - AttributeName :
          Attribute : 'latency'
          Condition : 'IS_LESS_THAN'
          ValueRange : 15.2
      Contexts:
       - AttributeName : 'tfs_controller'
         Attribute : 'url'
         Condition : 'IS_EQUAL_TO'
         ValueRange : 'http://192.168.165.10/'
       - AttributeName : 'tfs_session'
         Attribute : 'user'
         Condition : 'IS_EQUAL_TO'
         ValueRange : 'admin'
       - AttributeName : 'tfs_session'
         Attribute : 'password'
         Condition : 'IS_EQUAL_TO'
         ValueRange : 'admin'
  Context:
    AttributeName: 'admin_id'
    Attribute: 'state'
    Condition: 'IS_EQUAL_TO'
    ValueRange: 'flavor'
"""

# Validate the YAML data
configuration = yaml.safe_load(yaml_data)
if validate_yaml(configuration):
    print("YAML validation successful")
else:
    print("YAML validation failed")
