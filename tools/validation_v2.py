import yaml

def validate_yaml(yaml_data):
    # Define the expected schema
    expected_schema = {
        "Intent": {
            "AttributeName": ['cloud_continuum'],
            "Expectations": [{
                "Verb": str,
                "Object": {
                    "Type": str,
                    "Instance": str,
                    "Contexts": [{
                        "AttributeName": str,
                        "Attribute": str,
                        "Condition": str,
                        "ValueRange": str
                    }]
                },
                "Targets": [{
                    "AttributeName": str,
                    "Attribute": str,
                    "Condition": str,
                    "ValueRange": float
                }],
                "Contexts": [{
                    "AttributeName": str,
                    "Attribute": str,
                    "Condition": str,
                    "ValueRange": str
                }]
            }],
            "Context": {
                "AttributeName": str,
                "Attribute": str,
                "Condition": str,
                "ValueRange": str
            }
        }
    }

    shema = {
            "Expectations": [{
                "Verb": str,
                "Object": {
                    "Type": str,
                    "Instance": str,
                    "Contexts": [{
                        "AttributeName": str,
                        "Attribute": str,
                        "Condition": str,
                        "ValueRange": str
                    }]
                },
                "Targets": [{
                    "AttributeName": str,
                    "Attribute": str,
                    "Condition": str,
                    "ValueRange": float
                }],
                "Contexts": [{
                    "AttributeName": str,
                    "Attribute": str,
                    "Condition": str,
                    "ValueRange": str
                }]
            }],
        }
    try:
        # Load YAML data
        data = yaml.safe_load(yaml_data)

        # Validate against the schema
        if not isinstance(data, dict):
            raise ValueError("Invalid YAML structure")

        for key, value in shema.items():
            if key not in data:
                raise ValueError(f"Key '{key}' is missing")
            # print(f"Value {value}")
            if not isinstance(data[key], type(value)):
                raise ValueError(f"Key '{key}' has invalid type")
            if isinstance(data[key],list):
                if data[key] in value:
                    print("Valid value")
                else:
                    raise ValueError(f"Data '{data[key]}' has invalid value")

            # Recursively validate nested structures
            if isinstance(value, dict):
                validate_nested(data[key], value)
    
    except Exception as e:
        print("Validation error:", e)
        return False
    
    return True

def validate_expectation(data,schema):
    for key, value in schema.items():
        if key not in data:
            print(f"Value nest{value}")
            raise ValueError(f"Key '{key}' is missing")
        print(f"Value nest {data[key]}=?{value}")
        # if not isinstance(data[key], type(value)):
        # Recursively validate nested structures
        if isinstance(value, dict):
            validate_nested(data[key], value)
        elif isinstance(value, list):
            for item in data[key]:
                if not isinstance(item, type(value[0])):
                    raise ValueError(f"Invalid type in list for key '{key}:{item}'")
        if data[key] not in ['Contexts','Targets']:
            if data[key] not in value:
                raise ValueError(f"Key '{key}:{data[key]}' has invalid type nest")

def validate_nested(data, schema):
    for key, value in schema.items():
        if key not in data:
            print(f"Value nest{value}")
            raise ValueError(f"Key '{key}' is missing nest")
        print(f"Value nest {data[key]}=?{value}")
        # if not isinstance(data[key], type(value)):
        # Recursively validate nested structures
        if isinstance(value, dict):
            validate_nested(data[key], value)
        elif isinstance(value, list):
            for item in data[key]:
                if not isinstance(item, type(value[0])):
                    raise ValueError(f"Invalid type in list for key '{key}:{item}'")
        if data[key] not in ['Contexts','Targets']:
            if data[key] not in value:
                raise ValueError(f"Key '{key}:{data[key]}' has invalid type nest")

# YAML string from your example
exp_data = """
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
    - AttributeName : 'bw'
      Attribute : 'bandwith'
      Condition : 'IS_EQUAL_TO_OR_GREATER_THAN'
      ValueRange : 10.0
    - AttributeName : 'lt'
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
"""
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
        - AttributeName : 'bw'
          Attribute : 'bandwith'
          Condition : 'IS_EQUAL_TO_OR_GREATER_THAN'
          ValueRange : 10.0
        - AttributeName : 'lt'
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
if validate_yaml(exp_data):
    print("YAML validation successful")
else:
    print("YAML validation failed")
