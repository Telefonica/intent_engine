import importlib
import os
import logging

logger = logging.getLogger(__name__)

class Importer:

    def __init__(self, catalogue_file):
        self.__catalogue_file=catalogue_file
        self.__imported_modules=self.import_modules_from_file()

    def import_modules_from_file(self)-> dict:
        
        logger.debug("Importing from: %s",os.getcwd())

        with open(self.__catalogue_file, 'r') as file:
            module_names = [line.strip() for line in file if line.strip()]
            # print("Importer",module_names)

        imported_modules = {}
        for module_name in module_names:
            # print("module_name: ",module_name)
            # splitted=module_name.split(".")
            # print("splitted: ",splitted)
            try:
                imported_module = importlib.import_module(module_name)
                imported_modules[module_name] = imported_module
            except ImportError as e:
                print(f"Error importing module {module_name}: {e}")

        return imported_modules

    def get_imported_libraries(self):
        return self.__imported_modules

if __name__ == "__main__":
    imp=Importer("intent_catalogue.in")
    imported_modules = imp.get_imported_libraries()
    # Now you can use the imported modules
    for name, module in imported_modules.items():
        print(f"Module {name} imported successfully.")
        # Perform actions using the imported module
