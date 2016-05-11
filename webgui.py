# Created by: Anastassios Martakos
# Copyright (c) 2016 Anastassios Martakos

#!/usr/bin/env python3.4

import sys, os

BASE_DIR = '/opt/astro-wlan-analyzer'
sys.path.append(BASE_DIR)

from lib.db import getStats

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

def calculateGlobalStats(stats):
    return {}

@app.route("/")
def home():
    stats = getStats(DB)
    return render_template('home.html', diagrams=stats, glob={'stats' : calculateGlobalStats(stats)})


@app.route("/get/<date>")
def getSVG(date):
    proc = subprocess.Popen(['mkdir', os.path.join(BASE_DIR, 'tmp')], stdout=subprocess.PIPE)
    proc.communicate()
    proc = subprocess.Popen(['cp', '-r', os.path.join(BASE_DIR, 'gnuplotfile'), os.path.join(BASE_DIR, 'tmp/gnuplotfile')], stdout=subprocess.PIPE)
    proc.communicate()
    proc = subprocess.Popen(['sed', '-i', ''.join(['s/<date>/', date, '/g']), os.path.join(BASE_DIR, 'tmp/gnuplotfile')], stdout=subprocess.PIPE)
    proc.communicate()
    proc = subprocess.Popen(['gnuplot', os.path.join(BASE_DIR, 'tmp/gnuplotfile')], stdout=subprocess.PIPE)
    proc.communicate()

    return app.send_static_file('wifi.svg')

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
