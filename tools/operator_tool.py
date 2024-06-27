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

import logging,operator
logger = logging.getLogger(__name__)

class operatorTool():
    def __init__(self):
        ops = {
            "<": operator.lt,
            "=<": operator.le,
            "=": operator.eq,
            ">":operator.gt,
            ">=":operator.ge
        }
        
        # op_func = ops[op_char]
        # result = op_func(a, b)