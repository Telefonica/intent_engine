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
from queue import Queue

class sysout():

    def __init__(self,queue : Queue):
        self.__name="sysout"
        self.__args=[]
        self.__queue=queue
    def execute(self,string):
        print(" -> -> Executing: ", string, " <- <-")
        # True if no error
        return True