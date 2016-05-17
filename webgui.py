# Created by: Anastassios Martakos
# Copyright (c) 2016 Anastassios Martakos

#!/usr/bin/env python3.4

import sys, os

BASE_DIR = '/opt/wifi-observer'
sys.path.append(BASE_DIR)

from lib.db import getStats, getSSIDsName

import subprocess
import yaml
from flask import Flask, render_template
app = Flask(__name__)

# configuration
CONFIG =  os.path.join(BASE_DIR, 'wifi-observer.conf')

file = open(CONFIG, 'r')
config = yaml.load(file)
file.close()

DB = os.path.join(BASE_DIR, config['database'])

@app.route("/")
def home():
    stats = getStats(DB)
    ssids = [ 'combined' ]
    return render_template('home.html', ssids=ssids, diagrams=stats[0], glob=stats[1])

@app.route("/differentiate")
def differentiate():
    stats = getStats(DB)
    ssids = getSSIDsName()
    return render_template('home.html', ssids=ssids, diagrams=stats[0], glob=stats[1])

@app.route("/get/<date>")
def getSVG(date):
    return app.send_static_file(date + '.svg')

if __name__ == "__main__":
    app.run(debug=False)
