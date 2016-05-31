# Created by: Anastassios Martakos
# Copyright (c) 2016 Anastassios Martakos

#!/usr/bin/env python3.4

import sys, os

BASE_DIR = '/opt/wifi-observer'
sys.path.append(BASE_DIR)

from lib.db import getStats, getSSIDsName

import subprocess, yaml, datetime
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
    ssids = getSSIDsName(DB)
    return render_template('home.html', ssids=ssids, diagrams=stats[0], glob=stats[1])

@app.route("/d3")
def d3():
    current_week = datetime.datetime.today().strftime('%W')
    current_year = datetime.datetime.today().strftime('%Y')
    return renderD3(int(current_week), int(current_year))

@app.route("/d3/<year>/<end>")
def d3_cust(year, end):
    return renderD3(int(end), int(year))

@app.route("/get/<date>")
def getSVG(date):
    return app.send_static_file(date + '.svg')

def renderD3(current_week, current_year):
    next_year = current_year
    previous_year = current_year
    next_week = current_week + 1
    previous_week = current_week - 1;

    if current_week + 1 == 53:
        next_week = 1
        next_year = current_year + 1
    elif current_week - 1 < 1:
        previous_week = 52 - abs(current_week - 1)
        previous_year = current_year - 1

    return render_template('d3/index.html', week={ 'start' : current_week - 1, 'end' : current_week, 'next' : next_week, 'prev' : previous_week, 'next_year' : next_year, 'previous_year' : previous_year, 'year' : current_year })

if __name__ == "__main__":
    app.run(debug=False)
