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