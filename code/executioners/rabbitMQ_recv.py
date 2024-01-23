import json
import logging
from queue import Queue
import pika
import sys

def reciver(bind : list, queue : Queue):

    logging.info("Starting RMQ server in localhost:5672")
    logging.getLogger().setLevel(logging.INFO)
    connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost',port=5672))
    channel = connection.channel()

    channel.exchange_declare(exchange='topic_logs', exchange_type='topic')

    result = channel.queue_declare('pythonq', exclusive=True)
    queue_name = result.method.queue
    # queue_name = "kern.critical"

    binding_keys = bind
    if not binding_keys:
        sys.stderr.write("Usage: %s [binding_key]...\n" % bind)
        sys.exit(1)

    for binding_key in binding_keys:
        channel.queue_bind(
            exchange='topic_logs', queue=queue_name, routing_key=binding_key)

    logging.info(f' [*] Waiting for logs. To exit press CTRL+C in: {queue_name}, {binding_keys}')


    def callback(ch, method, properties, body):
        # logging.debug(f" [x] {method.routing_key}:{json.loads(body)}")
        queue.put(json.loads(body))
        logging.info("New message from RMQ: %s %s",method.routing_key,body)

    channel.basic_consume(
        queue=queue_name, on_message_callback=callback, auto_ack=False)

    channel.start_consuming()


if __name__ == "__main__":
    reciver(["kern","pythonq"])