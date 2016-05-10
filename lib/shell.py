# Copyright (c) 2016 Anastassios Martakos
# Created by: Anastassios Martakos

#!/usr/bin/env python3.4

import subprocess

from lib.utils import decodeUTF8

def disconnectWiFi(interface, defaults):
    proc = subprocess.Popen(['killall', 'wpa_supplicant'], stdout=subprocess.PIPE)
    proc.communicate()

    print("disconnect")

    proc = subprocess.Popen(['dhclient', '-r', interface], stdout=subprocess.PIPE)
    proc.communicate()

    # proc = subprocess.Popen(['iw', 'dev', interface, 'disconnect'], stdout=subprocess.PIPE)
    # proc.communicate()

    proc = subprocess.Popen(['ip', 'link', 'set', interface, 'down'], stdout=subprocess.PIPE)
    proc.communicate()

    confDefaultGW(defaults['interface'], defaults['gateway'])

def connectWiFi(ssid, interface, wpa):
    if(wpa):
        proc = subprocess.Popen(['ip', 'link', 'set',  interface, 'up' ], stdout=subprocess.PIPE)
        proc.communicate()
        proc = subprocess.Popen(['wpa_supplicant', '-B', '-i', interface, '-c', ''.join(['/etc/wpa_supplicant-', ssid, '.conf'])], stdout=subprocess.PIPE)
    else:
        # proc = subprocess.Popen(['ip', 'link', 'set',  interface, 'up' ], stdout=subprocess.PIPE)
        # proc.communicate()
        # proc = subprocess.Popen(['iw', 'dev',  interface, 'scan' ], stdout=subprocess.PIPE, shell=True)
        # proc.communicate()
        # proc = subprocess.Popen(['iw', 'dev',  interface, 'connect', ssid ], stdout=subprocess.PIPE, shell=True)
        # out = decodeUTF8(proc.communicate())
        # print(out)

        proc = subprocess.Popen('ip link set ' + interface + ' up && ' + 'iw dev ' + interface + ' scan && ' + 'iw dev ' + interface + ' connect ' + ssid, stdout=subprocess.PIPE, shell=True)


def getIP(interface):
    proc = subprocess.Popen('dhclient ' + interface, stdout=subprocess.PIPE, shell=True)
    return proc.pid

def killPID(pid):
    proc = subprocess.Popen(['kill', '-9',  str(pid) ], stdout=subprocess.PIPE)
    proc.communicate()

def checkIP(gw):
    proc = subprocess.Popen(['ip', 'a'], stdout=subprocess.PIPE)
    out = proc.communicate()
    out = decodeUTF8(out)
    if ''.join(['inet ', gw[0:4]]) in out:
        return True
    else:
        return False

def checkConnection(interface):
    proc = subprocess.Popen(['iw', 'dev', interface, 'link'], stdout=subprocess.PIPE)
    out = proc.communicate()
    out = decodeUTF8(out)
    if 'Not connected' in out:
        return False
    else:
        return True

def doPingAvr(target, interface, count):
    proc = subprocess.Popen(['ping', ''.join(['-c', str(count)]), '-I', interface, target], stdout=subprocess.PIPE)
    out = proc.communicate()
    out = decodeUTF8(out)

    try:
        out = out.split(' = ')[1]
        out = out.split(' ms')[0]
        out = out.split('/')[1]
    except:
        return 0

    return out

def getDBM(interface):
    proc = subprocess.Popen(['iw', 'dev', interface, 'link'], stdout=subprocess.PIPE)
    out = proc.communicate()
    out = decodeUTF8(out)
    try:
        out = out.split('signal: ')[1]
        out = out.split(' dBm')[0]
    except:
        return 'NULL'

    return out

def getBSSID(interface):
    proc = subprocess.Popen(['iw', 'dev', interface, 'link'], stdout=subprocess.PIPE)
    out = proc.communicate()
    out = decodeUTF8(out)
    out = out.split('Connected to ')[1]
    out = out.split(' (on ')[0]

    return out

def confDefaultGW(interface, gw):
    proc = subprocess.Popen(['ip', 'route', 'del', 'default'], stdout=subprocess.PIPE)
    out = proc.communicate()
    proc = subprocess.Popen(['ip', 'route', 'add', 'default', 'via', gw, 'dev', interface], stdout=subprocess.PIPE)
    out = proc.communicate()
