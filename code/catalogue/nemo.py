from ib_object import IB_object


class nemo():
    """
    This class works as a library for the Intent Engine. The structure is 
    difine in such way that the Intent Engine is capable of parsing a
    NEMO deployment intent. The principal functionality is to translate a 
    general NEMO deployment intent to an atomic intent. This atomic
    intent will be processed by its own library. 

    Relations: l2sm, (in future versions also vpn, sdnc)
    """
    def __init__(self):
        self.__module_name="nemo"
        self.__isILU=False
        self.__hasSBI=False
        self.__parser={}
        self.__checker={}
        self.__interface={}
        self.__functions=["deploy"]
        self.__decision_tree={
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

    def get_name(self):
        return self.__module_name
    def check_import(self):
        print("NEMO imported")

    def isILU(self):
        return self.__isILU
    
    def generate_subintent(self,intent:IB_object):
        intent.set_name("l2sm_deploy")
        return intent

    def checker(self,intent:IB_object):
        print("checker intent get name: ",intent.get_context().get_name())
        if intent.get_context().get_name() == "nemo_deployment":
            print("is NEMO")
            # return self.__classifier tree para que la decisón esté fuera
            return True
        return False
    def executioner(self):
        
        return
    # def classifier(self,intent : IB_object):
    #     ill=[]
    #     self.find_in_tree(intent.get_keywords(),self.__classifier,ill)
    #     sub_intents=[intent]
    #     return sub_intents,ill
    
    def get_decision_tree(self):
        return self.__decision_tree