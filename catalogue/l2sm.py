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
from intent_engine.catalogue.abstract_library import abstract_library
from intent_engine.core.ib_object import IB_object
import logging

logger = logging.getLogger(__name__)

class l2sm(abstract_library):
    """
    L2S-M ILU library
    
    This is a library to translate an Intent Logic Unit (i.e an atomic
    intent) into an order the L2S-M tecnology cand understand.
    In this case is a Kubernets CRD in YAML format.

    Functions:
        - create_overlay
        - migrate_service
        - modify_overlay
    
    Attributes:
        - Module name
        - isILU: this library is able to proccess atomic intents.
        - executer: stores a list of the executers (South Bound Interface) capable 
                    of sending a concrete order to L2S-M.
        - functions: a list of the atomic tasks that can be done by L2S-M.
        - decision_tree: keywords tree that an intent may have to be understood as
                        a L2S-M intent. This decision tree is the one deciding which
                        function is being executed given an ILU.
    
    Relations: nemo
    """
    def __init__(self):
        self.__module_name="l2sm"
        self.__isILU=True
        self.__executioners=[]
        self.__checker={}
        self.__interface={}
        self.__functions=[]
        self.__decision_tree={"l2sm_deployment":"l2sm"}
        self.__params={"node_name":"",
                       "network":"",
                       "provider_name":"",
                       "provider_domain":"",
                       "access_list":["public-key-1", "public-key-2"]}

    def get_name(self):
        return self.__module_name
    
    def check_import(self):
        print("L2SM imported")

    def isILU(self):
        """
        Return true if this library is able to procces atomic
        intetns.
        """
        return self.__isILU
    
    def classifier(self,ib_object:IB_object):
        return []
    
    def checker(self,intent : IB_object):
        if intent.get_name() == "l2sm_deployment":
            logger.debug("is l2sm")
            return True
        return False
    
    def get_decision_tree(self):
        return self.__decision_tree

    def translator(self,subintent : IB_object) -> tuple[list , str]:
        """
        This functions translate an atomic intent into a CRD L2S-M software
        can understand. This function will decide which functionality (deploy,
        modify, migrate) will be called.

        This decision can be done using the same idea of the decision tree or a more
        direct way.
        """
        # TODO: los subintents direan si hay que desplegar/migrar/eliminar
        logger.info("Translating L2S-M...")
        logger.debug("debug L2S-M...")
        for exp in subintent.get_expectations():
            exp_verb=exp.get_verb()
            logger.debug("expectation case %s",exp_verb)
            match exp_verb:
                case "request":
                    exp_obj=exp.get_object()
                    logger.debug("request case obj: %s",exp_obj)
                    exp_type=exp_obj.get_type()
                    match exp_type:
                        case "l2sm-network":
                            for obj_ctx in exp_obj.get_contexts():
                                # Loop ctx inside obj
                                logger.debug("objectctx case %s: ",obj_ctx)
                                att=obj_ctx.get_attribute()
                                match att:
                                    case "network":
                                        logger.debug("network case")
                                        self.__params['network']=obj_ctx.get_value_range()
                                    case "provider_name":
                                        logger.debug("provider case")
                                        self.__params['provider_name']=obj_ctx.get_value_range()
                                    case "domain":
                                        logger.debug("domain case")
                                        self.__params['provider_domain']=obj_ctx.get_value_range()
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

        return self.l2sm_schema(),"http_handler"

    def create_ilu(self,ilu_ref):
        return ilu_ref

    def l2sm_schema(self):

        config= {
                    "provider": {
                        "name": self.__params['provider_name'], #si
                        "domain": self.__params['provider_domain'] #si
                    },
                    "accessList": self.__params['access_list'] #si publickeys
                }
        structure = {
                    "apiVersion": "l2sm.k8s.local/v1",
                    "kind": "L2SMNetwork",
                    "metadata": {
                        "name": self.__params['network']
                    },
                    "spec": {
                        "type": "inter-vnet",
                        "config": config,
                        "signature": "sxySO0jHw4h1kcqO/LMLDgOoOeH8dOn8vZWv4KMBq0upxz3lcbl+o/36JefpEwSlBJ6ukuKiQ79L4rsmmZgglk6y/VL54DFyLfPw9RJn3mzl99YE4qCaHyEBANSw+d5hPaJ/I8q+AMtjrYpglMTRPf0iMZQMNtMd0CdeX2V8aZOPCQP75PsZkWukPdoAK/++y1vbFQ6nQKagvpUZfr7Ecb4/QY+hIAzepm6N6lNiFNTgj6lGTrFK0qCVfRhMD+vXbBP6xzZjB2N1nIheK9vx7kvj3HORjZ+odVMa+AOU5ShSKpzXTvknrtcRTcWWmXPNUZLoq5k3U+z1g1OTFcjMdQ===="
                    }
                }

        return structure
    
    def get_blue_print(self):

        return True

"""
apiVersion: l2sm.k8s.local/v1
kind: L2SMNetwork
metadata:
  name: spain-network si
spec:
  type: inter-vnet
  config: |
    {
      "provider": {
        "name": "uc3m", si
        "domain": "idco.uc3m.es" si
      },
      "accessList": ["public-key-1", "public-key-2"] si
    }
  signature: sxySO0jHw4h1kcqO/LMLDgOoOeH8dOn8vZWv4KMBq0upxz3lcbl+o/36JefpEwSlBJ6ukuKiQ79L4rsmmZgglk6y/VL54DFyLfPw9RJn3mzl99YE4qCaHyEBANSw+d5hPaJ/I8q+AMtjrYpglMTRPf0iMZQMNtMd0CdeX2V8aZOPCQP75PsZkWukPdoAK/++y1vbFQ6nQKagvpUZfr7Ecb4/QY+hIAzepm6N6lNiFNTgj6lGTrFK0qCVfRhMD+vXbBP6xzZjB2N1nIheK9vx7kvj3HORjZ+odVMa+AOU5ShSKpzXTvknrtcRTcWWmXPNUZLoq5k3U+z1g1OTFcjMdQ====
"""