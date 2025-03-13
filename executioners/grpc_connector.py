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
import grpc
from .grpc_libs import l2smmd
import logging
logger = logging.getLogger(__name__)

class grpc_connector():
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
        match params['connector']:
            case "l2smmd":
                logger.debug("l2smmd grpc proto")
                l2smmd.run(params,data)
            case _:
                logger.debug("NO grpc proto implemented")

        return True