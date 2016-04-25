# Created by: Anastassios Martakos
# Copyright (c) 2016 Anastassios Martakos

#!/usr/bin/env python3.4

import time

from lib.shell import disconnectWiFi, connectWiFi, checkIP, checkConnection, doPingAvr, getDBM, getBSSID, getIP, confDefaultGW

def checkSSID(ssid, encrypted, config):
    sanity = {'ssid' : ssid,
    'bssid' : 0,
    'time_start' : 0,
    'time_needed' : 0,
    'ping_average' : 0,
    'dbm' : 0}

    is_failed = False

    time_start = time.time();
    sanity['time_start'] = time_start

    connectWiFi(ssid, config['wifi_net']['interface'], encrypted)
    while(True):
        if time.time() - time_start > config['checks']['failed']:
            is_failed = True
            break

        if checkConnection(config['wifi_net']['interface']):
            break

    if not is_failed:
        getIP(config['wifi_net']['interface'])
        while(True):
            if time.time() - time_start > config['checks']['failed']:
                is_failed = True
                break

            if checkIP(config['checks']['ssids'][ssid]['gateway']):
                confDefaultGW(config['wifi_net']['interface'], config['checks']['ssids'][ssid]['gateway'])
                break

    time_end = time.time();
    sanity['time_needed'] = time_end - time_start

    if is_failed:
        sanity['ping_average'] = 0
        sanity['dbm'] = 0
        sanity['bssid'] = 0
    else:
        sanity['ping_average'] = doPingAvr(config['checks']['ping_target'], config['wifi_net']['interface'], config['checks']['ping_c'])
        sanity['dbm'] = getDBM(config['wifi_net']['interface'])
        sanity['bssid'] = getBSSID(config['wifi_net']['interface'])

    disconnectWiFi(config['wifi_net']['interface'], config['default_net'])

    return sanity
