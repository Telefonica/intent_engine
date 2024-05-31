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
import json
import logging
from queue import Queue
import pika
import sys

logger = logging.getLogger(__name__)
level = logger.level

def reciver(bind : list, queue : Queue, host, port):

    logger.info("Starting RMQ server in %s:%s",host,port)
    connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=host,port=port))
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
        logger.info("New message from RMQ: %s",method.routing_key)

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