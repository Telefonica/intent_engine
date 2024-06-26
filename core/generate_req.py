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
import requests
import json
import yamlParser

url = "http://localhost:5000/intent_queue/1"
data = yamlParser.yaml_to_data("input.yaml")
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
try:
    r = requests.post(url, data=json.dumps(data), headers=headers,timeout=20)
except requests.exceptions.Timeout:
    print("Timed out")
print(r.text)