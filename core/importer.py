# © 2024 Telefónica Innovación Digital

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
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
            logger.debug("module_name: %s",module_name)
            # splitted=module_name.split(".")
            # print("splitted: ",splitted)
            try:
                imported_module = importlib.import_module(module_name)
                logger.debug("imported_module: %s",imported_module)
                imported_modules[module_name] = imported_module
            except ImportError as e:
                logger.debug("Error importing module %s: %s",module_name,e)

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
