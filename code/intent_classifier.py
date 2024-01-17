from ib_object import IB_object

class Classifier():
    
    def __init__(self, module_instances) -> None:
        self.__modules=module_instances
        self.__trees=[mod.get_decision_tree()
                    for mod in module_instances]
        self.__ILUs=[ilu.get_name()
                    for ilu in module_instances
                    if ilu.isILU()]

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

    def classify(self,intent : list):
        
        ill=[]
        # puede ser que para un intent haya varias librerías que
        # lo entiendan como suyo --> Tengo todos los decision trees
        for tree in self.__trees:
            self.find_in_tree(intent.get_keywords(),tree,ill)
        sub_intents=[intent]

        return sub_intents,ill