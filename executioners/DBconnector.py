# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from queue import Queue
import logging
from intent_engine.core.database_utils import create_intent_graph, store_graph_in_graphdb
logger = logging.getLogger(__name__)

class DBconnector():
    """
    Executioner to write 
    """
    def __init__(self,queue : Queue):
         self.__args={}
         self.__queue=queue

    
    def send_to_intent_queue(self,data):
            # add an item to a size limited queue with a timeout
            try:
                self.__queue.put(data, timeout=5)
            except self.__queue.Full:
                print("Queue full")

    def execute(self,data_and_params):
        params={}
        data=data_and_params[0]
        params=data_and_params[1]
        logger.debug("Executing DBconnector...")
        match params['DBfunction']:
            case "store_graph":
                logger.debug("create_intent_graph, store in database")
                store_graph_in_graphdb(create_intent_graph(data),params['endpoint_url'],params['repository'])
            case _:
                logger.debug("NO DB function implemented")

        return True