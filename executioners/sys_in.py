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
from intent_engine.core import yamlParser

logger = logging.getLogger(__name__)

class sys_in():
    """
    Executioner to write 
    """
    def __init__(self,queue : Queue):
        self.__args=["inputs/","l2vpn_tfs.yaml"]
        self.__queue=queue
        data=yamlParser.yaml_to_data(self.__args[0]+self.__args[1])
        self.send_to_intent_queue(data)
    
    def send_to_intent_queue(self,data):
        # add an item to a size limited queue with a timeout
        try:
            self.__queue.put(data, timeout=5)
        except self.__queue.Full:
            print("Queue full")