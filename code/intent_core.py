import translator
import ib_object
import importer
import yamlParser
import os

def l2sm_create(href):
        # special code 1
        print('========1=======' + href)

def l2sm_modify(href):
    # special code 2
    print('========2=======' + href)

def l2sm_remove(href):
    # special code 3
    print('========3=======' + href)

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
    # ------- Intent assurance -------
    # a partir del objeto realizar comprobaciones en librería
    for module in module_instances:
        if module['instance'].checker(intent):
            # append por si hay varias librerías?
            print("keywords: ",intent.get_keywords())
        else:
            print("Intent not from :",module['class'])
            
    # ------- Intent classifier -------
    # while loop con la condicion de que sean todo ilus
    for module in module_instances:
        if not module['instance'].isILU():
            intent,ill=module['instance'].classifier(intent)
    print("ILL :",ill)
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
    
              
    # ------ Intent translator -------
    # ill=[]
    # ill.append(module['instance'].classifier(intent))
    # una vez sacada la funcion a ejecutar puede devolver las siguientes funciones con los interfaces
    # dict = {interfaz_func, variables}
              