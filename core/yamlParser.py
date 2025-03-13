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
    data=[]
    with open(yaml_file_path, 'r',encoding="utf-8") as yaml_file:
        for file in yaml.safe_load_all(yaml_file):
            data.append(file)

    return data