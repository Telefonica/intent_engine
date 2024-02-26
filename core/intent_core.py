# © 2024 Telefónica Innovación Digital, All rights reserved
import os
from queue import Queue
from intent_engine.core import ib_object
from intent_engine.core import importer
from intent_engine.core import yamlParser
from intent_engine.core.intent_classifier import Classifier
import logging

logger = logging.getLogger(__name__)

# create a bounded shared queue
buffer = Queue(maxsize=100)

def core():
    print('Enter Ctrl+C to stop:')
    logging.debug("Logger in DEBUG mode")
    # ------- Import modules -------
    print("---------- Importer----------")
    imp=importer.Importer("intent_catalogue.in")
    imported_modules = imp.get_imported_libraries()
    # Now you can use the imported modules
    module_instances=[]
    for name, module in imported_modules.items():
        class_and_instance={}
        logger.info("Module %s, %s imported successfully.",name,module)
        splited=name.split('catalogue.')[-1]
        class_and_instance['class'] =splited
        class_and_instance['instance']= getattr(module,splited)()
        logger.debug(class_and_instance['instance'].check_import())
        module_instances.append(class_and_instance)
        # Perform actions using the imported module

    # Los executioners serán las interfaces hacia afuera
    exec_instances=[]
    exec_cat=importer.Importer("executioner_catalogue.in")
    imported_executioners = exec_cat.get_imported_libraries()
    for name, module in imported_executioners.items():
        class_and_instance={}
        logger.info("Executioner %s, %s imported successfully.",name,module)
        splited=name.split('executioners.')[-1]
        class_and_instance['class'] =splited
        class_and_instance['instance']= getattr(module,splited)(buffer)
        # print(class_and_instance['instance'].check_import())
        exec_instances.append(class_and_instance)
    # Check NBI
    logger.info("module_instances: %s",module_instances)
    data=yamlParser.yaml_to_data("input.yaml")
    intent=ib_object.IB_object(data)
    logger.info(intent)

    while True:
        pop=buffer.get()
        intent=ib_object.IB_object(pop)
        # ------- Intent classifier -------
        logger.info("------- Intent classifier -------")
        
        classifier=Classifier([m['instance'] for m in module_instances])
        subintents,ill=classifier.classify(intent)
        logger.info("ILL : %s",ill)

        # ------ Intent translator -------
        logger.info("------ Intent translator -------")
        for i,ilu in enumerate(ill):
            subintent=subintents[i]
            for module in module_instances:
                if module['class']==ilu:
                    exec_obj,executioner=module['instance'].translator(subintent)
        # ------ Execution platform -------
                    logger.info(" ------ Execution platform -------")
                    for exec_instance in exec_instances:
                        if exec_instance['class'] in executioner:
                            logger.info("Runnning %s",exec_instance['class'])
                            exec_instance['instance'].execute(exec_obj)
        logger.info("Intent procesed !!!")