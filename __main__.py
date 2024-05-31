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
import signal
import sys
import os
from .core.intent_core import core

# Logger creation
date_fmt = "%H:%M:%S"
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logging.getLogger().addHandler(ch)
ch.setFormatter(logging.Formatter(
    '[%(levelname)s - %(asctime)s] %(name)s: [%(threadName)s] %(message)s',date_fmt))
logging.getLogger().setLevel(logging.DEBUG)
# logger = logging.getLogger(__name__)
logger = logging.getLogger(__name__)

def signal_handler(signal, frame):
    logger.info('You pressed Ctrl+C, keyboardInterrupt detected!')
    sys.exit(0)

def main():
    signal.signal(signal.SIGINT, signal_handler)
    core()

if __name__=="__main__":
    os.chdir('intent_engine')
    print(os.getcwd())
    main()
