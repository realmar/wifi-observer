# Created by: Anastassios Martakos
# Copyright (c) 2016 Anastassios Martakos

#!/usr/bin/env python3.4

import sys, os

BASE_DIR = '/opt/wifi-observer'
sys.path.append(BASE_DIR)

import yaml, datetime

from lib.db import connectDB, generateCSV

# configuration
CONFIG =  os.path.join(BASE_DIR, 'wifi-observer.conf')

file = open(CONFIG, 'r')
config = yaml.load(file)
file.close()

DB = os.path.join(BASE_DIR, config['database'])
db_connection = connectDB(DB)

current_week = datetime.datetime.today().strftime("%W")
current_year = datetime.datetime.today().strftime("%Y")

for i in range(1, int(current_week)):
    generateCSV(db_connection, os.path.join(BASE_DIR, 'static/d3/' + current_year + '-' + str(i) + '-' + str(i + 1) + '.csv'), str(i), str(i + 1))
