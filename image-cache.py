# Created by: Anastassios Martakos
# Copyright (c) 2016 Anastassios Martakos

#!/usr/bin/env python3.4

import sys, os

BASE_DIR = '/opt/wifi-observer'
sys.path.append(BASE_DIR)

import subprocess, datetime, yaml

from lib.db import getSSIDs

# configuration
CONFIG =  os.path.join(BASE_DIR, 'wifi-observer.conf')

file = open(CONFIG, 'r')
config = yaml.load(file)
file.close()

DB = os.path.join(BASE_DIR, config['database'])


ssids = getSSIDs(DB)
ssids.append({ 'name' : 'combined', 'where' : '' })
date = datetime.date.today().strftime("%Y-%m-%d")

for ssid in ssids:
    proc = subprocess.Popen(['mkdir', '-p', os.path.join(BASE_DIR, 'tmp')], stdout=subprocess.PIPE)
    proc.communicate()
    proc = subprocess.Popen(['cp', '-r', os.path.join(BASE_DIR, 'gnuplotfile'), os.path.join(BASE_DIR, 'tmp/gnuplotfile')], stdout=subprocess.PIPE)
    proc.communicate()
    proc = subprocess.Popen(['sed', '-i', ''.join(['s/<date>/', date, '/g']), os.path.join(BASE_DIR, 'tmp/gnuplotfile')], stdout=subprocess.PIPE)
    proc.communicate()
    proc = subprocess.Popen(['sed', '-i', ''.join(['s/<ssid>/', ssid['name'], '/g']), os.path.join(BASE_DIR, 'tmp/gnuplotfile')], stdout=subprocess.PIPE)
    proc.communicate()
    proc = subprocess.Popen(['sed', '-i', ''.join(['s/<addwhere>/', ssid['where'], '/g']), os.path.join(BASE_DIR, 'tmp/gnuplotfile')], stdout=subprocess.PIPE)
    proc.communicate()
    proc = subprocess.Popen(['gnuplot', os.path.join(BASE_DIR, 'tmp/gnuplotfile')], stdout=subprocess.PIPE)
    proc.communicate()
