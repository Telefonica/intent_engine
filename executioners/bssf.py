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

"""
Bssf logic for the intent engine
"""
import json
import logging

from queue import Queue
# from intent_engine.executioners.http_handler import http_handler
# from intent_engine.core import ib_model
from http_handler import http_handler
import logging
logger = logging.getLogger(__name__)

class bssf():
    def __init__(self,queue : Queue):
        self.__args={}
        self.__queue=queue
        self.__server_port=5000
        self.http_handler = http_handler(queue)
        logger.debug("BSSF init")
        # Starts listening to http requests from VAO
        self.setup_routes()
        self.start_server(self.__server_port)

    def setup_routes(self):
            self.http_handler.setup_routes("/bssf",processing_function=self.process_intent)

    def start_server(self, server_port):
        self.http_handler.start_server(server_port)

    def process_intent(self,request):
        """
        This would be for the request from VAO
        """
        logger.debug("Processing bssf")
        logger.debug("Request: %s",request)
        print("Processing bssf")
        print("Request: %s",request)

        intent_data=request

        nodes=[]
        links=[]
        applications=[]
        slices=[]
        intent={}
        contexts=[]
        expectations=[]
        id=0
        
        if(intent_data['componentNodeInstances']):
            for node in intent_data['componentNodeInstances']:
                logger.debug("Node: %s",node)
                if(node['componentNodeInstanceID']):
                    logger.debug("BSSF node")
                    context={
                        'contextAttribute':'componentNodeInstanceID',
                        'contextCondition':'IS_EQUAL_TO',
                        'contextValue':node['componentNodeInstanceID']
                    }
                    contexts.append(context)
                if(node['componentNodeInstanceName']):
                    context={
                        'contextAttribute':'componentNodeInstanceName',
                        'contextCondition':'IS_EQUAL_TO',
                        'contextValue':node['componentNodeInstanceName']
                    }
                    contexts.append(context)
                if(node['componentNodeInstanceHexID']):
                    context={
                        'contextAttribute':'componentNodeInstanceHexID',
                        'contextCondition':'IS_EQUAL_TO',
                        'contextValue':node['componentNodeInstanceHexID']
                    }
                    contexts.append(context)
                expectation_object={
                    'context':contexts,
                    'objectType':'node',
                    'objectInstance':node['componentNodeInstanceID']
                }
                expectation={
                    'expectationId':id+1,
                    'expectationVerb':'DELIVER',
                    'expectationObject':expectation_object
                }
                id+=1
                expectations.append(expectation)

        intent=self.data_to_intent(request)
        self.send_to_intent_queue(intent)
        return True

    def data_to_intent(self,data):
        return data
    
    def send_to_intent_queue(self,data):
        # add an item to a size limited queue with a timeout
        try:
            self.__queue.put(data, timeout=5)
        except self.__queue.Full:
            print("Queue full")


    def execute(self,data_and_params):
        """
        This would be for the response
        """
        logger.debug("Executing bssf")
        data=data_and_params[0]
        params=data_and_params[1]
        logger.debug("BSSF params: %s",params)
        if(params['type'] == 'http'):
            logger.debug("BSSF http")
            self.http_handler.execute(data_and_params)


# Example usage
if __name__ == "__main__":
    queue = Queue()
    handler = bssf(queue)