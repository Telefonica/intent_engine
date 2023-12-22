

class l2sm():

    def __init__(self):
        __isILU__:True

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