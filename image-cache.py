# Created by: Anastassios Martakos
# Copyright (c) 2016 Anastassios Martakos

#!/usr/bin/env python3.4

import sys, os

BASE_DIR = '/opt/astro-wlan-analyzer'
sys.path.append(BASE_DIR)

import subprocess
import yaml

from lib.db import getAllDates

# configuration
CONFIG =  os.path.join(BASE_DIR, 'wifi-observer.conf')

file = open(CONFIG, 'r')
config = yaml.load(file)
file.close()

DB = os.path.join(BASE_DIR, config['database'])

dates = getAllDates(DB)

for date in dates:
    date = date[0]
    proc = subprocess.Popen(['mkdir', '-p', os.path.join(BASE_DIR, 'tmp')], stdout=subprocess.PIPE)
    proc.communicate()
    proc = subprocess.Popen(['cp', '-r', os.path.join(BASE_DIR, 'gnuplotfile'), os.path.join(BASE_DIR, 'tmp/gnuplotfile')], stdout=subprocess.PIPE)
    proc.communicate()
    proc = subprocess.Popen(['sed', '-i', ''.join(['s/<date>/', date, '/g']), os.path.join(BASE_DIR, 'tmp/gnuplotfile')], stdout=subprocess.PIPE)
    proc.communicate()
    proc = subprocess.Popen(['gnuplot', os.path.join(BASE_DIR, 'tmp/gnuplotfile')], stdout=subprocess.PIPE)
    proc.communicate()
