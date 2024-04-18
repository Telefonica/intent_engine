import yaml
import os

def data_to_yaml(data):

    with open('input_v2.yaml', 'w') as yaml_file:
        yaml.dump(data, yaml_file, default_flow_style=False)

    print("YAML file 'pod.yaml' has been created.")
    return True

def yaml_to_data(relative_path):

    # Get the current working directory
    current_directory = os.getcwd()
    # Combine the current working directory and the relative path
    yaml_file_path = os.path.join(current_directory, relative_path)
    # Open the file and load the YAML data
    data={}
    with open(yaml_file_path, 'r') as yaml_file:
        data = yaml.safe_load(yaml_file)

    return data