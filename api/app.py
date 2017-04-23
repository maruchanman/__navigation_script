# coding: utf-8
import os
import re
import datetime
from flask import Flask, jsonify, request
from flask_cors import CORS
from modules.selector import Selector

app = Flask(__name__)
CORS(app)
CURRENTPATH = os.path.dirname(__file__)

@app.route('/navibo/<clientID>', methods=['POST'])
def route(clientID):
    selector = Selector(clientID, request.json)
    return jsonify(selector.get_message())

if __name__ == '__main__':
    app.run(port=5000)
