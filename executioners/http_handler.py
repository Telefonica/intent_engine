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
import requests
import yaml
import json
from flask import Flask, request, jsonify

logger = logging.getLogger(__name__)

class http_handler():
    def __init__(self,queue : Queue):
        self.__args=[]
        self.__addr='localhost' # Should come in config file (or intent?)
        self.__port=80
        # self.__port_flask=5000
        self.__queue=queue
        logger.debug("Http init")
        self.app = Flask(__name__)
        # self.setup_routes()
        # reduce log level
        # self.start_https_server(self.__args, queue)
    
    def execute(self,data_and_params):
        data=data_and_params[0]
        params=data_and_params[1]
        user="admin"
        password="admin"
        url=params['url']
        headers=params['headers']
        # url = 'http://192.168.165.168:8080'
        # headers = {'Content-Type': 'application/x-yaml'}
        print("Sending to http server data: %s",json.dumps(data))
        print("Sending to http server headers: %s %s",url,headers)
        session = requests.Session()
        session.auth = (user, password)
        if(headers['Content-Type'] == 'application/x-yaml'):
            response = session.post(url, headers=headers, data=yaml.dump(data),timeout=20)
        if(headers['Content-Type'] == 'application/json'):
            response = session.post(url, headers=headers, data=json.dumps(data),timeout=20)
        logger.info("Http response: %s",response)
        return True

    def setup_routes(self,route,processing_function):

        full_route='/api' + route
        logger.debug("Setting up routes %s",full_route)
        print("Setting up routes %s",full_route)

        @self.app.route(full_route, methods=['POST'])
        def api():
            if request.method == 'GET':
                return jsonify(isError= False,
                        message= "Success",
                        statusCode= 200,
                        data= "data"), 200
            if request.method == 'POST':
                data = request.get_json()
                logger.debug("Received data: %s", data)
                # Process the data as needed
                response = {"status": "success", "data": data}
                processing_function(data)
                return jsonify(response)

    def start_server(self, server_port):
        logger.debug("Starting server at %s:%s", self.__addr, server_port)
        self.app.run(host=self.__addr, port=server_port)


# Example usage
if __name__ == "__main__":
    queue = Queue()
    handler = http_handler(queue)
    handler.start_server(5000)