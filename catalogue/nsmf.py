#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
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
                "ENSURE":{"NSMF_SESSION":"nsmf"},
                "DELIVER":
                    {"NSMF_SESSION":"nsmf",
                        "NSMF_SLICE":"nsmf"},

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
        
        slices=[] # Each expectation is a region
        sessions=[] # Each expectation has a session
        slices_sessions={}
        
        for exp in intent.intentExpectations:
            slice_region={}
            slice_session={}
            for exp_ctx in exp.expectationContexts:
                if isinstance(exp_ctx,IntentNrm.GreenIntentContext): # placeholder
                    logger.debug("Url: %s",exp_ctx.contextValueRange)
                    params['url']=exp_ctx.contextValueRange
                    params['headers']={'Content-Type': 'application/x-yaml'} # - 

                match exp_ctx.contextAttribute:
                    case "name":
                        slice_region['name']=exp_ctx.contextValueRange
                        slice_session['name']=exp_ctx.contextValueRange
                        logger.debug("Region name: %s",slice_region['name'])
                    case "user-density":
                        slice_region['user-density']=exp_ctx.contextValueRange
                        slice_session['user-density']=exp_ctx.contextValueRange
                        logger.debug("User density: %s",slice_region['user-density'])

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
                                        slice_region['sst']=obj_ctx.contextValueRange
                                    case "isolation-model":
                                        logger.debug("isolation-model")
                                        if 'isolation-model' not in slice_region:
                                            slice_region['isolation-model'] = {}
                                        slice_region['isolation-model']['private-sectors'] = obj_ctx.contextValueRange
                                    case "plmn":
                                        logger.debug("plmn case")
                                        slice_region['plmn']=obj_ctx.contextValueRange # This is directly a dict
                                    case _:
                                        logger.debug("NOT matching in case: %s",att)

                            for exp_trg in exp.expectationTargets:
                                # Loop trg inside exp
                                att=exp_trg.targetName
                                match att:
                                    case "dLAmbr":
                                        logger.debug("dLAmbr case")
                                        # trg_ctxs=exp_trg.targetContexts
                                        if 'ambr' not in slice_region:
                                            slice_region['ambr'] = {}
                                        slice_region['ambr']['downlink']=exp_trg.targetValueRange
                                    case "uLAmbr":
                                        logger.debug("uLAmbr case")
                                        # trg_ctxs=trg_ctx.targetContexts
                                        if 'ambr' not in slice_region:
                                            slice_region['ambr'] = {}
                                        slice_region['ambr']['uplink']=exp_trg.targetValueRange
                            slices.append(slice_region)
                            # pprint(slices)

                        case "NSMF_SESSION":
                            # DUPLICATED IN CASE NSMFSESiON IS DELIVER not ENSURE VERB
                            for obj_ctx in exp_obj.objectContexts:
                                # Loop ctx inside obj
                                logger.debug("objectctx case %s: ",obj_ctx)
                                att=obj_ctx.contextAttribute
                                logger.debug("attobjectctx case %s: ",att)
                                match att:
                                    case "id":
                                        logger.debug("id case")
                                        slice_session['id']=obj_ctx.contextValueRange
                                    case "type":
                                        logger.debug("type case")
                                        slice_session['type']=obj_ctx.contextValueRange
                                    case "dnn":
                                        logger.debug("dnn case")
                                        slice_session['dnn']=obj_ctx.contextValueRange
                                    case _:
                                        logger.debug("NOT matching in case: %s",att)

                            for exp_trg in exp.expectationTargets:
                                # Loop trg inside exp
                                flows=[]
                                flow={}
                                att=exp_trg.targetName
                                match att:
                                    case "dLAmbr":
                                        logger.debug("dLAmbr case")
                                        trg_ctxs=exp_trg.targetContexts
                                        slice_session['ambr']['downlink']=exp_trg.targetValueRange
                                    case "uLAmbr":
                                        logger.debug("uLAmbr case")
                                        trg_ctxs=exp_trg.targetContexts
                                        slice_session['ambr']['uplink']=exp_trg.targetValueRange
                                    case "qfi":
                                        logger.debug("qfi case")
                                        if trg_ctx.targetContexts:
                                            for trg_ctx in exp_trg.targetContexts:
                                                att=trg_ctx.contextAttribute
                                                match att:
                                                    case "flow":
                                                        logger.debug("flow case")
                                                        flow_id=trg_ctx.contextValueRange
                                        flow[flow_id]['qfi']=exp_trg.targetValueRange
                                    case "quality":
                                        logger.debug("quality case")
                                        if trg_ctx.targetContexts:
                                            for trg_ctx in exp_trg.targetContexts:
                                                att=trg_ctx.contextAttribute
                                                match att:
                                                    case "flow":
                                                        logger.debug("flow case")
                                                        flow_id=trg_ctx.contextValueRange
                                        flow[flow_id]['quality']=exp_trg.targetValueRange
                                    case "arpPriorityLevel":
                                        logger.debug("arpPriorityLevel case")
                                        if trg_ctx.targetContexts:
                                            for trg_ctx in exp_trg.targetContexts:
                                                att=trg_ctx.contextAttribute
                                                match att:
                                                    case "flow":
                                                        logger.debug("flow case")
                                                        flow_id=trg_ctx.contextValueRange
                                        flow[flow_id]['arp']['priority-level']=exp_trg.targetValueRange
                                    case "arpPreemptionCapability":
                                        logger.debug("arpPreemptionCapability case")
                                        if trg_ctx.targetContexts:
                                            for trg_ctx in exp_trg.targetContexts:
                                                att=trg_ctx.contextAttribute
                                                match att:
                                                    case "flow":
                                                        logger.debug("flow case")
                                                        flow_id=trg_ctx.contextValueRange
                                        flow[flow_id]['arp']['preemption-capability']=exp_trg.targetValueRange
                                    case "arpPreemptionVulnerability":
                                        logger.debug("arpPreemptionVulnerability case")
                                        if trg_ctx.targetContexts:
                                            for trg_ctx in exp_trg.targetContexts:
                                                att=trg_ctx.contextAttribute
                                                match att:
                                                    case "flow":
                                                        logger.debug("flow case")
                                                        flow_id=trg_ctx.contextValueRange
                                        flow[flow_id]['arp']['preemption-vulnerability']=exp_trg.targetValueRange
                                    case "dLGbr":
                                        logger.debug("dLGbr case")
                                        slice_session['gbr']['downlink']=exp_trg.targetValueRange
                                    case "uLGbr":
                                        logger.debug("uLGbr case")
                                        slice_session['gbr']['uplink']=exp_trg.targetValueRange
                                    case "dLMbr":
                                        logger.debug("dLMbr case")
                                        slice_session['mbr']['downlink']=exp_trg.targetValueRange
                                    case "uLMbr":
                                        logger.debug("uLMbr case")
                                        slice_session['mbr']['uplink']=exp_trg.targetValueRange
                                    case "plr":
                                        logger.debug("plr case")
                                        slice_session['plr']=exp_trg.targetValueRange
                                    case _:
                                        logger.debug("NOT matching in case: %s",att)
                                # slice_session['flows'].append(flow)
                                # pprint(slice_session)
                            slice_session['flows'].append(flow)
                            sessions.append(slice_session)

                case "ENSURE":
                    exp_obj=exp.expectationObject
                    logger.debug("DELIVER case obj: %s",exp_obj)
                    exp_type=exp_obj.objectType
                    params['service']="create_network" # TODO: only create slice?
                    match exp_type:
                        case "NSMF_SESSION":
                            for obj_ctx in exp_obj.objectContexts:
                                # Loop ctx inside obj
                                logger.debug("objectctx case %s: ",obj_ctx)
                                att=obj_ctx.contextAttribute
                                logger.debug("attobjectctx case %s: ",att)
                                match att:
                                    case "id":
                                        logger.debug("id case")
                                        slice_session['id']=obj_ctx.contextValueRange
                                    case "type":
                                        logger.debug("type case")
                                        slice_session['type']=obj_ctx.contextValueRange
                                    case "dnn":
                                        logger.debug("dnn case")
                                        slice_session['dnn']=obj_ctx.contextValueRange
                                    case _:
                                        logger.debug("NOT matching in case: %s",att)
                            flows=[]
                            flow={}
                            for exp_trg in exp.expectationTargets:
                                # Loop trg inside exp
                                # pprint("START FOR ")
                                # pprint(flow)
                                att=exp_trg.targetName
                                                
                                match att:
                                    case "dLAmbr":
                                        logger.debug("dLAmbr case")
                                        # trg_ctxs=exp_trg.targetContexts
                                        if 'ambr' not in slice_session:
                                            slice_session['ambr'] = {}
                                        slice_session['ambr']['downlink']=exp_trg.targetValueRange
                                    case "uLAmbr":
                                        logger.debug("uLAmbr case")
                                        if 'ambr' not in slice_session:
                                            slice_session['ambr'] = {}
                                        slice_session['ambr']['uplink']=exp_trg.targetValueRange
                                    case "qfi":
                                        logger.debug("qfi case")
                                        if exp_trg.targetContexts:
                                            for trg_ctx in exp_trg.targetContexts:
                                                att=trg_ctx.contextAttribute
                                                match att:
                                                    case "flow":
                                                        logger.debug("flow case")
                                                        flow_id=trg_ctx.contextValueRange
                                        if str(flow_id) not in flow:
                                            flow[str(flow_id)]={}
                                        flow[str(flow_id)]['qfi']=exp_trg.targetValueRange
                                    case "quality":
                                        logger.debug("quality case")
                                        if exp_trg.targetContexts:
                                            for trg_ctx in exp_trg.targetContexts:
                                                att=trg_ctx.contextAttribute
                                                match att:
                                                    case "flow":
                                                        logger.debug("flow case")
                                                        flow_id=trg_ctx.contextValueRange
                                        if str(flow_id) not in flow:
                                            flow[str(flow_id)]={}
                                        flow[str(flow_id)]['quality']=exp_trg.targetValueRange
                                    case "arpPriorityLevel":
                                        logger.debug("arpPriorityLevel case")
                                        if exp_trg.targetContexts:
                                            for trg_ctx in exp_trg.targetContexts:
                                                att=trg_ctx.contextAttribute
                                                match att:
                                                    case "flow":
                                                        logger.debug("flow case")
                                                        flow_id=trg_ctx.contextValueRange
                                        if str(flow_id) not in flow:
                                            flow[str(flow_id)]={}
                                        if 'arp' not in flow[str(flow_id)] and str(flow_id) in flow:
                                            flow[str(flow_id)]['arp']={}
                                        if str(flow_id) in flow and 'arp' in flow[str(flow_id)]:
                                            if 'priority-level' not in flow[str(flow_id)]['arp']:
                                                flow[str(flow_id)]['arp']['priority-level']={}
                                        flow[str(flow_id)]['arp']['priority-level']=exp_trg.targetValueRange
                                    case "arpPreemptionCapability":
                                        logger.debug("arpPreemptionCapability case")
                                        if exp_trg.targetContexts:
                                            for trg_ctx in exp_trg.targetContexts:
                                                att=trg_ctx.contextAttribute
                                                match att:
                                                    case "flow":
                                                        logger.debug("flow case")
                                                        flow_id=trg_ctx.contextValueRange
                                        if str(flow_id) not in flow:
                                            flow[str(flow_id)]={}
                                        if 'arp' not in flow[str(flow_id)] and str(flow_id) in flow:
                                            flow[str(flow_id)]['arp']={}
                                        if str(flow_id) in flow and 'arp' in flow[str(flow_id)]:
                                            flow[str(flow_id)]['arp']['preemption-capability']={}
                                        flow[str(flow_id)]['arp']['preemption-capability']=exp_trg.targetValueRange
                                    case "arpPreemptionVulnerability":
                                        logger.debug("arpPreemptionVulnerability case")
                                        if exp_trg.targetContexts:
                                            for trg_ctx in exp_trg.targetContexts:
                                                att=trg_ctx.contextAttribute
                                                match att:
                                                    case "flow":
                                                        logger.debug("flow case")
                                                        flow_id=trg_ctx.contextValueRange
                                        if str(flow_id) not in flow:
                                            flow[str(flow_id)]={}
                                        if 'arp' not in flow[str(flow_id)] and str(flow_id) in flow:
                                            flow[str(flow_id)]['arp']={}
                                        if str(flow_id) in flow and 'arp' in flow[str(flow_id)]:
                                            flow[str(flow_id)]['arp']['preemption-vulnerability']={}
                                        flow[str(flow_id)]['arp']['preemption-vulnerability']=exp_trg.targetValueRange
                                    case "dLGbr":
                                        logger.debug("dLGbr case")
                                        if 'gbr' not in slice_session:
                                            slice_session['gbr'] = {}
                                        slice_session['gbr']['downlink']=exp_trg.targetValueRange
                                    case "uLGbr":
                                        logger.debug("uLGbr case")
                                        if 'gbr' not in slice_session:
                                            slice_session['gbr'] = {}
                                        slice_session['gbr']['uplink']=exp_trg.targetValueRange
                                    case "dLMbr":
                                        logger.debug("dLMbr case")
                                        if 'mbr' not in slice_session:
                                            slice_session['mbr'] = {}
                                        slice_session['mbr']['downlink']=exp_trg.targetValueRange
                                    case "uLMbr":
                                        logger.debug("uLMbr case")
                                        if 'mbr' not in slice_session:
                                            slice_session['mbr'] = {}
                                        slice_session['mbr']['uplink']=exp_trg.targetValueRange
                                    case "plr":
                                        logger.debug("plr case")
                                        if 'plr' not in slice_session:
                                            slice_session['plr'] = {}
                                        slice_session['plr']=exp_trg.targetValueRange
                                    case _:
                                        logger.debug("NOT matching in case: %s",att)
                                if 'flows' not in slice_session:
                                    slice_session['flows']=[]
                                
                                # pprint(slice_session)
                            slice_session['flows'].append(flow)
                            slices.append(slice_session)
            # pprint(slice_region)
            # pprint(slice_session)
        # slices['sessions']=sessions
        self.__params['slices']=slices
        self.__params['sessions']=sessions
        
        for ctx in intent.intentContexts:
            match ctx.contextAttribute:
                case "name":
                    logger.debug("intent context name case")
                    self.__params['name']=ctx.contextValueRange
                case "namespace":
                    logger.debug("intent context namespace case")
                    self.__params['namespace']=ctx.contextValueRange

        params['connector']="nsmf"
        # pprint(self.__params)
        return [self.nsmf_schema(params['service']),params],"sys_out"
    

    def nsmf_schema(self, service):
        """
        Create a schema for the NSMF component.
        """
        region_type=[]
        session_type=[]
        for type_a in self.__params.get("slices", []):
            if 'sst' in type_a:
                region_type.append(type_a)
                logger.debug("Type_a type appended")
        for type_b in self.__params.get("slices", []):
            if 'flows' in type_b:
                logger.debug("Type_b type appended")
                session_type.append(type_b)

        for region in region_type:
            for session in session_type:
                if region['name']==session['name']:
                    logger.debug("Region and session match")
                    pprint(region)
                    pprint("---------")
                    pprint(session)
                    flows=[]
                    for flow in session.get("flows", []):
                        for key in flow.keys():
                            logger.debug("Key: %s",key)
                            pprint("----flow-----")
                            pprint(flow[key]['arp'])
                            unique_flow = {
                                "qfi": flow[key].get("qfi", ""),
                                "quality": flow[key].get("quality", ""),
                                "arp": {
                                    "priority-level": (flow[key]['arp']).get("priority-level", ""),
                                    "preemption-capability": (flow[key]['arp']).get("preemption-capability"),
                                    "preemption-vulnerability": (flow[key]['arp']).get("preemption-vulnerability")
                                },
                                "gbr": {
                                    "downlink": session['gbr'].get("downlink", ""),
                                    "uplink": session['gbr'].get("uplink", "")
                                },
                                "mbr": {
                                    "downlink": session['mbr'].get("downlink", ""),
                                    "uplink": session['mbr'].get("uplink", "")
                                },
                                "plr": session.get("plr", "")
                            }
                            flows.append(unique_flow)
                    session_spec = {
                        "id": session.get("id", ""),
                        "type": session.get("type", ""),
                        "dnn": session.get("dnn", ""),
                        "ambr": {
                            "downlink": session['ambr'].get("downlink", ""),
                            "uplink": session['ambr'].get("uplink", "")
                        },
                        "flows": flows
                    }
                    
                    slice_spec = {
                    "name": region.get("name", ""),
                    "user-density": region.get("user-density", ""),
                    "isolation-model": {
                        "private-sectors": json.loads(region['isolation-model'].get("private-sectors", ""))
                    },
                    "plmn": json.loads(region.get("plmn", {})),
                    "sst": region.get("sst", ""),
                    "sd": region.get("sd", ""),
                    "ambr": {
                        "downlink": region['ambr'].get("downlink", ""),
                        "uplink": region['ambr'].get("uplink", "")
                    },
                    "sessions": []
                }
                    slice_spec["sessions"].append(session_spec)
                
        schema = {
            "apiVersion": "athena.trirematics.io/v1",
            "kind": "Slice",
            "metadata": {
                "name": self.__params.get("name", ""),
                "namespace": self.__params.get("namespace", "")
            },
            "spec": {
                "slices": []
            }
        }
        schema["spec"]["slices"].append(slice_spec)

        return schema