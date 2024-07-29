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

        self.__addr=os.environ.get('AMQP_HOST')
        if(self.__addr):
            # Docker container case where hostname needed
            logger.debug("Reading enviroment RBMQ vars: %s",self.__addr)
        else:
            self.__addr="132.227.122.23"
        self.__broker_exchange=os.environ.get('RMQ_EXCHANGE')
        if(self.__broker_exchange):
            logger.debug("Reading enviroment RBMQ vars: %s",self.__broker_exchange)
        else:
            self.__broker_exchange="mo"
        self.__broker_queue=os.environ.get('RMQ_QUEUE')
        if(self.__broker_queue):
            logger.debug("Reading enviroment RBMQ vars: %s",self.__broker_queue)
        else:
            self.__broker_queue="mncc"
        self.__broker_port=os.environ.get('RMQ_PORT')
        if(self.__broker_port):
            logger.debug("Reading enviroment RBMQ vars: %s",self.__broker_port)
        else:
            self.__broker_port=30403
        
        self.__broker_user=os.environ.get('RMBQ_USER')
        if(self.__broker_user):
            logger.debug("Reading enviroment RBMQ vars: %s",self.__broker_user)
        else:
            self.__broker_user='nemo-user'

        self.__broker_pass=os.environ.get('RMBQ_PASSWORD')
        if(self.__broker_pass):
            logger.debug("Reading enviroment RBMQ vars: %s",self.__broker_pass)
        else:
            self.__broker_pass='PRE4utv0ytf0fnbeuv'
        
        self.__args=[os.environ.get('RMQ_BINDING')]
        if(self.__args):
            # Docker container case where hostname needed
            logger.debug("Reading enviroment RBMQ vars: %s",self.__args)
        else:
            self.__args=["create-network-paths"]

        # Intent queue
        self.__queue=queue
        # reduce log level
        logging.getLogger("pika").setLevel(logging.WARNING)
        self.start_mq_server(self.__args, queue)

    def start_mq_server(self,args : list,queue : Queue):
        logger.debug("Start threads RMQ")
        thread=threading.Thread(target=reciver,
                                args=(queue,self.__addr,
                                      self.__broker_port,self.__broker_exchange,
                                      self.__broker_queue,self.__broker_user,
                                      self.__broker_pass,args))
        thread.daemon = True # die when the main thread dies
        thread.start()
    
    def send_to_intent_queue(self,data):
        # add an item to a size limited queue with a timeout
        try:
            self.__queue.put(data, timeout=5)
        except self.__queue.Full:
            print("Queue full")