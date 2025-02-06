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

from devtools import pprint
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

        slice_data=request

        nodes=[]
        links=[]
        applications=[]
        slices=[]
        intent={}
        objectContexts=[]
        expectations=[]
        id=0

        # Nodes definition
        if('componentNodeInstances' in slice_data):
            for node in slice_data['componentNodeInstances']:
                logger.debug("Node: %s",node)
                print("Node: %s",node)
                objectContexts=[]
                expectation={}
                if('componentNodeInstanceID' in node):
                    logger.debug("BSSF node")
                    objectContexts.append({
                        'contextAttribute':'componentNodeInstanceID',
                        'contextCondition':'IS_EQUAL_TO',
                        'contextValue':node['componentNodeInstanceID']
                    })
                if('componentNodeInstanceName' in node):
                    objectContexts.append({
                        'contextAttribute':'componentNodeInstanceName',
                        'contextCondition':'IS_EQUAL_TO',
                        'contextValue':node['componentNodeInstanceName']
                    })
                if('componentNodeInstanceHexID' in node):
                    objectContexts.append({
                        'contextAttribute':'componentNodeInstanceHexID',
                        'contextCondition':'IS_EQUAL_TO',
                        'contextValue':node['componentNodeInstanceHexID']
                    })
                expectation_object={
                    'objectContexts':objectContexts,
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

        # Links definition
        if('graphLinkNodeInstances' in slice_data):
            for link in slice_data['graphLinkNodeInstances']:
                objectContexts=[]
                expectation={}
                if('graphLinkNodeInstanceID' in link):
                    objectContexts.append({
                        'contextAttribute':'graphLinkNodeInstanceID',
                        'contextCondition':'IS_EQUAL_TO',
                        'contextValue':link['graphLinkNodeInstanceID']
                    })
                if('fromComponentNodeInstanceID' in link):
                    objectContexts.append({
                        'contextAttribute':'fromComponentNodeInstanceID',
                        'contextCondition':'IS_EQUAL_TO',
                        'contextValue':link['fromComponentNodeInstanceID']
                    })
                if('toComponentNodeInstanceID' in link):
                    objectContexts.append({
                        'contextAttribute':'toComponentNodeInstanceID',
                        'contextCondition':'IS_EQUAL_TO',
                        'contextValue':link['toComponentNodeInstanceID']
                    })
                if('type' in link):
                    objectContexts.append({
                        'contextAttribute':'type',
                        'contextCondition':'IS_EQUAL_TO',
                        'contextValue':link['type']
                    })
                expectation_object={
                    'objectType':'6green_slice',
                    'objectInstance':link['graphLinkNodeInstanceID'],
                    'objectContexts':objectContexts
                }
                expectation={
                    'expectationId':id+1,
                    'expectationVerb':'DELIVER',
                    'expectationObject':expectation_object
                }
                id+=1
                expectations.append(expectation)
        
        intent['intentExpectations']=expectations

        # Constrains for nodes
        if 'constraints' in slice_data:
            for constraint in slice_data['constraints']:
                objectContexts=[]
                expectation={}
                if('componentNodeInstanceID' in constraint):
                # Computing constrains for nodes
                # Look for the node in the nodes list to add this target
                    for expectation in intent['intentExpectations']:
                        for objectContext in expectation['expectationObject']['objectContexts']:
                            if objectContext['contextAttribute']=='componentNodeInstanceID':
                                if objectContext['contextValue']==constraint['componentNodeInstanceID']:
                                    targetContexts=[]
                                    targetContexts.append({
                                        'contextAttribute':'category',
                                        'contextCondition':'IS_EQUAL_TO',
                                        'contextValue':constraint['category']
                                    })
                                    targetContexts.append({
                                        'contextAttribute':'type',
                                        'contextCondition':'IS_EQUAL_TO',
                                        'contextValue':constraint['type']
                                    })
                                    if 'expectationTargets' not in expectation['expectationObject']:
                                        expectation['expectationObject']['expectationTargets']=[]

                                    expectation['expectationObject']['expectationTargets'].append({
                                        'targetName': constraint['constraintID'],
                                        'targetCondition': 'IS_EQUALTO', # TODO: function to decided conditions
                                        'targetValue': constraint['constraintValue']+" "+constraint['constraintUnit'],
                                        'targetContexts': targetContexts
                                    })
                if('interfaceInstanceID' in constraint):
                    # Computing constrains for links --> slices
                    # Create an expectation for the slice with the constraints as targets
                    objectContexts=[]
                    expectation={}
                    expectationTargets=[]
                    expectationContexts=[]
                    objectContexts.append({
                        'contextAttribute':'interfaceInstanceID',
                        'contextCondition':'IS_EQUAL_TO',
                        'contextValue':constraint['interfaceInstanceID']
                    })
                    if 'resourceType' in constraint:
                        objectContexts.append({
                            'contextAttribute':'resourceType',
                            'contextCondition':'IS_EQUAL_TO',
                            'contextValue':constraint['resourceType']
                        })
                    if 'radioServiceType' in constraint:
                        objectContexts.append({
                            'contextAttribute':'radioServiceType',
                            'contextCondition':'IS_EQUAL_TO',
                            'contextValue':constraint['radioServiceType']
                        })
                    if 'allocationRetentionPriorityProfile' in constraint:
                        objectContexts.append({
                            'contextAttribute':'allocationRetentionPriorityProfile',
                            'contextCondition':'IS_EQUAL_TO',
                            'contextValue':constraint['allocationRetentionPriorityProfile']
                        })
                    if 'minimumGuaranteedBandwidth' in constraint:
                        expectationTargets.append({
                            'targetAttribute':'minimumGuaranteedBandwidth',
                            'targetCondition':'IS_HIGHER_THAN',
                            'targetValue':str(constraint['minimumGuaranteedBandwidth'])+" "+constraint['constraintUnit']
                        })
                    if 'maximumRequiredBandwidth' in constraint:
                        expectationTargets.append({
                            'targetAttribute':'maximumRequiredBandwidth',
                            'targetCondition':'IS_LOWER_THAN',
                            'targetValue':str(constraint['maximumRequiredBandwidth'])+" "+constraint['constraintUnit']
                        })
                    if 'category' in constraint:
                        expectationContexts.append({
                            'contextAttribute':'category',
                            'contextCondition':'IS_EQUAL_TO',
                            'contextValue':constraint['category']
                        })
                    if 'type' in constraint:
                        expectationContexts.append({
                            'contextAttribute':'type',
                            'contextCondition':'IS_EQUAL_TO',
                            'contextValue':constraint['type']
                        })
                    if 'qi' in constraint:
                        expectationTargets.append({
                            'targetAttribute':'qi',
                            'targetCondition':'IS_EQUAL_TO',
                            'targetValue':constraint['qi']
                        })
                    intent_expectation={
                        'expectationId':id+1,
                        'expectationObject':{
                            'objectType':'interfaceInstance',
                            'objectInstance':constraint['interfaceInstanceID'],
                            'objectContexts':objectContexts},
                        'expectationTargets': expectationTargets,
                        'expectationContexts':expectationContexts
                    }
                    id+=1
                    expectations.append(intent_expectation)

        # Intent contexts
        

        intent['intentId']=slice_data['applicationInstanceID']
        intent['userLabel']=slice_data['name']
        intent['intentAdminState']='PENDING'

        pprint(intent)
        
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

def check_key(dic, key):
    if key in dic.keys():
        print("Present, ", end =" ")
        print("value =", dic[key])
    else:
        print("Not present")

# Example usage
if __name__ == "__main__":
    queue = Queue()
    handler = bssf(queue)