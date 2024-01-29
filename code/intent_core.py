from queue import Queue
import translator
import ib_object
import importer
import yamlParser
import os
from intent_classifier import Classifier
import logging

logging.basicConfig(level=logging.INFO,
                        datefmt="%H:%M:%S")
# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logging.getLogger().addHandler(ch)
ch.setFormatter(logging.Formatter(
    '[%(levelname)s - %(asctime)s] %(name)s: [%(threadName)s] %(message)s'))
logging.getLogger().setLevel(logging.DEBUG)

# create a bounded shared queue
buffer = Queue(maxsize=100)

if __name__ == "__main__":
    logging.debug("Logger in DEBUG mode")
    # ------- Import modules -------
    print("---------- Importer----------")
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

    # Los executioners serán las interfaces hacia afuera
    exec_instances=[]
    exec_cat=importer.Importer("executioner_catalogue.in")
    imported_executioners = exec_cat.get_imported_libraries()
    for name, module in imported_executioners.items():
        class_and_instance={}
        print(f"Executioner {name},{module} imported successfully.")
        splited=name.split('executioners.')[-1]
        class_and_instance['class'] =splited
        class_and_instance['instance']= getattr(module,splited)(buffer)
        # print(class_and_instance['instance'].check_import())
        exec_instances.append(class_and_instance)
    # Check NBI
    print("module_instances: ",module_instances)
    data=yamlParser.yaml_to_data("input.yaml")
    intent=ib_object.IB_object(data)
    print(intent)

    while True:
        intent=ib_object.IB_object(buffer.get())
        # ------- Intent classifier -------
        print("------- Intent classifier -------")
        
        classifier=Classifier([m['instance'] for m in module_instances])
        subintents,ill=classifier.classify(intent)
        print("ILL :",ill)

        # ------ Intent translator -------
        print("------ Intent translator -------")
        for ilu in ill:
            for module in module_instances:
                if module['class']==ilu:
                    exec_obj,executioner=module['instance'].translator(subintents)
        # ------ Execution platform -------
                    print(" ------ Execution platform -------")
                    for exec_instance in exec_instances:
                        if exec_instance['class'] in executioner:
                            logging.debug("Runnning %s",exec_instance['class'])
                            exec_instance['instance'].execute(exec_obj)
