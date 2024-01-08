from ib_object import IB_object

class l2sm():

    def __init__(self):
        self.__isILU=True
        self.__hasSBI=True
        self.__parser={}
        self.__checker={}
        self.__interface={}
        self.__functions=[]

    def check_import(self):
        print("L2SM imported")
    def isILU(self):
        return self.__isILU
    def classifier(self,ib_object:IB_object):
        return []
    
    def checker(self,intent : IB_object):
        if intent.get_name() == "l2sm_deployment":
            print("is l2sm")
            return True
        return False
    def do_something_create(self,href):
        # special code 1
        print('========1=======' + href)

    def do_something_modify(self,href):
        # special code 2
        print('========2=======' + href)

    def do_something_remove(self,href):
        # special code 3
        print('========3=======' + href)

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

    
    # def find(self,d, tag):
    #     if tag in d:
    #         yield d[tag]
    #     for k, v in d.items():
    #         if isinstance(v, dict):
    #             for i in find(v, tag):
    #                 yield i

    # def get_yaml_keys(self,data):
    #     for k,v in data.items():
    #         yield k
    #         if isinstance(v,dict):
    #             for i in self.get_yaml_keys(v):
    #                 yield i
    #         if isinstance(v,list):
    #             for i in v:
    #                 self.get_yaml_keys(i)

    # if __name__ == "__main__":
    #     print(l2sm.get_yaml_keys(l2sm_structure()))