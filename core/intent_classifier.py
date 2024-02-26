from .ib_object import IB_object
import logging
logger = logging.getLogger(__name__)

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
                logger.info("%s : %s",key, value)
                if key in keywords:
                    self.find_in_tree(keywords,value,leaves)
        elif isinstance(obj, list):
            for item in obj:
                self.find_in_tree(keywords,item,leaves)
        else:
            # print("is leave :",obj)
            leaves.append(obj)

    def classify(self,intent : list):

        """
        When an intent is recived in the intent_core 
        """
        ill=[]
        # puede ser que para un intent haya varias librerías que
        # lo entiendan como suyo --> Tengo todos los decision trees
        # while loop con la condicion de que sean todo ilus
        # for module in module_instances:
        #     if not module['instance'].isILU():
        #         tree=module['instance'].get_decision_tree(intent)
        for tree in self.__trees:
            self.find_in_tree(intent.get_keywords(),tree,ill)
        sub_intents=[intent]
        o=[logger.info("Subintents : %s",s) for s in sub_intents]
        return sub_intents,ill