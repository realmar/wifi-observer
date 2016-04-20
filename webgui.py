# Created by: Anastassios Martakos
# Copyright (c) 2016 Anastassios Martakos

#!/usr/bin/env python3.4

from flask import Flask
app = Flask(__name__)

# configuration
DATABASE = 'awa.db'

@app.route("/")
def hello():
    return "Hello World"

if __name__ == "__main__":
    app.run()
