# Created by: Anastassios Martakos
# Copyright (c) 2016 Anastassios Martakos

#!/usr/bin/env python3.4

import time

from lib.shell import *

def checkSSID(ssid, encrypted, config, logdir):
    sanity = {'ssid' : ssid,
    'bssid' : 0,
    'time_start' : 0,
    'time_needed_conn' : 0,
    'time_needed_dhcp' : 0,
    'ping_average' : 0,
    'dbm' : 0}

    is_failed = False

    initializeInterface(config['wifi_net']['interface'])

    time_start = time.time();
    sanity['time_start'] = time_start

    connectWiFi(ssid, config['wifi_net']['interface'], encrypted, logdir)

    while(True and encrypted):
        if time.time() - time_start > config['checks']['failed_conn']:
            is_failed = True
            break

        if checkAuth(config['wifi_net']['interface'], logdir + '/' + ssid + '.tmplog'):
            break

    while(True and not encrypted):
        if time.time() - time_start > config['checks']['failed_conn']:
            is_failed = True
            break

        if checkConnection(config['wifi_net']['interface'], logdir + '/' + ssid + '.tmplog'):
            break

    time_end = time.time();
    sanity['time_needed_conn'] = time_end - time_start

    time.sleep(4)

    time_start = time.time();
    if not is_failed:
        sanity['bssid'] = getBSSID(config['wifi_net']['interface'])
        sanity['dbm'] = getDBM(config['wifi_net']['interface'])
        pid = getIP(config['wifi_net']['interface'])
        while(True):
            if time.time() - time_start > config['checks']['failed_dhcp']:
                is_failed = True
                killPID(pid)
                break

            if checkIP(config['checks']['ssids'][ssid]['gateway']):
                confDefaultGW(config['wifi_net']['interface'], config['checks']['ssids'][ssid]['gateway'])
                break
    else:
        sanity['bssid'] = 'NULL'
        sanity['dbm'] = 'NULL'

    time_end = time.time();
    sanity['time_needed_dhcp'] = time_end - time_start

    sanity['errors'] = collectErrors(ssid, logdir)

    if is_failed:
        sanity['ping_average'] = 0
    else:
        sanity['ping_average'] = doPingAvr(config['checks']['ping_target'], config['wifi_net']['interface'], config['checks']['ping_c'])

    disconnectWiFi(config['wifi_net']['interface'], config['default_net'])

    return sanity
