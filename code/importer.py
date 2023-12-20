import importlib

def import_modules_from_file(file_path):
    with open(file_path, 'r') as file:
        module_names = [line.strip() for line in file if line.strip()]

    imported_modules = {}
    for module_name in module_names:
        try:
            imported_module = importlib.import_module(module_name)
            imported_modules[module_name] = imported_module
        except ImportError as e:
            print(f"Error importing module {module_name}: {e}")

    return imported_modules

if __name__ == "__main__":
    module_file_path = "intent_catalogue.in"
    imported_modules = import_modules_from_file(module_file_path)

    # Now you can use the imported modules
    for module_name, module in imported_modules.items():
        print(f"Module {module_name} imported successfully.")
        # Perform actions using the imported module
