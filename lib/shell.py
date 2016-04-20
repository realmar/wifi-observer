# Created by: Anastassios Martakos
# Copyright (c) 2016 Anastassios Martakos

#!/usr/bin/env python3.4

import subprocess

from lib.utils import decodeUTF8

def disconnectWiFi(interface):
    proc = subprocess.Popen(['killall', 'wpa_supplicant'], stdout=subprocess.PIPE)
    proc.communicate()

    print("disconnect")

    proc = subprocess.Popen(['dhclient', '-r', interface], stdout=subprocess.PIPE)
    proc.communicate()

    proc = subprocess.Popen(['iw', 'dev', interface, 'disconnect'], stdout=subprocess.PIPE)
    proc.communicate()

def connectWiFi(ssid, interface, wpa):
    if(wpa):
        proc = subprocess.Popen(['wpa_supplicant', '-B', '-i', interface, '-c', ''.join(['/etc/wpa_supplicant-', ssid, '.conf'])], stdout=subprocess.PIPE)
    else:
        proc = subprocess.Popen(['iw', 'dev',  interface, 'connect', ssid ], stdout=subprocess.PIPE)

def getIP(interface):
    proc = subprocess.Popen(['dhclient', interface], stdout=subprocess.PIPE)
    out = proc.communicate()

def checkIP():
    proc = subprocess.Popen(['ip', 'a'], stdout=subprocess.PIPE)
    out = proc.communicate()
    out = decodeUTF8(out)
    if 'inet 10.' in out || 'inet 172.30.' in out:
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
    out = out.split(' = ')[1]
    out = out.split(' ms')[0]
    out = out.split('/')[1]

    return out

def getDBM(interface):
    proc = subprocess.Popen(['iw', 'dev', interface, 'link'], stdout=subprocess.PIPE)
    out = proc.communicate()
    out = decodeUTF8(out)
    out = out.split('signal: ')[1]
    out = out.split(' dBm')[0]

    return out

def getBSSID(interface):
    proc = subprocess.Popen(['iw', 'dev', interface, 'link'], stdout=subprocess.PIPE)
    out = proc.communicate()
    out = decodeUTF8(out)
    out = out.split('Connected to ')[1]
    out = out.split(' (on ')[0]

    return out
