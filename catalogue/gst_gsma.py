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
from intent_engine.core import IntentNrm
from intent_engine.core.ib_model import IntentModel

logger = logging.getLogger(__name__)

class gst_gsma(abstract_library):
    """
    Library for 6Green project NEST GSMA intents
    """
    def __init__(self):
        decision_tree={
           "gst" : {
                   "Slice_5ginduce":{"DELIVER":"enif_slice"},
                   "Node_5ginduce":{"DELIVER":"enif_slice"},
                   "LinkNode_5ginduce":{"DELIVER":"enif_slice"},
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
    
    def get_name(self):
        return self.__module_name
    
    def check_import(self):
        print("GST_GSMA imported")

    def isILU(self):
        """
        Return true if this library is able to procces atomic
        intents.
        """
        return self.__isILU
    
    def classifier(self, ib_object : IntentModel):
        return []
    
    def get_decision_tree(self):
        return self.__decision_tree
    
    def generate_subintent(self, intent : IntentModel):
        subintent=intent
        logger.debug("Generate subintent model type: %s",type(subintent))
        return subintent

    def translator(self,subintent : IntentModel) -> tuple[list , str]:
        """
        This functions translate an atomic intent into a CRD L2S-M software
        can understand. This function will decide which functionality (deploy,
        modify, migrate) will be called.

        This decision can be done using the same idea of the decision tree or a more
        direct way.
        """
        # TODO: los subintents direan si hay que desplegar/migrar/eliminar
        # logger.debug("intent model: %s",subintent)
        logger.debug("Intent model type: %s",type(subintent))
        intent = subintent.get_intent()
        params={}
        logger.info("Translating L2S-M...")
        logger.debug("debug L2S-M...")
        for exp in intent.intentExpectations:
            exp_verb=exp.expectationVerb
            logger.debug("expectation case %s",exp_verb)
            # assert isinstance(exp, IntentNrm.L2SMExpectation)
            logger.debug("Expectation type: %s", type(exp))
            match exp_verb:
                case "DELIVER":
                    try:
                        IntentNrm.NewNetworkExpectation(**(exp.dict()))
                    except ValidationError as exc:
                        logger.warning("Assurance error for L2SM NewNetworkExpectation:  %s", exc)
                    exp_obj=exp.expectationObject
                    logger.debug("DELIVER case obj: %s",exp_obj)
                    exp_type=exp_obj.objectType
                    params['service']="create_network"
                    match exp_type:
                        case "L2SM_NETWORK":
                            for obj_ctx in exp_obj.objectContexts:
                                # Loop ctx inside obj
                                logger.debug("objectctx case %s: ",obj_ctx)
                                att=obj_ctx.contextAttribute
                                logger.debug("attobjectctx case %s: ",att)
                                match att:
                                    case "network":
                                        logger.debug("network case")
                                        self.__params['network']=obj_ctx.contextValueRange
                                    case "providerName":
                                        logger.debug("provider case")
                                        self.__params['provider_name']=obj_ctx.contextValueRange
                                    case "domain":
                                        logger.debug("domain case")
                                        self.__params['provider_domain']=obj_ctx.contextValueRange
                                    case _:
                                        logger.debug("NOT matching in case: %s",att)

                    for trg_ctx in exp.expectationTargets:
                        # Loop trg inside exp
                        att=trg_ctx.targetName
                        match att:
                            case "secure":
                                logger.debug("signature case")
                                trg_ctxs=trg_ctx.targetContexts
                                if trg_ctxs:
                                    for trg_ctx in trg_ctxs:
                                        # Loop ctx inside trg inside exp
                                        att=trg_ctx.contextAttribute
                                        match att:
                                            case "publicKey":
                                                logger.debug("signature_trg_ctx case")
               
            for exp_ctx in exp.expectationContexts:
                if isinstance(exp_ctx,IntentNrm.NEMOIntentContext):
                    logger.debug("Url: %s",exp_ctx.contextValueRange)
                    params['url']=exp_ctx.contextValueRange
                    params['headers']={'Content-Type': 'application/x-yaml'}
            params['connector']="l2smmd"
            return [self.l2sm_schema(params['service']),params],"sys_out"

    def create_ilu(self,ilu_ref):
        return ilu_ref

    def l2sm_schema(self, request_type):

        if request_type == "create_network":
            request={
                "network":{
                    "name":self.__params['network'],
                    "provider":{
                        "name": self.__params['provider_name'],
                        "domain":self.__params['provider_domain']
                    },
                    "pod_cidr":""
                }
            }
        if request_type == "delete_network":
            request={"network_name":self.__params['network']}

        return request