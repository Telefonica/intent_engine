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
from abc import ABC, abstractmethod

from intent_engine.catalogue.abstract_library import abstract_library
from intent_engine.core.ib_object import IB_object

logger = logging.getLogger(__name__)

class slice_5g(abstract_library):
    """
    Library for 5G Cumucore network slicing and QoS management.
    Parameters:
    - SUPI: Subscriber identification, for which the dataflow is requested. SUPI
            information needs to be known by the application using the API.
            SUPI information is created to user with a SIM which is used with
            the target UE.
    - Time: Time of the rule exists. Value formatting according to ISO8661
            standard (YYYYMMDDThhmmss±0000)
            Time type
            - Start- stop (START-STOP), bot time fields in use
            - Start - no stop limit (START-FROM), only start time field in
            use
            - Until stop limit (UNTIL-STOP) only stop time field in use
    - profileName: Profile name in the PCF which is to be used for the QoS
      parameters. (5QI class-> GBR / Non GBR, ARP values, etc)
      String value referencing the profile type defined in the PCF for the
      API usage.
    - ulCapacity: Requested Uplink capacity for the dataflow, value in megabits, float
                  value eg 1.5. MAX possible uplink capacity is defined in the profile
                  at PCF
    - dlCapacity: Requested downlink capacity for the dataflow, value in megabits,
                  float value eg 1.5. MAX possible downlink capacity is defined in the
                  profile at PCF.
    - ip4Filters: IP filters for the dataflow, value is table if there are multiple
                  separated addresses in use or separated filter for directions.
                  Filter Type
                  - IN = filter traffic from this address to UE to this dataflow.
                  - OUT = filter traffic going to this address from UE to dataflow.
                  - BOTH = both traffic to/from this address to put to dataflow
                  Address
                  - IP address of the source / target
                  - IP address value can be also range
                  (192.168.10.10-192.168.10.20)
                  - ANY = moves all traffic to dataflow in question
                  Port information
                  - Type of port: TCP, UDP, ANY
                  - Port number (1- 65536) or range ( 1000-1010)
                  - Multiple single port definition for single IP needs own
                  structure for each port definition
    - flowID: Identifies the flow in question to be modified/deleted
    """
    def __init__(self):
        """
        """
        # Careful, example for default parameters to Cumucore API
        params={
  "SUPI": "XYZ123",
  "time": {
    "type": "START-STOP",
    "startime": "20210510T123000-2000",
    "stoptime": "20210510T134500-2000"
  },
  "profileName": "audio128k",
  "ulCapacity": "0.2",
  "dlCapacity": "0.2",
  "ip4Filters": [
    {
      "type": "BOTH",
      "ip4Address": "192.168.10.10",
      "portType": "TCP",
      "portNumber": "1000-1005"
    }
  ]
}
        decision_tree={
            "cloud_continuum" : {
               "nemo_deployment":{
                   "5g_slice_flow":{
                       "create":["slice_5g"]}
                    },
                "mininet": "mininet_controller"
                }
        }
        super().__init__(module_name="slice_5g",isILU=False,params=params,decision_tree=decision_tree)
        self.__params=params
 
    def translator(self,subintent : IB_object)-> tuple[list , str]:
        exec_params=[]
        logger.info("Translating slice_5g...")
        logger.debug("debug slice_5g...")
        for exp in subintent.get_expectations():
            exp_verb=exp.get_verb()
            logger.debug("expectation case %s",exp_verb)
            match exp_verb:
                case "create":
                    exp_obj=exp.get_object()
                    logger.debug("create case obj: %s",exp_obj)
                    exp_type=exp_obj.get_type()
                    match exp_type:
                        case "5g_slice_flow":
                            # Possible list of ipv4 filters
                            ip4filters=[]
                            for obj_ctx in exp_obj.get_contexts():
                                # Loop ctx inside obj
                                # Filter
                                ipv4filter={}
                                logger.debug("objectctx case %s: ",obj_ctx)
                                att=obj_ctx.get_attribute()
                                # several filters have to be referenced so matching
                                # between ip,port,type
                                match att:
                                    case "ip4Address":
                                        logger.debug("ip4Address case %s",obj_ctx.get_value_range())
                                        ipv4filter['ip4Address']=obj_ctx.get_value_range()
                                        logger.debug("params after %s",self.__params)
                                    case "type":
                                        logger.debug("type case")
                                        ipv4filter['type']=obj_ctx.get_value_range()
                                    case "portNumber":
                                        logger.debug("portNumber case")
                                        ipv4filter['portNumber']=obj_ctx.get_value_range()
                                    case "portType":
                                        logger.debug("portType case")
                                        ipv4filter['portType']=obj_ctx.get_value_range()
                                # append to ipv4 filters althoug functionality not jet #TODO
                                ip4filters.append(ipv4filter)
                            self.__params['ipv4filters']=ip4filters
                    for exp_trg in exp.get_target():
                        # Loop trg inside exp
                        att=exp_trg.get_attribute()
                        match att:
                            case "ulCapacity":
                                logger.debug("ulCapacity case")
                                self.__params['ulCapacity']=exp_trg.get_value_range()
                                exp_trg_ctx=exp_trg.get_context()
                                if exp_trg_ctx:
                                    for ctx in exp_trg_ctx:
                                        # Loop ctx inside trg inside exp
                                        att=ctx.get_attribute()
                                        match att:
                                            case "profile":
                                                logger.debug("profile_exp_trg_ctx case")
                                                self.__params['profile']=ctx.get_value_range()
                                                self.__params['SUPI']=ctx.get_name()
                            case "dlCapacity":
                                logger.debug("dlCapacity case")
                                exp_trg_ctx=exp_trg.get_context()
                                self.__params['dlCapacity']=exp_trg.get_value_range()
                                if exp_trg_ctx:
                                    for ctx in exp_trg_ctx:
                                        # Loop ctx inside trg inside exp
                                        att=ctx.get_attribute()
                                        match att:
                                            case "profile":
                                                logger.debug("profile_exp_trg_ctx case")

        # esto debería context del intent
        match subintent.get_context().get_name():
            case "nemo_deployment":
                logger.debug("intent context tfs controller case")
                match subintent.get_context().get_attribute():
                    case "instantceid":
                        logger.debug("intent context att 5g slice case")
                        # maybe here store in database by id?
        return [self.__params,exec_params],"sysout"
