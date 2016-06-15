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
import datetime

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
        sanity = checkSSID(config['checks']['ssids'][ssid]['name'], config['checks']['ssids'][ssid]['encrypted'], config, BASE_DIR + '/log')

        id = writeCheck(db_connection, sanity, {'conn' : config['checks']['failed_conn'], 'dhcp' : config['checks']['failed_dhcp']})

        try:
            file = open(BASE_DIR + '/log/' + ssid + '.tmplog', 'r')
        except:
            pass
        else:
            try:
                gfile = open(BASE_DIR + '/log/' + ssid + '.log', 'a')
            except:
                file.close()
            else:
                gfile.write('==== SSID: ' + ssid + ' == ' + datetime.datetime.fromtimestamp(int(sanity['time_start'])).strftime('%Y-%m-%d %H:%M:%S') + ' == DB ID: ' + str(id) + '\n')
                gfile.write(file.read())
                gfile.close()
                file.close()

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
