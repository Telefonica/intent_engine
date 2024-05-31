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
from flask import Flask, render_template, request, jsonify
from execution_platform import Execution_platform

app = Flask(__name__)
exec= Execution_platform()

@app.route('/')
def index():
    conn = exec.get_connection()
    return render_template('index.html', posts=conn)

@app.route('/intent_queue/<uuid>', methods=['GET', 'POST'])
def add_message(uuid):
    content = request.json
    print(content)
    return jsonify({"uuid":uuid})


if __name__ == "__main__":
    app.run(debug=True)