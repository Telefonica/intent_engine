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

import ast
import logging
from intent_engine.catalogue.abstract_library import abstract_library
from intent_engine.core.ib_model import IntentModel

logger = logging.getLogger(__name__)

class enif_slice(abstract_library):
    """
    Library for 6Green project
    """
    def __init__(self):
        decision_tree={
           "green" : {
               "Slice_Energy_Saving":{
                   "DEPLOY":"enif_slice"
                    }
                }
        }
        self.__componentNodeInstances={
          "componentNodeInstanceID": "",
          "componentNodeInstanceHexID": "",
          "componentNodeInstanceName": ""
          }
        self.__AccessConstrains={
    "constraintID": "",
    "interfaceInstanceID": "",
    "qi": "",
    "radioServiceType": "",
    "resourceType": "",
    "allocationRetentionPriorityProfile": 0,
    "minimumGuaranteedBandwidth": 0,
    "maximumRequiredBandwidth": 0,
    "constraintUnit": "",
    "category": "ACCESS",
    "type": ""
        }
        self.__ComponentHostingConstrains={
          "constraintID": "",
          "category": "",
          "componentNodeInstanceID": "",
          "componentNodeInstanceHexID": "",
          "type": "",
          "constraintMetric": "",
          "constraintValue": "",
          "constraintUnit": ""
        }
        params={
            "applicationInstanceID":"",
            "name":"",
            "callbackURL":"",
            "authenticationDetails":"",
            "componentNodeInstances":[],
            "constraints":[],
            "graphLinkNodeInstances":[],
        }
        super().__init__(module_name="enif_slice",isILU=True,params=params,decision_tree=decision_tree)
        self.__params=params
    
    def translator(self,subintent : IntentModel) -> tuple[list , str]:
        exec_params=[]
        params={}
        instances={}
        logger.info("Translating enif_slice...")
        logger.debug("debug enif_slice connector...")
        logger.debug("subint: %s",subintent)
        for exp in subintent.get_expectations():
            exp_verb=exp.get_verb()
            logger.debug("expectation case %s",exp_verb)
            match exp_verb:
                case "ensure":
                    exec_params=[]
                    self.__params={
                        "Constrain type":"green"
                    }
                    logger.info("Translating green_bssf in enif...")
                    logger.debug("debug enif_slice...")
                    
                    return [self.__params,exec_params],"sysout"
                case "deploy":
                    exp_obj=exp.get_object()
                    logger.debug("deploy case obj: %s",exp_obj)
                    exp_type=exp_obj.get_type()
                    match exp_type:
                        case "slice_intent_5ginduce":
                            for obj_ctx in exp_obj.get_contexts():
                                # Loop ctx inside obj
                                logger.debug("objectctx case %s: ",obj_ctx)
                                att=obj_ctx.get_attribute()
                                match att:
                                    case "name":
                                        logger.debug("name case %s",obj_ctx.get_value_range())
                                        self.__params['name']=obj_ctx.get_value_range()
                                        logger.debug("params after %s",self.__params)
                                        if obj_ctx.get_name() not in instances.keys():
                                            instances[obj_ctx.get_name()]={}
                                        instances[obj_ctx.get_name()]['name']=obj_ctx.get_value_range()
                                    case "hex_ID":
                                        logger.debug("hex_ID case")
                                        if obj_ctx.get_name() not in instances.keys():
                                            instances[obj_ctx.get_name()]={}
                                        self.__params['hex_ID']=obj_ctx.get_value_range()
                                        instances[obj_ctx.get_name()]['hex_ID']=obj_ctx.get_value_range()
                                    case "type":
                                        logger.debug("type case")
                                        if obj_ctx.get_name() not in instances.keys():
                                            instances[obj_ctx.get_name()]={}
                                        self.__params['type']=obj_ctx.get_value_range()
                                        instances[obj_ctx.get_name()]['type']=obj_ctx.get_value_range()
                                    case "from_to":
                                        logger.debug("from_to case")
                                        if obj_ctx.get_name() not in instances.keys():
                                            instances[obj_ctx.get_name()]={}
                                        self.__params['from_to']=obj_ctx.get_value_range()
                                        instances[obj_ctx.get_name()]['from_to']=obj_ctx.get_value_range()
                                    case "to":
                                        logger.debug("to case")
                                        if obj_ctx.get_name() not in instances.keys():
                                            instances[obj_ctx.get_name()]={}
                                        self.__params['to']=obj_ctx.get_value_range()
                                        instances[obj_ctx.get_name()]['to']=obj_ctx.get_value_range()
                    for trg_ctx in exp.get_target():
                        # Loop trg inside exp
                        att=trg_ctx.get_attribute()
                        match att:
                            case "RAM":
                                logger.debug("RAM case")
                                trg_ctx=trg_ctx.get_context()
                                if trg_ctx:
                                    for ctx in trg_ctx:
                                        # Loop ctx inside trg inside exp
                                        att=ctx.get_attribute()
                                        match att:
                                            case "type":
                                                logger.debug("type_trg_ctx case")
                            case "V_CPU":
                                logger.debug("V_CPU case")
                                trg_ctx=trg_ctx.get_context()
                                if trg_ctx:
                                    for ctx in trg_ctx:
                                        # Loop ctx inside trg inside exp
                                        att=ctx.get_attribute()
                                        match att:
                                            case "type":
                                                logger.debug("type_trg_ctx case")
                            case "region":
                                logger.debug("region case")
                                trg_ctx=trg_ctx.get_context()
                                if trg_ctx:
                                    for ctx in trg_ctx:
                                        # Loop ctx inside trg inside exp
                                        att=ctx.get_attribute()
                                        match att:
                                            case "radio_service_type":
                                                logger.debug("radio_service_type_trg_ctx case")
                            case "guaranteed_bandwidth":
                                logger.debug("guaranteed_bandwidth case")
                                trg_ctx=trg_ctx.get_context()
                                if trg_ctx:
                                    for ctx in trg_ctx:
                                        # Loop ctx inside trg inside exp
                                        att=ctx.get_attribute()
                                        match att:
                                            case "radio_service_type":
                                                logger.debug("radio_service_type_trg_ctx case")
                                            case "resource_service_type":
                                                logger.debug("resource_service_type_trg_ctx case")
                                            case "qi":
                                                logger.debug("qi_trg_ctx case")
                                            case "allocation_priority_profile":
                                                logger.debug("allocation_priority_profile_trg_ctx case")
                    
                    for exp_ctx in exp.get_context():
                        att=exp_ctx.get_attribute()
                        match att:
                            case "url":
                                logger.debug("url case")
                                
                                params['url']=exp_ctx.get_value_range()
                                params['headers'] = {'Content-Type': 'multipart/form-data'}
                                params['connect_type'] = 'get'
                            case "user":
                                logger.debug("user case")
                                params['user']=exp_ctx.get_value_range()
                            case "password":
                                logger.debug("pass case")
                                params['password']=exp_ctx.get_value_range()


        # esto debería context del intent
        logger.debug("int ctx: %s",subintent.get_context())
        match subintent.get_context().get_name():
            case "green":
                logger.debug("intent context green case")
                match subintent.get_context().get_attribute():
                    case "state":
                        logger.debug("intent context att state case")
                    case "permits":
                        logger.debug("intent context att permits case")

        return [self.slice_schema(instances),params],"sysout"

    def generate_subintent(self,intent:IntentModel) -> IntentModel:
        """
        Return sub intents of a slice in a green context.
        """
        logger.debug("Simple enif_slice")
        logger.debug("With intent: %s", intent.get_name())
        subintent=IntentModel()
        subintent.set_name(intent.get_name())
        subintent.set_context(intent.get_context())
        for exp in intent.get_expectations():
            if exp.get_object().get_type() == 'slice_intent_5ginduce':
                match exp.get_verb():
                    # remove any not enif_slice type expectation
                    case "deploy":
                        logger.debug("Generating sub intent ENIF->ENIF...")
                        ilu="enif_slice"
                        subintent.set_expectations([exp])
                        subintent.set_context(intent.get_context())
                        logger.debug("generated subintent:%s",subintent)
                    case "ensure":
                        logger.debug("Generating sub intent GREEN(ENIF)->ENIF...")
                        ilu="enif_slice"
                        subintent.set_expectations([exp])
                        subintent.set_context(intent.get_context())
                        logger.debug("generated subintent:%s",subintent)
        return subintent
    
    def slice_schema(self, slice_content: dict):
        componentNodeInstances=[]
        graphLinkNodeInstances=[]
        for instace in slice_content:
            logger.debug("split content %s",instace.split("node_instance_"))
            if instace.split("node_instance_")[0] == "":
                node_instance_id=instace.split("node_instance_")
                logger.debug("node_instance: %s from %s", instace,slice_content)
                componentNode={
                    "componentNodeInstanceID": node_instance_id[1],
                    "componentNodeInstanceHexID": slice_content[instace]['hex_ID'],
                    "componentNodeInstanceName": slice_content[instace]['name']
                }
                componentNodeInstances.append(componentNode)
            if instace.split("graph_link_node_instance_")[0] == "":
                if slice_content[instace]['type'] =="CORE":
                    link_instance_id=instace.split("graph_link_node_instance_")
                    logger.debug("link_instance: %s from %s", instace,slice_content)
                    from_node=ast.literal_eval(slice_content[instace]['from_to'])[0]
                    to_node=ast.literal_eval(slice_content[instace]['from_to'])[1]
                    from_hex=slice_content["node_instance_"+str(from_node)]['hex_ID']
                    to_hex=slice_content["node_instance_"+str(to_node)]['hex_ID']
                    graphLinkNode={
                                "graphLinkNodeInstanceID": link_instance_id[1],
                                "fromComponentNodeInstanceHexID": from_node,
                                # [key for key, value in slice_content.items() if value == 2]
                                "fromComponentNodeInstanceID": from_hex,
                                "toComponentNodeInstanceID": to_node,
                                "toComponentNodeInstanceHexID": to_hex,
                                "type": "CORE"
                                }
                    graphLinkNodeInstances.append(graphLinkNode)
        slice_schema={   
        "SliceIntent":{
        "SliceIntentIdentifier":{},
        "ServiceMeshIdentifier":{},
        "Constraints":{
            "ComponentHostingConstraints":{
                "RequirementIdentifier":{},
                "ComponentIdentifier":{},
                "ConstraintType":["CPU","RAM","Storage"]
            },
            "GrapLinkConstrains":{
                "GraphicLinkQosConstraint":{
                    "RequirementIdentifier":{},
                    "GraphLinkIdentifier":{},
                    "ConstraintType":["Delay","Jitter","PacketLoss","Throughput"]

                }
            },
            "AccessConstrains":{
                "AccessQualityProfile":{
                    "QCI":{},
                    "ResourceType":{},
                    "Prioriry":{},
                    "PacketDelayBudget":{},
                    "PacketErrorLossRate":{},
                    "UEType":{}
                }
            }
        },
        "LogicalFunctions":{}
    },
    "ApplicationComponent":{
        "Component":{
            "ComponentIdentifier":{},
            "Distribution":{},
            "ExposedInterface":{
                "InterfaceIdentifier":{},
                "InterfaceType":{},
                "Port":{},
                "TransmissionProtocol":{}
            },
            "Configuration":{},
            "Volume":{},
            "MinimumExecutionRequirements":{
                "VCPUs":{},
                "RAM":{},
                "Storage":{},
                "HypervisorType":{}
            },
            "ExposedMetric":{},
            "RequiredInterface":{
                "GraphLink":{
                    "GraphLinkIdentifier":{},
                    "ComponentIdentifier":{},
                    "InterfaceIdentifier":{}
                }
            },
            "Capability":{}

        }
    },
    "QoSDescriptor":{
        "GraphLinkQoS":{},
        "AccessQos":{}
    }
}

        return componentNode


    #     componentNodeInstances={
    #       "componentNodeInstanceID": "",
    #       "componentNodeInstanceHexID": "",
    #       "componentNodeInstanceName": ""
    #       }
    #     AccessConstrains={
    # "constraintID": "",
    # "interfaceInstanceID": "",
    # "qi": "",
    # "radioServiceType": "",
    # "resourceType": "",
    # "allocationRetentionPriorityProfile": 0,
    # "minimumGuaranteedBandwidth": 0,
    # "maximumRequiredBandwidth": 0,
    # "constraintUnit": "",
    # "category": "ACCESS",
    # "type": ""
    #     }
    #     ComponentHostingConstrains={
    #       "constraintID": "",
    #       "category": "",
    #       "componentNodeInstanceID": "",
    #       "componentNodeInstanceHexID": "",
    #       "type": "",
    #       "constraintMetric": "",
    #       "constraintValue": "",
    #       "constraintUnit": ""
    #     }