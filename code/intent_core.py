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

    # cwd = os.getcwd()
    # os.chdir(cwd)
    data=yamlParser.yaml_to_data("input.yaml")
    # print(data)
    intent=ib_object.IB_object(data)
    print(intent)
    # ------- Intent assurance -------
    # a partir del objeto realizar comprobaciones en librería
    # ------- Intent classifier -------
    l = ['create', 'modify', 'remove'] # from decision tree
    intent_keywords=["create"]
    for e in l:              # this is my condition list
        if e in intent_keywords:  # this is the mechanism to choose the right function #intent checker
            # return globals()['do_something_' + e]()
            globals()['l2sm_' + e](e)
    # esto tendría que ser recursivo, checkerar primero nemo tree, luego l2sm tree
    # y si es ILU buscar las funciones y ejecutar
            
    # ------ Intent translator -------
    # una vez sacada la funcion a ejecutar puede devolver las siguientes funciones con los interfaces
    # dict = {interfaz_func, variables}
    # 