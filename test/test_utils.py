import os, sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from lib.utils import *
from lib.exceptions import InvalidConfig

config = {}

def test_01_configIntegrity_db():
    try: configIntegrity(config)
    except InvalidConfig as e: assert True
    else: assert False

def test_02_configIntegrity_computer():
    config['database'] = 'sampletext'
    try: configIntegrity(config)
    except InvalidConfig as e: assert True
    else: assert False

def test_03_configIntegrity_computer_location():
    config['database'] = 'sampletext'
    config['computer'] = {}
    try: configIntegrity(config)
    except InvalidConfig as e: assert True
    else: assert False

def test_04_configIntegrity_default_net():
    config['database'] = 'sampletext'
    config['computer'] = {}
    config['computer']['location'] = 'sampletext'
    try: configIntegrity(config)
    except InvalidConfig as e: assert True
    else: assert False

def test_05_configIntegrity_def_if():
    config['database'] = 'sampletext'
    config['computer'] = {}
    config['computer']['location'] = 'sampletext'
    config['default_net'] = {}
    try: configIntegrity(config)
    except InvalidConfig as e: assert True
    else: assert False


def test_06_configIntegrity_def_gw():
    config['database'] = 'sampletext'
    config['computer'] = {}
    config['computer']['location'] = 'sampletext'
    config['default_net'] = {}
    config['default_net']['interface'] = 'sampletext'
    try: configIntegrity(config)
    except InvalidConfig as e: assert True
    else: assert False


def test_07_configIntegrity_chks():
    config['database'] = 'sampletext'
    config['computer'] = {}
    config['computer']['location'] = 'sampletext'
    config['default_net'] = {}
    config['default_net']['interface'] = 'sampletext'
    config['default_net']['gateway'] = 'sampletext'
    try: configIntegrity(config)
    except InvalidConfig as e: assert True
    else: assert False


def test_08_configIntegrity_chks_interval():
    config['database'] = 'sampletext'
    config['computer'] = {}
    config['computer']['location'] = 'sampletext'
    config['default_net'] = {}
    config['default_net']['interface'] = 'sampletext'
    config['default_net']['gateway'] = 'sampletext'
    config['checks'] = {}
    try: configIntegrity(config)
    except InvalidConfig as e: assert True
    else: assert False


def test_09_configIntegrity_chks_f_conn():
    config['database'] = 'sampletext'
    config['computer'] = {}
    config['computer']['location'] = 'sampletext'
    config['default_net'] = {}
    config['default_net']['interface'] = 'sampletext'
    config['default_net']['gateway'] = 'sampletext'
    config['checks'] = {}
    config['checks']['interval'] = 'sampletext'
    try: configIntegrity(config)
    except InvalidConfig as e: assert True
    else: assert False


def test_10_configIntegrity_chks_f_dhcp():
    config['database'] = 'sampletext'
    config['computer'] = {}
    config['computer']['location'] = 'sampletext'
    config['default_net'] = {}
    config['default_net']['interface'] = 'sampletext'
    config['default_net']['gateway'] = 'sampletext'
    config['checks'] = {}
    config['checks']['interval'] = 'sampletext'
    config['checks']['failed_conn'] = 'sampletext'
    try: configIntegrity(config)
    except InvalidConfig as e: assert True
    else: assert False


def test_11_configIntegrity_chks_ping_c():
    config['database'] = 'sampletext'
    config['computer'] = {}
    config['computer']['location'] = 'sampletext'
    config['default_net'] = {}
    config['default_net']['interface'] = 'sampletext'
    config['default_net']['gateway'] = 'sampletext'
    config['checks'] = {}
    config['checks']['interval'] = 'sampletext'
    config['checks']['failed_conn'] = 'sampletext'
    config['checks']['failed_dhcp'] = 'sampletext'
    try: configIntegrity(config)
    except InvalidConfig as e: assert True
    else: assert False


def test_12_configIntegrity_ping_t():
    config['database'] = 'sampletext'
    config['computer'] = {}
    config['computer']['location'] = 'sampletext'
    config['default_net'] = {}
    config['default_net']['interface'] = 'sampletext'
    config['default_net']['gateway'] = 'sampletext'
    config['checks'] = {}
    config['checks']['interval'] = 'sampletext'
    config['checks']['failed_conn'] = 'sampletext'
    config['checks']['failed_dhcp'] = 'sampletext'
    config['checks']['ping_c'] = 'sampletext'
    try: configIntegrity(config)
    except InvalidConfig as e: assert True
    else: assert False


def test_13_configIntegrity_chks_ssids():
    config['database'] = 'sampletext'
    config['computer'] = {}
    config['computer']['location'] = 'sampletext'
    config['default_net'] = {}
    config['default_net']['interface'] = 'sampletext'
    config['default_net']['gateway'] = 'sampletext'
    config['checks'] = {}
    config['checks']['interval'] = 'sampletext'
    config['checks']['failed_conn'] = 'sampletext'
    config['checks']['failed_dhcp'] = 'sampletext'
    config['checks']['ping_c'] = 'sampletext'
    config['checks']['ping_target'] = 'sampletext'
    try: configIntegrity(config)
    except InvalidConfig as e: assert True
    else: assert False

def test_14_configIntegrity_chks_no_ssids():
    config['database'] = 'sampletext'
    config['computer'] = {}
    config['computer']['location'] = 'sampletext'
    config['default_net'] = {}
    config['default_net']['interface'] = 'sampletext'
    config['default_net']['gateway'] = 'sampletext'
    config['checks'] = {}
    config['checks']['interval'] = 'sampletext'
    config['checks']['failed_conn'] = 'sampletext'
    config['checks']['failed_dhcp'] = 'sampletext'
    config['checks']['ping_c'] = 'sampletext'
    config['checks']['ping_target'] = 'sampletext'
    config['checks']['ssids'] = []
    try: configIntegrity(config)
    except InvalidConfig as e: assert True
    else: assert False

def test_15_configIntegrity_():
    config['database'] = 'sampletext'
    config['computer'] = {}
    config['computer']['location'] = 'sampletext'
    config['default_net'] = {}
    config['default_net']['interface'] = 'sampletext'
    config['default_net']['gateway'] = 'sampletext'
    config['checks'] = {}
    config['checks']['interval'] = 'sampletext'
    config['checks']['failed_conn'] = 'sampletext'
    config['checks']['failed_dhcp'] = 'sampletext'
    config['checks']['ping_c'] = 'sampletext'
    config['checks']['ping_target'] = 'sampletext'
    config['checks']['ssids'] = []
    config['checks']['ssids'] = ['sampletext', 'sampletext']
    print(config)
    assert configIntegrity(config) == True
