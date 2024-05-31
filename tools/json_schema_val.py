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
import json
from pathlib import Path
import jsonschema
import jsonschema.exceptions
import yaml
from referencing import Registry, Resource
from referencing.exceptions import NoSuchResource
import referencing.jsonschema

# YAML string from your example
yaml_data = """
Intent:
  AttributeName: 'cloud_continuum'
  Expectations:
    - Verb: 'request'
      Object :
       Type : 'l2vpna'
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
# Describe what kind of json you expect.
intentSchema = {
  "$schema": "https://json-schema.org/draft/2019-09/schema",
  "$id": "/schemas/intent",
  "type": "object",
  "properties": {
    "Intent": {
      "type": "object",
      "properties": {
        "AttributeName": {
          "type": "string"
        },
        "Expectations": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "Verb": {
                "type": "string"
              },
              "Object": {
                "type": "object",
                "properties": {
                  "Type": {
                    "enum": ["l2vpn"]
                  },
                  "Instance": {
                    "type": "string"
                  },
                  "Contexts": {
                    "type": "array",
                      "items":{
                        "anyOf":[{"$ref":"#/$def/Context_n"},
                      {"$ref": "/schemas/Context"}
                      ]
                    }
                  }
                },
                "required": [
                  "Type",
                  "Instance",
                  "Contexts"
                ]
              },
              "Targets": {
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "AttributeName": {
                      "type": [
                        "string",
                        "null"
                      ]
                    },
                    "Attribute": {
                      "type": "string"
                    },
                    "Condition": {
                      "type": "string"
                    },
                    "ValueRange": {
                      "type": [
                        "number",
                        "null"
                      ]
                    },
                    "Context": {
                      "$ref": "/schemas/Context"
                    }
                  },
                  "required": [
                    "Attribute",
                    "Condition",
                    "ValueRange"
                  ]
                }
              },
              "Contexts": {
                "type": "array",
                "items": {
                  "$ref": "/schemas/Context"
                }
              }
            },
            "required": [
              "Verb",
              "Object",
              "Targets",
              "Contexts"
            ]
          }
        },
        "Context": {
          "$ref": "/schemas/Context"
        }
      },
      "required": [
        "AttributeName",
        "Expectations",
        "Context"
      ]
    }
  },
  "$def": {
    "Context_n": {
      "type": "object",
      "properties": {
        "AttributeName": {
          "type": [
            "string",
            "null"
          ]
        },
        "Attribute": {
          "enum":["node_src","node_dst"]
        },
        "Condition": {
          "type": "string"
        },
        "ValueRange": {
          "type": "string"
        }
      },
      "required": [
        "Attribute",
        "Condition",
        "ValueRange"
      ]
    }
  }
}

contextSchema = {
    "$schema": "https://json-schema.org/draft/2019-09/schema",
    "$id": "/schemas/Context",
    "type": "object",
    "Context": {
      "type": "object",
      "properties": {
        "AttributeName": {
          "type": [
            "string",
            "null"
          ]
        },
        "Attribute": {
          "type": "string"
        },
        "Condition": {
          "type": "string"
        },
        "ValueRange": {
          "type": "string"
        }
      }
    },
    "required":["Attribute","Condition","ValueRange"]
}

cloud_schema = {
  "$schema": "https://json-schema.org/draft/2019-09/schema",
  "$id": "/schemas/cloud_continuum",
  "type": "object",
  "properties": {
    "Expectation": {
      "type": "object",
      "oneOf": [
        {
          "if": {
            "Type": {
              "const": "l2sm"
            }
          },
          "then": {
            "$ref": "/schemas/l2sm"
          },
          "else": False
        },
        {
          "if": {
            "Type": {
              "const": "l2vpna"
            }
          },
          "then": {
            "$ref": "/schemas/l2vpn"
          },
          "else": False
        }
      ]
    }
  }
}

l2vpn_schema = {
    "$schema": "https://json-schema.org/draft/2019-09/schema",
    "$id" : "/schemas/l2vpn",
    "type" : "object",
    "required" : ["go"] 
}

cloud_composed_schema = {
  "$schema": "https://json-schema.org/draft/2019-09/schema",
  "$id": "/schemas/cloud_continuum_comp",
  "required": [
    "Intent"
  ],
  "if": {
    "$ref": "/schemas/intent"
  },
  "then": {
    "anyOf": [
      {
        "$ref": "#/schemas/l2vpn"
      },
      {
      	"$ref": "#/schemas/l2sm"
      }
    ]
  },
  "else": False,
  "schemas": {
    "l2vpn": {
      "$id": "schemas/l2vpn",
      "type": "object",
      "properties": {
        "Intent": {
          "type": "object",
          "required": [
            "Expectations"
          ],
          "properties": {
            "Expectations": {
              "type": "array",
              "items": {
                "type": "object",
                "required": [
                  "Object"
                ],
                "properties": {
                  "Object": {
                    "type": "object",
                    "required": [
                      "Type"
                    ],
                    "properties": {
                      "Type": {
                        "const": "l2vpn"
                      }
                    }
                  }
                }
              }
            }
          }
        }
      },
      "required": [
        "Intent"
      ]
    },
    "l2sm": {
      "$id": "schemas/l2sm",
      "type": "object",
      "properties": {
        "Intent": {
          "type": "object",
          "required": [
            "Expectations"
          ],
          "properties": {
            "Expectations": {
              "type": "array",
              "items": {
                "type": "object",
                "required": [
                  "Object"
                ],
                "properties": {
                  "Object": {
                    "type": "object",
                    "required": [
                      "Type"
                    ],
                    "properties": {
                      "Type": {
                        "const": "l2sm"
                      }
                    }
                  }
                }
              }
            }
          }
        }
      },
      "required": [
        "Intent"
      ]
    },
  }
}

SCHEMAS = Path("intent_engine/tools/schemas")
def retrieve_from_filesystem(uri: str):
    if not uri.startswith("http://localhost/"):
        raise NoSuchResource(ref=uri)
    path = SCHEMAS / Path(uri.removeprefix("http://localhost/"))
    contents = json.loads(path.read_text())
    return Resource.from_contents(contents)
def validateJson(jsonData):
    try:
        # intent_schema = intentSchema #jsonloads
        # context_schema = contextSchema
        # schema_lib = {
        #     intent_schema['$id'] : intent_schema,
        #     context_schema['$id'] : context_schema,
        # }
        # registry = Registry(retrieve=retrieve_from_filesystem)
        registry = Registry()
        resource = Resource.from_contents(contextSchema)
        registry = resource @ registry
        resource = Resource.from_contents(cloud_schema)
        registry = resource @ registry
        resource = Resource.from_contents(l2vpn_schema)
        registry = resource @ registry
        resource = Resource.from_contents(intentSchema)
        registry = resource @ registry
        resource = Resource.from_contents(cloud_composed_schema)
        registry = resource @ registry
        # print(registry.contents("/schemas/cloud_continuum_comp"))
        # resolver = RefResolver.from_schema(intent_schema, store=schema_lib)
        validator = jsonschema.Draft202012Validator(schema=intentSchema,registry=registry)
        validator = jsonschema.Draft202012Validator(schema=cloud_schema,registry=registry)
        validator = jsonschema.Draft202012Validator(schema=cloud_composed_schema,registry=registry)
        validator.validate(instance=jsonData)
    except jsonschema.exceptions.ValidationError as err:
        validator = jsonschema.Draft7Validator(intentSchema)
        errors = validator.iter_errors(jsonData)  # get all validation errors
        for error in errors:
            print(error)
            print('------')
            break
        print(err)
        s=err
        return False
    return True

# Convert json to python object.
dictdata=yaml.safe_load(yaml_data)
# print(dictdata)
jsonData = json.dumps(dictdata['Intent'])
# validate it
isValid = validateJson(dictdata)
if isValid:
    # print(jsonData)
    print("Given JSON data is Valid")
else:
    # print(jsonData)
    print("Given JSON data is InValid")
