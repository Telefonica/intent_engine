#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
from typing import List

from devtools import pprint
from intent_engine.catalogue.abstract_library import abstract_library
from intent_engine.core import IntentNrm
from intent_engine.core.ib_model import IntentModel, jsonable_model_encoder
from intent_engine.core.database_utils import create_intent_graph, store_graph_in_graphdb

logger = logging.getLogger(__name__)

class nsmf(abstract_library):
    """
    Library for 6Green project NSMF component
    """
    def __init__(self):
        params={}
        decision_tree={
           "green" : {
               "Slice_Energy_Saving":{
                    "ENSURE":"green_bssf",
                    "DELIVER":"slice"
                },
                "Slice_nsmf":{
                    "ENSURE":"green_bssf",
                    "DELIVER":
                        {"NSFM_SESSION":"nsmf",
                         "NSFM_SLICE":"nsmf"},
                }
           }
        }
        super().__init__(module_name="nsmf",isILU=True,params=params,decision_tree=decision_tree)
        self.__params=params

    def generate_subintent(self,intent : IntentModel):
        subintent=intent
        logger.debug("Generate subintent model type: %s",type(subintent))
        return subintent
    def translator(self,subintent : IntentModel) -> tuple[list , str]:
        """
        Translate the subintent to a concrete order.
        """
        logger.debug("Translating subintent...")
        intent=subintent.get_intent()
        intent_dict=intent.dict(exclude_defaults=True)
        logger.debug("Intent dict: %s",intent_dict)
        params={}

        for exp in intent.intentExpectations:
            exp_verb=exp.expectationVerb
            logger.debug("expectation case %s",exp_verb)
            # assert isinstance(exp, IntentNrm.L2SMExpectation)
            logger.debug("Expectation type: %s", type(exp))
            match exp_verb:
                case "DELIVER":
                    # try:
                    #     IntentNrm.NewNetworkExpectation(**(exp.dict()))
                    # except ValidationError as exc:
                    #     logger.warning("Assurance error for L2SM NewNetworkExpectation:  %s", exc)
                    exp_obj=exp.expectationObject
                    logger.debug("DELIVER case obj: %s",exp_obj)
                    exp_type=exp_obj.objectType
                    params['service']="create_network" # TODO: only create slice?
                    match exp_type:
                        case "NSMF_SLICE":
                            for obj_ctx in exp_obj.objectContexts:
                                # Loop ctx inside obj
                                logger.debug("objectctx case %s: ",obj_ctx)
                                att=obj_ctx.contextAttribute
                                logger.debug("attobjectctx case %s: ",att)
                                match att:
                                    case "sst":
                                        logger.debug("sst case")
                                        self.__params['sst']=obj_ctx.contextValueRange
                                    case "isolation-model":
                                        logger.debug("isolation-model")
                                        self.__params['isolation-model']=obj_ctx.contextValueRange
                                    case "plmn":
                                        logger.debug("plmn case")
                                        self.__params['plmn']=obj_ctx.contextValueRange # This is directly a dict
                                    case _:
                                        logger.debug("NOT matching in case: %s",att)

                    for trg_ctx in exp.expectationTargets:
                        # Loop trg inside exp
                        att=trg_ctx.targetName
                        match att:
                            case "dLAmbr":
                                logger.debug("dLAmbr case")
                                trg_ctxs=trg_ctx.targetContexts
                                if trg_ctxs: # Not targets in principle
                                    for trg_ctx in trg_ctxs:
                                        # Loop ctx inside trg inside exp
                                        att=trg_ctx.contextAttribute
                                        match att:
                                            case "area":
                                                logger.debug("area case")
                            case "uLAmbr":
                                logger.debug("uLAmbr case")
                                trg_ctxs=trg_ctx.targetContexts
                                if trg_ctxs: # Not targets in principle
                                    for trg_ctx in trg_ctxs:
                                        # Loop ctx inside trg inside exp
                                        att=trg_ctx.contextAttribute
                                        match att:
                                            case "area":
                                                logger.debug("area case")
                
            for exp_ctx in exp.expectationContexts:
                if isinstance(exp_ctx,IntentNrm.GreenIntentContext): # placeholder
                    logger.debug("Url: %s",exp_ctx.contextValueRange)
                    params['url']=exp_ctx.contextValueRange
                    params['headers']={'Content-Type': 'application/x-yaml'}
                
                match exp_ctx.contextAttribute:
                    case "name":
                        self.__params['name']=exp_ctx.contextValueRange
                        logger.debug("Region name: %s",self.__params['name'])
                    case "user-density":
                        self.__params['user-density']=exp_ctx.contextValueRange
                        logger.debug("User density: %s",self.__params['user-density'])
                        
        for ctx in intent.intentContexts:
            match ctx.contextAttribute:
                case "name":
                    logger.debug("intent context name case")
                case "namespace":
                    logger.debug("intent context namespace case")

        params['connector']="nsmf"
        return [self.nsmf_schema(params['service']),params],"sys_out"
    

    def nsmf_schema(self, params):
        """
        Create a schema for the NSMF component.
        """
        schema = {
            "apiVersion": "athena.trirematics.io/v1",
            "kind": "Slice",
            "metadata": {
                "name": params.get("name", ""),
                "namespace": params.get("namespace", "")
            },
            "spec": {
                "slices": []
            }
        }

        slice_spec = {
            "regions": [],
            "isolation-model": {
                "private-sectors": params.get("isolation-model", [])
            },
            "plmn": params.get("plmn", {}),
            "sst": params.get("sst", ""),
            "sd": params.get("sd", ""),
            "ambr": {
                "downlink": params.get("dLAmbr", ""),
                "uplink": params.get("uLAmbr", "")
            },
            "sessions": []
        }

        for region in params.get("regions", []):
            region_spec = {
                "name": region.get("name", ""),
                "user-density": region.get("user-density", "")
            }
            slice_spec["regions"].append(region_spec)

        for session in params.get("sessions", []):
            session_spec = {
                "id": session.get("id", ""),
                "type": session.get("type", ""),
                "dnn": session.get("dnn", ""),
                "ambr": {
                    "downlink": session.get("dLAmbr", ""),
                    "uplink": session.get("uLAmbr", "")
                },
                "flows": []
            }

            for flow in session.get("flows", []):
                flow_spec = {
                    "qfi": flow.get("qfi", ""),
                    "quality": flow.get("quality", ""),
                    "arp": {
                        "priority-level": flow.get("priority-level", ""),
                        "preemption-capability": flow.get("preemption-capability", ""),
                        "preemption-vulnerability": flow.get("preemption-vulnerability", "")
                    },
                    "gbr": {
                        "downlink": flow.get("dLGbr", ""),
                        "uplink": flow.get("uLGbr", "")
                    },
                    "mbr": {
                        "downlink": flow.get("dLMbr", ""),
                        "uplink": flow.get("uLMbr", "")
                    },
                    "plr": flow.get("plr", "")
                }
                session_spec["flows"].append(flow_spec)

            slice_spec["sessions"].append(session_spec)

        schema["spec"]["slices"].append(slice_spec)

        return schema