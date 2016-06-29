import os, sys, sqlite3, datetime
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)

from lib.checker import *
from test.helpers.helper_funcs import loadConfig

config = loadConfig(BASE_DIR + '/test/mockup/wifi-observer.conf.mock')

def test_checkSSID():
    result = checkSSID('eth', 'True', config, BASE_DIR + '/test/temp/')

    assert 'errors' in result
    assert 'dbm' in result
    assert 'time_needed_conn' in result
    assert 'ping_average' in result
    assert 'time_needed_dhcp' in result
    assert 'bssid' in result
    assert 'ssid' in result
    assert 'time_start' in result
