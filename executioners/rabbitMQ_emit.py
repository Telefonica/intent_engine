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
    with open("inputs/tfs_ctx.yaml", 'r') as yaml_file:
        data = yaml.safe_load(yaml_file)
    print(data)
    sender("*mncc" ,json.dumps(data))