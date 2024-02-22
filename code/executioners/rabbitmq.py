import logging
from queue import Queue
import threading
from .rabbitMQ_recv import reciver
import concurrent.futures
import signal,sys

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
        self.__addr='localhost' # Should come in config file (or intent?)
        self.__port=5672
        self.__queue=queue
        # reduce log level
        logging.getLogger("pika").setLevel(logging.WARNING)
        self.start_mq_server(self.__args, queue)

    def start_mq_server(self,args : list,queue : Queue):
        logger.debug("Start threads RMQ")
        thread=threading.Thread(target=reciver,args=(args,queue))
        thread.daemon = True # die when the main thread dies
        thread.start()
    
    def send_to_intent_queue(self,data):
        # add an item to a size limited queue with a timeout
        try:
            self.__queue.put(data, timeout=5)
        except self.__queue.Full:
            print("Queue full")