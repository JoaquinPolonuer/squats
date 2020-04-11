from flask import Flask, request
from flask_cors import CORS
import json
from detect import run as camera

app = Flask(__name__)
CORS(app)
curValue = {}


class Value:
    value = {}


value = Value()
@app.route("/info", methods=["GET"])
def handle_request():
    print(value.value)
    return json.dumps(value.value)


@app.route("/info", methods=["POST"])
def handle_post():
    req = json.loads(request.data)
    res = {"status": "OK"}
    value.value = req

    return json.dumps(res)


@app.route("/start", methods=["POST"])
def handle_start():
    res = {"status": "OK"}
    camera()
    return json.dumps(res)


app.run()
