# Created by: Anastassios Martakos
# Copyright (c) 2016 Anastassios Martakos

#!/usr/bin/env python3.4

# base dir has to be set
import sys

BASE_DIR = '/opt/astro-wlan-analyzer'
sys.path.append(BASE_DIR)

import yaml
import os
import time

from multiprocessing import Process

from lib.db import connectDB, writeCheck
from lib.checker import checkSSID

# configuration
CONFIG =  os.path.join(BASE_DIR, 'wifi-observer.conf')

file = open(CONFIG, 'r')
config = yaml.load(file)
file.close()

DB = os.path.join(BASE_DIR, config['database'])
db_connection = connectDB(DB)

# functions
def executeCheck():
    sanity = checkSSID(config['checks']['ssids'][ssid]['name'], config['checks']['ssids'][ssid]['encrypted'], config)

    writeCheck(db_connection, sanity, config['checks']['failed'])
    print(sanity)

# excecution
try:
    while(True):
        processes = []
        for ssid in config['checks']['ssids'].keys():
            processes.append(Process(target=executeCheck))

        time.sleep(config['checks']['interval'])

        for proc in processes:
            proc.join()

except KeyboardInterrupt:
    print('Interrupted by User')
    sys.exit(0)
