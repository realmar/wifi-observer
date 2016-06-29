wifi-observer
=============
Description
-----------
With this software you can observe *n* wifi *ssids*.

checks
------
There are following checks implemented:
  - time needed to connect to a ssid (NULL if not successful)
  - time needed to do dhcp when connected (NULL if not successful)
  - average time needed for *n* pings in the connected wifi
  - dbm

this data with *ssid*, *bssid*, *start time* and *location* are logged into a sqlite database.

Deployment
----------
```sh
# NOTE: verify that all drivers needed for the wifi devices are installed and loaded

$ sqlite3 wifi-observer.db < wifi-observer.db.sql
$ vim wifi-observer.conf
  # adapt to your needed

# adapt the BASE_DIR so that it is pointing into the wifi-observer directory
$ vim observer.py webgui.py image-cache.py build-all-images.py webgui.wsgi
  BASE_DIR = '<dir-of-wifi-observer>'

# also adapt the pathes in the gnuplotfile

# install services, located in services/*
# observer
wifi-observer.sh.conf   # upstart
wifi-observer.services  # systemd

# webgui, ONLY DEBUGGING
wo-webgui.sh.conf       # upstart

$ python3.4 observer.py   # run observer

# install cronjob
# this cronjob generates the plots every 2nd minute
$ crontab -e
*/2 7-20 * * * /usr/bin/python3.4 /opt/astro-wlan-analyzer/image-cache.py
0 */1 * * * /usr/bin/python3.4 /opt/wifi-observer/data_cache.py
0 0 */1 * * /usr/bin/python3.4 /opt/wifi-observer/collective_data_cache.py

# initially generate all images
$ python3.4 build-all-images.py

# initially generate all csv data
$ python3.4 build_all_data.py
```

### wpa_supplicant
`observer.py` uses `wpa_supplicant` therefore you need do configure `wpa_supplicant`. For each `ssid` you want to check there has to be a config file in `/etc/` following this name schema: `/etc/wpa_supplicant-<ssid>.conf`

Here an example:

```sh
network={
	ssid="<ssid>"
	scan_ssid=1
	key_mgmt=WPA-EAP
	pairwise=CCMP
	group=CCMP
	eap=PEAP
	identity="<username>"
	password=<password> [or] hash:<password-hash>
	phase1="peaplabel=0"
	phase2="auth=MSCHAPV2"
}
```

### Apache
```xml
<VirtualHost *:80>
  ServerAdmin <you-email>
  ServerName <domain>

  DocumentRoot /opt/wifi-observer

  WSGIDaemonProcess wifi-observer user=wifiobserver
  WSGIScriptAlias / /opt/wifi-observer/webgui.wsgi

  <Directory /opt/wifi-observer>
    WSGIProcessGroup wifi-observer
    WSGIApplicationGroup %{GLOBAL}
    require all granted
  </Directory>

  ErrorLog ${APACHE_LOG_DIR}/error.log
  CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
```

Testing
-------
Run the testsuite:
```sh
$ export BASE=<root-wifi-observer>

$ cd <root-wifi-observer>
$ bash test/setup.#!/bin/sh
$ nosetests3 --with-coverage --cover-package=lib.checker,lib.db,lib.exceptions,lib.shell,lib.utils
$ bash test/teardown.sh
```
