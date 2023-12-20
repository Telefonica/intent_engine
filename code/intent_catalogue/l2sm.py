
def l2sm_structure():

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
    
    data = {
        'apiVersion': 'v1',
        'kind': 'Pod',
        'metadata': {
            'name': 'ping',
            'labels': {
                'app': 'ping-pong'
            },
            'annotations': {
                'k8s.v1.cni.cncf.io/networks': 'ping-network'
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
            ]
            # Uncomment the following line if you want to place the pod in a specific node
            # 'nodeName': 'masterk8s'
        }
    }

    return data

def find(d, tag):
    if tag in d:
        yield d[tag]
    for k, v in d.items():
        if isinstance(v, dict):
            for i in find(v, tag):
                yield i

def get_yaml_keys(data):
    for k,v in data.items():
        yield k
        if isinstance(v,dict):
            for i in get_yaml_keys(v):
                yield i
        if isinstance(v,list):
            for i in v:
                get_yaml_keys(i)

if __name__ == "__main__":
    
    
    print(get_yaml_keys(l2sm_structure()))