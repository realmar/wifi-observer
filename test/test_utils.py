import os, sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from lib.utils import *
from lib.exceptions import InvalidConfig

config = {}

def test_configIntegrity_db():
    try: configIntegrity(config)
    except InvalidConfig as e: assert False
    else: assert True
config['database'] = 'sampletext'

def test_configIntegrity_computer():
    try: configIntegrity(config)
    except InvalidConfig as e: assert False
    else: assert True
config['computer'] = {}

def test_configIntegrity_computer_location():
    try: configIntegrity(config)
    except InvalidConfig as e: assert False
    else: assert True
config['computer']['location'] = 'sampletext'

def test_configIntegrity_default_net():
    try: configIntegrity(config)
    except InvalidConfig as e: assert False
    else: assert True
config['default_net'] = {}

def test_configIntegrity_def_if():
    try: configIntegrity(config)
    except InvalidConfig as e: assert False
    else: assert True
config['default_net']['interface'] = 'sampletext'


def test_configIntegrity_def_gw():
    try: configIntegrity(config)
    except InvalidConfig as e: assert False
    else: assert True
config['default_net']['gateway'] = 'sampletext'


def test_configIntegrity_chks():
    try: configIntegrity(config)
    except InvalidConfig as e: assert False
    else: assert True
config['checks'] = {}


def test_configIntegrity_chks_interval():
    try: configIntegrity(config)
    except InvalidConfig as e: assert False
    else: assert True
config['checks']['interval'] = 'sampletext'


def test_configIntegrity_chks_f_conn():
    try: configIntegrity(config)
    except InvalidConfig as e: assert False
    else: assert True
config['checks']['failed_conn'] = 'sampletext'


def test_configIntegrity_chks_f_dhcp():
    try: configIntegrity(config)
    except InvalidConfig as e: assert False
    else: assert True
config['checks']['failed_dhcp'] = 'sampletext'


def test_configIntegrity_chks_ping_c():
    try: configIntegrity(config)
    except InvalidConfig as e: assert False
    else: assert True
config['checks']['ping_c'] = 'sampletext'


def test_configIntegrity_ping_t():
    try: configIntegrity(config)
    except InvalidConfig as e: assert False
    else: assert True
config['checks']['ping_target'] = 'sampletext'


def test_configIntegrity_chks_ssids():
    try: configIntegrity(config)
    except InvalidConfig as e: assert False
    else: assert True
config['checks']['ssids'] = []

def test_configIntegrity_chks_no_ssids():
    try: configIntegrity(config)
    except InvalidConfig as e: assert False
    else: assert True
config['checks']['ssids'] = ['sampletext', 'sampletext']

def test_configIntegrity_():
    assert configIntegrity(config) == True
