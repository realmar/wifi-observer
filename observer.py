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

from lib.db import connectDB, writeCheck
from lib.checker import checkSSID

# configuration
CONFIG =  os.path.join(BASE_DIR, 'wifi-observer.conf')

file = open(CONFIG, 'r')
config = yaml.load(file)
file.close()

#DB = os.path.join(BASE_DIR, config['database'])
#db_connection = connectDB(DB)

# excecution
try:
    while(True):
        for ssid in config['checks']['ssids'].keys():
            sanity = checkSSID(config['checks']['ssids'][ssid]['name'], config['checks']['ssids'][ssid]['encrypted'], config)

            #writeCheck(db_connection, sanity)
            print(sanity)

        time.sleep(config['checks']['interval'])

except KeyboardInterrupt:
    print('Interrupted by User')
    sys.exit(0)
