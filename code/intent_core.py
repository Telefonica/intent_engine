import translator
import ib_object
import importer
import yamlParser
import os
from intent_classifier import Classifier

if __name__ == "__main__":

    # ------- Import modules -------
    imp=importer.Importer("intent_catalogue.in")
    imported_modules = imp.get_imported_libraries()
    # Now you can use the imported modules
    module_instances=[]
    for name, module in imported_modules.items():
        class_and_instance={}
        print(f"Module {name},{module} imported successfully.")
        splited=name.split('catalogue.')[-1]
        class_and_instance['class'] =splited
        class_and_instance['instance']= getattr(module,splited)()
        print(class_and_instance['instance'].check_import())
        module_instances.append(class_and_instance)
        # Perform actions using the imported module
    # Importar dependerá de la interfaz del módulo
    # Check NBI
    print("module_instances: ",module_instances)
    data=yamlParser.yaml_to_data("input.yaml")
    intent=ib_object.IB_object(data)
    print(intent)
            
    # ------- Intent classifier -------
    # while loop con la condicion de que sean todo ilus
    # for module in module_instances:
    #     if not module['instance'].isILU():
    #         tree=module['instance'].get_decision_tree(intent)
    
    classifier=Classifier([m['instance'] for m in module_instances])
    subintents,ill=classifier.classify(intent)
    print("ILL :",ill)

    for ilu in ill:
        order=ilu.translator(subintents)
        
    #
    # de momento asumo que solo hay dos pasos
    # popear el último hasta que sea ilu
    # si la lista vacía stop
    # modules_have_ill = True
    # while modules_have_ill:
    #     for module in module_instances:
    #         if not module['instance'].isILU():
    #             tree=module['instance'].get_decision_tree(intent)
    #             module_instances.pop(module)


    

    # el classifier tiene que dar una ill
    # que pasa si lo que da no es ILU?
    # classifier de ILU == null
    # l = ['create', 'modify', 'remove'] # from decision tree
    # intent_keywords=["create"]
    # for e in l:              # this is my condition list
    #     if e in intent_keywords:  # this is the mechanism to choose the right function #intent checker
    #         # return globals()['do_something_' + e]()
    #         globals()['l2sm_' + e](e)
    # esto tendría que ser recursivo, checkerar primero nemo tree, luego l2sm tree
    # y si es ILU buscar las funciones y ejecutar
    
    # ------- Intent assurance -------
    # a partir del objeto realizar comprobaciones en librería
    # ------ Intent translator -------
    # ill=[]
    # ill.append(module['instance'].classifier(intent))
    # una vez sacada la funcion a ejecutar puede devolver las siguientes funciones con los interfaces
    # dict = {interfaz_func, variables}

