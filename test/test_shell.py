import os, sys
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)

from lib.shell import *
from lib.exceptions import InvalidConfig
from nose.tools import timed

from test.helpers.helper_funcs import loadConfig

config = loadConfig(BASE_DIR + '/test/mockup/wifi-observer.conf.mock')

def test_disconnectWiFi():
    assert disconnectWiFi('sampletext', config['default_net'])

def test_connectWiFi():
    assert connectWiFi('sampletext', 'sampletext', 'sampletext', 'sampletext')

@timed(4.1)
def test_initializeInterface():
    assert initializeInterface('sampletext')

def test_getIP():
    assert type(getIP('sampletext')) == type(42)

def test_killPID():
    assert killPID(42)

def test_checkIP():
    assert not checkIP('172.30.72.1')
    assert checkIP('10.0.0.0')

def test_checkConnection():
    assert not checkConnection('sampletext', BASE_DIR + '/test/files/wifi_open_bad')
    assert checkConnection('sampletext', BASE_DIR + '/test/files/wifi_open_good')

def test_checkAuth():
    assert not checkAuth('sampletext', BASE_DIR + '/test/files/wifi_enc_bad')
    assert checkAuth('sampletext', BASE_DIR + '/test/files/wifi_enc_good')

def test_doPingAvr():
    assert not doPingAvr('heustock.ethz.ch', 'br0', 2) == 0
    assert doPingAvr('heustock.ethz.ch', 'sampletext', 2) == 0

def test_getDBM():
    assert not getDBM('sampletext') == 'NULL'

def test_getBSSID():
    try: getBSSID('sampletext')
    except: assert False
    else: assert True

def test_confFefaultGW():
    assert confDefaultGW

def test_collectErrors():
    assert len(collectErrors(BASE_DIR +  '/test/files/wifi_enc_bad_no_conn')) == 0
    result = collectErrors(BASE_DIR + '/test/files/wifi_enc_bad')
    assert result[0]['code'] == 'CTRL-EVENT-EAP-FAILURE'
    assert result[0]['id'] == 0
