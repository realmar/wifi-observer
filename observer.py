# Created by: Anastassios Martakos
# Copyright (c) 2016 Anastassios Martakos

#!/usr/bin/env python3.4

# base dir has to be set
import sys

BASE_DIR = '/opt/wifi-observer'
sys.path.append(BASE_DIR)

import yaml
import os
import time

from multiprocessing import Process
from syslog import syslog, LOG_INFO

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
    for ssid in config['checks']['ssids'].keys():
        sanity = checkSSID(config['checks']['ssids'][ssid]['name'], config['checks']['ssids'][ssid]['encrypted'], config)

        writeCheck(db_connection, sanity, {'conn' : config['checks']['failed_conn'], 'dhcp' : config['checks']['failed_dhcp']})
        print(sanity)
        syslog(LOG_INFO, sanity.__str__())

# excecution
try:
    while(True):
        proc = Process(target=executeCheck)
        proc.start()
        time.sleep(config['checks']['interval'])
        proc.join()

except KeyboardInterrupt:
    print('Interrupted by User')
    db_connection.close()
    sys.exit(0)

db_connection.close()
