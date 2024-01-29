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

    channel.exchange_declare(exchange='topic_logs', exchange_type='topic')

    routing_key = key if len(key) > 2 else 'anonymous.info'
    channel.basic_publish(
        exchange='topic_logs', routing_key=routing_key, body=message)
    print(f" [x] Sent {routing_key}:{message}")
    connection.close()

if __name__ == "__main__":
    data={}
    with open("input.yaml", 'r') as yaml_file:
        data = yaml.safe_load(yaml_file)
    print(data)
    sender("kern" ,json.dumps(data))