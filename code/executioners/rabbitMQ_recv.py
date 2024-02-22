import json
import logging
from queue import Queue
import pika
import sys
import logging

logger = logging.getLogger(__name__)
level = logger.level

def reciver(bind : list, queue : Queue):

    logger.info("Starting RMQ server in localhost:5672")
    connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost',port=5672))
    channel = connection.channel()

    channel.exchange_declare(exchange='mo', exchange_type='topic')

    result = channel.queue_declare('mncc', exclusive=True)
    queue_name = result.method.queue
    # queue_name = "kern.critical"

    binding_keys = bind
    if not binding_keys:
        sys.stderr.write("Usage: %s [binding_key]...\n" % bind)
        sys.exit(1)

    for binding_key in binding_keys:
        channel.queue_bind(
            exchange='mo', queue=queue_name, routing_key=binding_key)
    # logging.getLogger().setLevel(level)
    logger.info(' [*] Waiting for logs. To exit press CTRL+C in: %s %s',queue_name, binding_keys)

    def callback(ch, method, properties, body):
        # logging.debug(f" [x] {method.routing_key}:{json.loads(body)}")
        queue.put(json.loads(body))
        logger.info("New message from RMQ: %s %s",method.routing_key,body)

    channel.basic_consume(
        queue=queue_name, on_message_callback=callback, auto_ack=False)
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        logger.debug("RMQ server interrupt")
        channel.close()
        sys.exit()

if __name__ == "__main__":
    reciver(["mo","mncc"])