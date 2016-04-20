# Created by: Anastassios Martakos
# Copyright (c) 2016 Anastassios Martakos

#!/usr/bin/env python3.4

import time

from lib.shell import disconnectWiFi, connectWiFi, checkIP, checkConnection, doPingAvr, getDBM, getBSSID, getIP

def checkSSID(ssid, encrypted, config):
    sanity = {'ssid' : ssid,
    'bssid' : 0,
    'time_start' : 0,
    'time_needed' : 0,
    'ping_average' : 0,
    'dbm' : 0}

    time_start = time.time();
    sanity['time_start'] = time_start

    connectWiFi(ssid, config['interface'], encrypted)
    while(True):
        if time.time() - time_start > config['checks']['failed']:
            break

        if checkConnection(config['interface']):
            break

    if time.time() - time_start < config['checks']['failed']:
        print("getting IP")
        getIP(config['interface'])
        while(True):
            if time.time() - time_start > config['checks']['failed']:
                break

            if checkIP():
                break

    time_end = time.time();
    sanity['time_needed'] = time_end - time_start

    sanity['ping_average'] = doPingAvr(config['checks']['ping_target'], config['interface'], config['checks']['ping_c'])
    sanity['dbm'] = getDBM(config['interface'])
    sanity['bssid'] = getBSSID(config['interface'])

    disconnectWiFi(config['interface'])
