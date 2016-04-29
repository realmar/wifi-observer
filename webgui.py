# Created by: Anastassios Martakos
# Copyright (c) 2016 Anastassios Martakos

#!/usr/bin/env python3.4

import sys, os

BASE_DIR = '/opt/astro-wlan-analyzer'
sys.path.append(BASE_DIR)

from lib.db import getUniqueDates

import subprocess
from flask import Flask
app = Flask(__name__)

# configuration
DATABASE = 'wifi-observer.db'

@app.route("/")
def home():
    return render_template('home.html', diagrams=getUniqueDates())


@app.route("/get/<date>")
def getSVG():
    proc = subprocess.Popen(['mkdir', os.path.join([BASE_DIR, 'tmp'])], stdout=subprocess.PIPE)
    proc.communicate()
    proc = subprocess.Popen(['cp', '-r', os.path.join([BASE_DIR, 'gnuplotfile']), os.path.join([BASE_DIR, 'tmp/gnuplotfile'])], stdout=subprocess.PIPE)
    proc.communicate()
    proc = subprocess.Popen(['sed', '-i', ''.join(['s/\<date\>/', date, '/g']), os.path.join([BASE_DIR, 'tmp/gnuplotfile'])], stdout=subprocess.PIPE)
    proc.communicate()
    proc = subprocess.Popen(['gnuplot', os.path.join([BASE_DIR, 'tmp/gnuplotfile'])], stdout=subprocess.PIPE)
    proc.communicate()

    return app.send_static_file('wifi.svg')

if __name__ == "__main__":
    app.run(host='0.0.0.0')
