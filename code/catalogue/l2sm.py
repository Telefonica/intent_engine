from ib_object import IB_object

class l2sm():
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
            print("is l2sm")
            return True
        return False
    
    def get_decision_tree(self):
        return self.__decision_tree

    def translator(self,subintent : IB_object) -> (dict , str):
        """
        This functions translate an atomic intent into a CRD L2S-M software
        can understand. This function will decide which functionality (deploy,
        modify, migrate) will be called.

        This decision can be done using the same idea of the decision tree or a more
        direct way.
        """
        # TODO: los subintents direan si hay que desplegar/migrar/eliminar
        return self.l2sm_structure(),"sysout"

    def create_ilu(self,ilu_ref):

        return ilu_ref

    def l2sm_structure(self):

        nodename='masterk8s'
        network='ping-network'
        pod_name='ping'
        
        structure = {
            'apiVersion': 'v1',
            'kind': 'Pod',
            'metadata': {
                'name': pod_name,
                'labels': {
                    'app': 'ping-pong'
                },
                'annotations': {
                    'k8s.v1.cni.cncf.io/networks': network
                }
            },
            'spec': {
                'containers': [
                    {
                        'name': 'router',
                        'command': ["/bin/ash", "-c", "trap : TERM INT; sleep infinity & wait"],
                        'image': 'alpine:latest',
                        'securityContext': {
                            'capabilities': {
                                'add': ['NET_ADMIN']
                            }
                        }
                    }
                ],
                # Uncomment the following line if you want to place the pod in a specific node
                'nodeName': nodename
            }
        }

        return structure
