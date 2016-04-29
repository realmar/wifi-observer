# Created by: Anastassios Martakos
# Copyright (c) 2016 Anastassios Martakos

#!/usr/bin/env python3.4

import subprocess
from flask import Flask
app = Flask(__name__)

# configuration
DATABASE = 'wifi-observer.db'

@app.route("/")
def home():


@app.route("/get/<date>")
def getSVG():
    proc = subprocess.Popen(['gnuplot', 'gnuplotfile'], stdout=subprocess.PIPE)
    proc.communicate()

    return app.send_static_file('wifi.svg')

if __name__ == "__main__":
    app.run(host='0.0.0.0')
