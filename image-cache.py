# Created by: Anastassios Martakos
# Copyright (c) 2016 Anastassios Martakos

#!/usr/bin/env python3.4

import sys, os

BASE_DIR = '/opt/wifi-observer'
sys.path.append(BASE_DIR)

import subprocess, datetime

date = datetime.date.today().strftime("%Y-%m-%d")
proc = subprocess.Popen(['mkdir', '-p', os.path.join(BASE_DIR, 'tmp')], stdout=subprocess.PIPE)
proc.communicate()
proc = subprocess.Popen(['cp', '-r', os.path.join(BASE_DIR, 'gnuplotfile'), os.path.join(BASE_DIR, 'tmp/gnuplotfile')], stdout=subprocess.PIPE)
proc.communicate()
proc = subprocess.Popen(['sed', '-i', ''.join(['s/<date>/', date, '/g']), os.path.join(BASE_DIR, 'tmp/gnuplotfile')], stdout=subprocess.PIPE)
proc.communicate()
proc = subprocess.Popen(['gnuplot', os.path.join(BASE_DIR, 'tmp/gnuplotfile')], stdout=subprocess.PIPE)
proc.communicate()
