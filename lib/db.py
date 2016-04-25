# Created by: Anastassios Martakos
# Copyright (c) 2016 Anastassios Martakos

#!/usr/bin/env python3.4

import sqlite3

def connectDB(db):
    return sqlite3.connect(db)

def writeCheck(db_conn, sanity, timeout):
    if(not checkEntry(db_conn, 'bssids', 'bssid', sanity['bssid'])):
        insertSingle(db_conn, 'bssids', 'bssid', sanity['bssid'])
    if(not checkEntry(db_conn, 'ssids', 'bssid', sanity['ssid'])):
        insertSingle(db_conn, 'ssids', 'bssid', sanity['ssid'])

    bssid_id = checkEntry(db_conn, 'bssids', 'bssid', sanity['bssid'])
    ssid_id = checkEntry(db_conn, 'ssids', 'bssid', sanity['ssid'])

    time_needed = 'NULL' if sanity['time_needed'] > timeout else sanity['time_needed']
    ping_average = 'NULL' if sanity['ping_average'] == 0 else sanity['ping_average']

    sql_string = 'INSERT INTO data(time_needed, ping_average, time_start, dbm, ssid_fk, bssid_fk) VALUES(' + time_needed + ', ' + ping_average + ', ' + sanity['time_start'] + ', ' + sanity['dbm'] + ', ' + ssid_id + ', ' + bssid_id + ')'

    try:
        entries = db_conn.cursor.execute(sql_string)
    except sqlite3.Error as e:
        return True

def checkEntry(db_conn, table, column, search):
    sql_string = 'SELECT id FROM ' + table + ' WHERE ' + column + '="' + search + '""'
    try:
        entries = db_conn.cursor.execute(sql_string)
    except sqlite3.Error as e:
        return True

    for entry in entries.fetchall():
        return entry

    return False

def insertSingle(db_conn, table, column, value):
    sql_string = 'INSERT INTO ' + table + ' VALUES(' + columm + ')' + ' VALUES("' + value + '")'

    try:
        entries = db_conn.cursor.execute(sql_string)
    except sqlite3.Error as e:
        return True

    return False
