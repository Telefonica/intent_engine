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
import pika
import yaml
import json

"""
Test class simulation NEMO Meta-Orchestrator sending an Intent to the 
RabbitMQ queue.
"""
def sender(key,message):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost',port=5672))
    channel = connection.channel()

    channel.exchange_declare(exchange='mo', exchange_type='topic')

    routing_key = key if len(key) > 2 else 'anonymous.info'
    channel.basic_publish(
        exchange='mo', routing_key=routing_key, body=message)
    print(f" [x] Sent {routing_key}:{message}")
    connection.close()

if __name__ == "__main__":
    data={}
    with open("inputs/6green_int.yaml",'r') as yaml_file:
        data = yaml.safe_load(yaml_file)
    print(data)
    sender("*mncc" ,json.dumps(data))