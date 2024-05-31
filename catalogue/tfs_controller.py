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

class tfs_controller(abstract_library):
    """
    Abstract class created as 
    """
    def __init__(self):
        decision_tree={
           "cloud_continuum" : {
               "tfs_controller":{
                   "l2vpn":{
                       "request":["tfs_controller"]}
                    }
                }
        }
        params={
            "context_uuid":"admin",
            "service_uuid":"l2-acl-svc-intent",
            "node_src":"5.5.5.5",
            "endpoint_src":"GigabitEthernet0/0/0/1", #Endpoint to tfs format?
            "node_dst":"3.3.3.3",
            "endpoint_dst":"GigabitEthernet0/0/0/1",
            "bandwidth":"10.0",
            "latency":"15.2",
            "vlan_id":999,
            "circuit_id":"999",
            "ni_name":"ninametfssssss"
        }
        super().__init__(module_name="tfs_controller",isILU=True,params=params,decision_tree=decision_tree)
        self.__params=params
    
    def translator(self,subintent : IB_object) -> tuple[list , str]:
        # TODO: cambiar el connect_type dependiendo del intent de  tfs session
        exec_params=[]
        params={}
        logger.info("Translating TFS connector...")
        logger.debug("debug TFS connector...")
        for exp in subintent.get_expectations():
            exp_verb=exp.get_verb()
            logger.debug("expectation case %s",exp_verb)
            match exp_verb:
                case "request":
                    exp_obj=exp.get_object()
                    logger.debug("request case obj: %s",exp_obj)
                    exp_type=exp_obj.get_type()
                    match exp_type:
                        case "l2vpn":
                            for obj_ctx in exp_obj.get_contexts():
                                # Loop ctx inside obj
                                logger.debug("objectctx case %s: ",obj_ctx)
                                att=obj_ctx.get_attribute()
                                match att:
                                    case "node_src":
                                        logger.debug("node_src case %s",obj_ctx.get_value_range())
                                        self.__params['node_src']=obj_ctx.get_value_range()
                                        logger.debug("params after %s",self.__params)
                                    case "node_dst":
                                        logger.debug("node_dst case")
                                        self.__params['node_dst']=obj_ctx.get_value_range()
                                    case "vlan_id":
                                        logger.debug("vlan_id case")
                                        self.__params['vlan_id']=obj_ctx.get_value_range()
                    for trg_ctx in exp.get_target():
                        # Loop trg inside exp
                        att=trg_ctx.get_attribute()
                        match att:
                            case "signature":
                                logger.debug("signature case")
                        trg_ctx=trg_ctx.get_context()
                        if trg_ctx:
                            for ctx in trg_ctx:
                                # Loop ctx inside trg inside exp
                                att=ctx.get_attribute()
                                match att:
                                    case "signature":
                                        logger.debug("signature_trg_ctx case")
                    
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
        match subintent.get_context().get_name():
            case "tfs_controller":
                logger.debug("intent context tfs controller case")
                match subintent.get_context().get_attribute():
                    case "state":
                        logger.debug("intent context att state case")
                    case "permits":
                        logger.debug("intent context att permits case")

        return [self.vpnl2_schema(),params],"sysout"

    def ietf_l2vpn_schema(self):
        ietf_l2vpn={
            
        }
        return 
    def vpnl2_schema(self):

        vpn_descriptor={
                        "services": [
                            {
                                "service_id": {
                                    "context_id": {"context_uuid": {"uuid": self.__params['context_uuid']}},
                                    "service_uuid": {"uuid": self.__params['service_uuid']}
                                },
                                "service_type": 2,
                                "service_status": {"service_status": 1},
                                "service_endpoint_ids": [
                                    {"device_id": {"device_uuid": {"uuid": self.__params['node_src']}}, "endpoint_uuid": {"uuid": "0/0/1-"+self.__params['endpoint_src']}},
                                    {"device_id": {"device_uuid": {"uuid": self.__params['node_dst']}}, "endpoint_uuid": {"uuid": "0/0/1-"+self.__params['endpoint_dst']}}
                                ],
                                "service_constraints": [
                                    {"custom": {"constraint_type": "bandwidth[gbps]", "constraint_value": self.__params['bandwidth']}},
                                    {"custom": {"constraint_type": "latency[ms]", "constraint_value": self.__params['latency']}}
                                ],
                                "service_config": {"config_rules": [
                                    {"action": 1, "custom": {"resource_key": "/settings", "resource_value": {
                                    }}},
                                    {"action": 1, "custom": {"resource_key": "/device["+self.__params['node_src']+"]/endpoint[0/0/1-"+self.__params['endpoint_src']+"]/settings", "resource_value": {
                                        "sub_interface_index": 0,
                                        "ni_name":self.__params['ni_name'],
                                        "vlan_id": int(self.__params['vlan_id']),
                                        "circuit_id": self.__params['circuit_id'],
                                        "remote_router":self.__params['node_dst']
                                    }}},
                                    {"action": 1, "custom": {"resource_key": "/device["+self.__params['node_dst']+"]/endpoint[0/0/1-"+self.__params['endpoint_dst']+"]/settings", "resource_value": {
                                        "sub_interface_index": 0,
                                        "ni_name":self.__params['ni_name'],
                                        "vlan_id": int(self.__params['vlan_id']),
                                        "circuit_id": self.__params['circuit_id'],
                                        "remote_router":self.__params['node_src']
                                    }}}
                                ]}
                            }
                        ]
                    }

        return vpn_descriptor
