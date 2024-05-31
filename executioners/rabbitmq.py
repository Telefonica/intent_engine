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
import logging
from queue import Queue
import threading
from .rabbitMQ_recv import reciver
import os

logger = logging.getLogger(__name__)

class rabbitmq():
    """
    The RabbitMQ executer stablish a connection between a RabbitMQ
    message broker and the Intent Engine. This executer will start
    a connecttion and send the entering intent to the internal 
    queue of the intent_core.
    """
    def __init__(self,queue : Queue):
        self.__args=["*mncc"]
        self.__addr=os.environ.get('AMQP_HOST')
        if(self.__addr):
            # Docker container case where hostname needed
            logger.debug("Reading enviroment RBMQ vars: %s",self.__addr)
        else:
            self.__addr="localhost"
        self.__broker_queue=os.environ.get('QUEUE_NAME')
        self.__port=5672
        self.__queue=queue
        # reduce log level
        logging.getLogger("pika").setLevel(logging.WARNING)
        self.start_mq_server(self.__args, queue)

    def start_mq_server(self,args : list,queue : Queue):
        logger.debug("Start threads RMQ")
        thread=threading.Thread(target=reciver,args=(args,queue,self.__addr,self.__port))
        thread.daemon = True # die when the main thread dies
        thread.start()
    
    def send_to_intent_queue(self,data):
        # add an item to a size limited queue with a timeout
        try:
            self.__queue.put(data, timeout=5)
        except self.__queue.Full:
            print("Queue full")