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
from intent_engine.core.ib_object import IB_object

logger = logging.getLogger(__name__)

class enif_slice(abstract_library):
    """
    Library for 6Green project
    """
    def __init__(self):
        decision_tree={
           "green" : {
               "intent_id":{
                   "slice_intent_5ginduce":{
                       "deploy": "enif_slice"} #mirar esto
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
    
    def translator(self,subintent : IB_object) -> tuple[list , str]:
        # TODO: cambiar el connect_type dependiendo del intent de  tfs session
        exec_params=[]
        params={}
        instances={}
        logger.info("Translating enif_slice...")
        logger.debug("debug enif_slice connector...")
        logger.debug("subint: %s",subintent.get_expectations())
        for exp in subintent.get_expectations():
            exp_verb=exp.get_verb()
            logger.debug("expectation case %s",exp_verb)
            match exp_verb:
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
                logger.debug("intent context tfs controller case")
                match subintent.get_context().get_attribute():
                    case "state":
                        logger.debug("intent context att state case")
                    case "permits":
                        logger.debug("intent context att permits case")

        return [self.slice_schema(instances),params],"sysout"

    def generate_subintent(self,intent:IB_object) -> IB_object:
        """
        Return sub intents of a slice in a green context.
        """
        ilu="enif_slice"

        return intent,ilu
    
    def slice_schema(self, slice_content):

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

        return slice_schema
