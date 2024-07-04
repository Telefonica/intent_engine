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
from intent_engine.core.ib_model import IntentModel

logger = logging.getLogger(__name__)

class gst_gsma(abstract_library):
    """
    Library for 6Green project
    """
    def __init__(self):
        decision_tree={
           "gst" : {
               "intent_id":{
                   "slice_intent":{
                       "deploy": "slice"} #mirar esto
                    }
                }
        }
        params={}
        self.__gst_to_3gpp={
            "dLThptPerSlice":"ServiceProfile",
            "dLThptPerUE":"ServiceProfile",
            "uLThptPerSlice":"ServiceProfile",
            "uLThptPerUE":"ServiceProfile",
            "maxNumberofPDUSessions":"ServiceProfile",
        }

        # self.__gst_3gpp_performance={
        #     "TopSliceSubnetProfile":{
        #         "dLThptPerSliceSubnet":"",
        #         "dLThptPerUE":"",
        #         "uLThptPerSliceSubnet":"",
        #         "uLThptPerUE":"",
        #     },
        #     "ServiceProfile":{
        #         "dLThptPerSlice":"",
        #         "dLThptPerUE":"",
        #         "uLThptPerSlice":"",
        #         "uLThptPerUE":"",
        #     },
        #     "NetworkSliceSubnetProviderCapabilities":{
        #         "dLlatency":"",
        #         "uLlatency":"",
        #         "dLThptPerSliceSubnet":"",
        #         "uLThptPerSliceSubnet":"",
        #         "coverageAreaTAList":""
        #     }
        # }
        super().__init__(module_name="gst_gsma",isILU=True,params=params,decision_tree=decision_tree)
        self.__params=params
    
    def translator(self,subintent : IB_object) -> tuple[list , str]:
        exec_params=[]
        params={}
        instances={}
        logger.info("Translating gst_gsma...")
        logger.debug("debug gst_gsma connector...")
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
                        case "slice":
                            for obj_ctx in exp_obj.get_contexts():
                                # Loop ctx inside obj
                                logger.debug("objectctx case %s: ",obj_ctx)
                                att=obj_ctx.get_attribute()
                                for gst_att in self.__gst_to_3gpp:
                                    logger.debug("name case %s",obj_ctx.get_value_range())
                                    self.__params[gst_att]=obj_ctx.get_value_range()
                                    logger.debug("params after %s",self.__params)
                                    if obj_ctx.get_name() not in instances.keys():
                                        instances[obj_ctx.get_name()]={}
                                    instances[obj_ctx.get_name()][gst_att]=obj_ctx.get_value_range()
                    for trg_ctx in exp.get_target():
                        # Loop trg inside exp
                        att=trg_ctx.get_attribute()
                        for gst_target in gst_att:
                            trg_ctx=trg_ctx.get_context()
                            logger.debug("gst targets %s",gst_target)
                            if trg_ctx:
                                for ctx in trg_ctx:
                                    # Loop ctx inside trg inside exp
                                    att=ctx.get_attribute()
                                    
                    for exp_ctx in exp.get_context():
                        att=exp_ctx.get_attribute()
                        match att:
                            case "user":
                                logger.debug("user case")
                                params['user']=exp_ctx.get_value_range()

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

    def generate_subintent(self,intent:IB_object) -> IB_object:
        """
        Return sub intents of a slice in a green context.
        """
        ilu="enif_slice"

        return intent,ilu
    
    def slice_schema(self, slice_content: dict):
        return slice_content