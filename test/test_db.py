import os, sys, sqlite3, datetime
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)

from nose.util import absfile

from lib.db import *
from lib.exceptions import InvalidConfig

from test.helpers.helper_funcs import loadConfig, buildSanity

config = loadConfig(BASE_DIR + '/test/mockup/wifi-observer.conf.mock')
DB_PATH = os.path.join(BASE_DIR, config['database']) + '.mock'

def test_connectDB():
    __db_connection = connectDB(DB_PATH)
    assert type(__db_connection) == sqlite3.Connection
    __db_connection.close()

class TestDB:
    def __init__(self):
        self.db_connection = connectDB(DB_PATH)

    def __del__(self):
        self.db_connection.close()

    def test_01_writeCheck(self):
        assert type(writeCheck(db_conn=self.db_connection, sanity=buildSanity(), timeouts={'conn' : config['checks']['failed_conn'], 'dhcp' : config['checks']['failed_dhcp']}, location=config['computer']['location'])) == type(42)

    def test_checkEntry(self):
        print(checkEntry(self.db_connection, 'ssids', 'ssid', 'eth-5'))
        assert not checkEntry(self.db_connection, 'ssids', 'ssid', 'eth-5') == False
        assert checkEntry(self.db_connection, 'ssids', 'ssid', 'samplessid') == False

    def test_insertSingle(self):
        assert not insertSingle(self.db_connection, 'errors', 'code', 'sampleerror')

    def test_getAllDate(self):
        assert type(getAllDates(DB_PATH)) == type([])

    def test_getSSIDs(self):
        assert type(getSSIDs(DB_PATH)) == type([])

    def test_getSSIDsName(self):
        assert type(getSSIDsName(DB_PATH)) == type([])

    def test_generateCSV(self):
        current_week = datetime.datetime.today().strftime("%W")
        current_year = datetime.datetime.today().strftime("%Y")

        generateCSV(self.db_connection, BASE_DIR + '/test/temp/test.csv', str(int(current_week) - 1), current_week)

        assert not absfile(BASE_DIR + '/test/temp/test.csv') == None

    def test_getStats(self):
        result = getStats(DB_PATH)

        assert type(result) == type([])
        assert type(result[0]) == type([])
        assert type(result[1]) == type({})
