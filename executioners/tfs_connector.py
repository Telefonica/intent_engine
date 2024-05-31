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


logger = logging.getLogger(__name__)

class tfs_connector():
    def __init__(self,queue : Queue):
        self.__args={}
        self.__addr='localhost' # Should come in config file (or intent?)
        self.__port=80
        self.__queue=queue
        logger.debug("TFS connector init")
        # reduce log level
        # self.start_https_server(self.__args, queue)
    
    def execute(self,data_and_params):
        params={}
        params=data_and_params[1]
        # data=data_and_params[0]
        logger.debug("data_and_params: %s",data_and_params)
        logger.debug("params: %s",params)
        if(params['connect_type']=='get'):
            self.get_and_post(data_and_params)
        if(params['connect_type']=='nbi'):
            self.__args['user']=params['user']
            self.__args['pasword']=params['password']
            self.tfs_nbi(data_and_params)
        return True
    
    def get_and_post(self,data_and_params):
        data=data_and_params[0]
        params=data_and_params[1]
        user="admin"
        password="admin"
        token=""
        if 'user' in self.__args:
            user=self.__args['user']
        if 'password' in self.__args:
            password=self.__args['pasword']
        session = requests.Session()
        session.auth = (user, password)
        if(params['connect_type']=="get"):
            url=params['url']
            url='http://192.168.165.10/webui'
            headers=params['headers']
            response=session.get(url=url)
            for item in response.iter_lines():
                # logger.debug("req %s",item)
                if("csrf_token" in str(item)):
                    string=str(item).split('<input id="csrf_token" name="csrf_token" type="hidden" value=')[1]
                    # string=str(item).strip('value=')
                    token=string.split(">")[0].strip('"')
                    # logger.debug("%s  %s",string,token)
            logger.debug("csrf token %s",token)
            
            if(headers['Content-Type'] == 'application/x-yaml'):
                response = session.post(url, headers=headers, data=yaml.dump(data),timeout=20)
            if(headers['Content-Type'] == 'application/json'):
                response = session.post(url, headers=headers, data=json.dumps(data),timeout=20)
            if(headers['Content-Type'] == 'multipart/form-data'):
                logger.debug("Data to send: %s",data)
                with open('temp.json', 'w') as outfile:
                    json.dump(data, outfile)
                with open('temp.json','r') as f:
                    files={'descriptors': f}
                    token={'csrf_token':token}
                    response = session.post(url,files=files,data=token,timeout=60)
            logger.debug("Http response: %s",response.text)
        return True
    
    def tfs_nbi(self,data_and_params):

        return True