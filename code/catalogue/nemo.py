from ib_object import IB_object

class nemo():

    def __init__(self):
        self.__isILU=False
        self.__hasSBI=False
        self.__parser={}
        self.__checker={}
        self.__interface={}
        self.__functions=["deploy"]
        self.__classifier={
                            "cloud_continuum": {
                                "nemo_deployment":{
                                    "create":{
                                        "vpnl2":"vpn",
                                        "overlay":"l2sm"
                                    },
                                    "modify":"l2sm",
                                    "migrate":"sdnc l2sm"
                                }
                            }}

    def check_import(self):
        print("NEMO imported")

    def isILU(self):
        return self.__isILU
    
    def translator(self,intent:IB_object):
        intent.__name="l2sm_deploy"
        return intent

    def checker(self,intent:IB_object):
        print("checker intent get name: ",intent.get_context().get_name())
        if intent.get_context().get_name() == "nemo_deployment":
            print("is NEMO")
            # return self.__classifier tree para que la decisón esté fuera
            return True 
        return False
    
    def classifier(self,intent : IB_object):
        ill=[]
        self.find_in_tree(intent.get_keywords(),self.__classifier,ill)
        sub_intents=[intent]
        return sub_intents,ill
    
    # Este decison tree en el classifier, para interface sin saber que hay detrás
    def find_in_tree(self,keywords,obj,leaves: list):
        if isinstance(obj, dict):
            for key, value in obj.items():
                print(key, ":", value)
                if key in keywords:
                    self.find_in_tree(keywords,value,leaves)
        elif isinstance(obj, list):
            for item in obj:
                self.find_in_tree(keywords,item,leaves)
        else:
            # print("is leave :",obj)
            leaves.append(obj)
    