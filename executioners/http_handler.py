# © 2024 Telefónica Innovación Digital, All rights reserved
import logging
from queue import Queue
import requests
import yaml
import json

logger = logging.getLogger(__name__)

class http_handler():
    def __init__(self,queue : Queue):
        self.__args=[]
        self.__addr='localhost' # Should come in config file (or intent?)
        self.__port=80
        self.__queue=queue
        logger.debug("Http init")
        # reduce log level
        # self.start_https_server(self.__args, queue)
    
    def execute(self,data):
        url = 'http://192.168.165.168:8080'
        headers = {'Content-Type': 'application/x-yaml'}
        print("Sending to http server: %s",json.dumps(data))
        response = requests.post(url, headers=headers, data=yaml.dump(data),timeout=20)
        logger.info("Http response: %s",response)
        return True