wifi-observer
=============
Description
-----------
With this software you can observe *n* wifi *ssids*

checks
------
There are following checks implemented:
  - time needed to connect to ssid
  - average time needed for *n* pings in the connected wifi
  - dbm

this data with *ssid*, *bssid* and *start time* are logged into a sqlite database.

Deployment
----------
```sh
# NOTE: verify that all drivers needed for the wifi devices are loaded

$ sqlite3 wifi-observer.db < wifi-observer.db.sql
$ vim wifi-observer.conf
  # adapt to your needed

# adapt the BASE_DIR so that it is pointing into the wifi-observer directory
$ vim observer.py
  BASE_DIR = '<dir-of-wifi-observer>'

# install services
# observer
wifi-observer.sh.conf   # upstart
wifi-observer.services  # systemd

# webgui, ONLY DEBUGGING
wo-webgui.sh.conf       # upstart

$ python3.4 observer.py   # run observer

# install cronjob
# this cronjob generates the plots every 2nd minute
$ crontab -e
*/2 * * * * /usr/bin/python3.4 /opt/astro-wlan-analyzer/image-cache.py
```
