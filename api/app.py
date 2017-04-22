# coding: utf-8
import os
import re
import datetime
from flask import Flask, jsonify, request
from modules.selector import Selector

app = Flask(__name__)
CURRENTPATH = os.path.dirname(__file__)

@app.route('/navibo/<clientID>', methods=['POST'])
def route():
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(port=5000)
