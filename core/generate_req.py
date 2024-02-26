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