# Created by: Anastassios Martakos
# Copyright (c) 2016 Anastassios Martakos

#!/usr/bin/env python3.4

from lib.exceptions import *

def decodeUTF8(tulp):
    return tulp[0].decode('utf-8')

def configIntegrity(config):
    if config.get('database') == None:
        raise InvalidConfig('Specify a database')

    if config.get('computer') == None:
        raise InvalidConfig('set computer location')

    if config.get('computer').get('location') == None:
        raise InvalidConfig('set computer location')

    if config.get('default_net') == None:
        raise InvalidConfig('Configure default_net')

    if config.get('default_net').get('interface') == None:
        raise InvalidConfig('define default_net interface')

    if config.get('default_net').get('gateway') == None:
        raise InvalidConfig('define default_net gateway')

    if config.get('checks') == None:
        raise InvalidConfig('configure checks')

    if config.get('checks').get('interval') == None:
        raise InvalidConfig('specify check interval')

    if config.get('checks').get('failed_conn') == None:
        raise InvalidConfig('specify connection timeout')

    if config.get('checks').get('failed_dhcp') == None:
        raise InvalidConfig('specify dhcp timeout')

    if config.get('checks').get('ping_c') == None:
        raise InvalidConfig('specify ping count')

    if config.get('checks').get('ping_target') == None:
        raise InvalidConfig('specify a ping target')

    if config.get('checks').get('ssids') == None:
        raise InvalidConfig('configure some ssids')

    if len(config.get('checks').get('ssids')) == 0:
        raise InvalidConfig('configure some ssids')

    return True
