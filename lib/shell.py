# Created by: Anastassios Martakos
# Copyright (c) 2016 Anastassios Martakos

#!/usr/bin/env python3.4

import subprocess

def disconnectWiFi(interface):
    proc = subprocess.Popen(['killall', 'wpa_supplicant'], stdout=subprocess.PIPE)
    proc.communicate()

    proc = subprocess.Popen(['iw', 'dev', interface, 'disconnect'], stdout=subprocess.PIPE)
    proc.communicate()

def connectWiFi(ssid, interface):
    proc = subprocess.Popen(['wpa_supplicant', '-B', '-i', interface, '-c', ''.join(['/etc/wpa_supplicant-', ssid])], stdout=subprocess.PIPE)
    proc = subprocess.Popen(['dhclient', interface], stdout=subprocess.PIPE)
    out = proc.communicate()

def checkIP():
    proc = subprocess.Popen(['killall', 'wpa_supplicant'], stdout=subprocess.PIPE)
    out = proc.communicate()
    if 'inet 10.' in out:
        return True
    else:
        return False

def checkConnection():
    proc = subprocess.Popen(['iw', 'dev', interface, 'link'], stdout=subprocess.PIPE)
    out = proc.communicate()
    if 'Not connected' in out:
        return False
    else:
        return True

def doPingAvr(target, interface, count):
    proc = subprocess.Popen(['ping', ''.join(['-c', count]), '-I', interface, target], stdout=subprocess.PIPE)
    out = proc.communicate()
    out = out.split(' = ')[1]
    out = out.split(' ms')[0]
    out = out.split('/')[1]

    return out

def getDBM(interface):
    proc = subprocess.Popen(['iw', 'dev', interface, 'link'], stdout=subprocess.PIPE)
    out = proc.communicate()
    out = out.split('signal: ')[1]
    out = out.split(' dBm')[0]

    return out

def getBSSID(interface):
    proc = subprocess.Popen(['iw', 'dev', interface, 'link'], stdout=subprocess.PIPE)
    out = proc.communicate()
    out = out.split('Connected to ')[1]
    out = out.split(' (on ')[0]

    return out
