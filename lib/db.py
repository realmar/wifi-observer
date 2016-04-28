# Created by: Anastassios Martakos
# Copyright (c) 2016 Anastassios Martakos

#!/usr/bin/env python3.4

import sqlite3

def connectDB(db):
    return sqlite3.connect(db)

def writeCheck(db_conn, sanity, timeout):
    bssid_id = sanity['bssid']
    c = db_conn.cursor()

    if bssid_id != 'NULL':
        if(not checkEntry(db_conn, 'bssids', 'bssid', sanity['bssid'])):
            insertSingle(db_conn, 'bssids', 'bssid', sanity['bssid'])
        bssid_id = checkEntry(db_conn, 'bssids', 'bssid', sanity['bssid'])

    if(not checkEntry(db_conn, 'ssids', 'ssid', sanity['ssid'])):
        insertSingle(db_conn, 'ssids', 'ssid', sanity['ssid'])
    ssid_id = checkEntry(db_conn, 'ssids', 'ssid', sanity['ssid'])

    time_needed = 'NULL' if sanity['time_needed'] > timeout else str(int(sanity['time_needed']))
    ping_average = 'NULL' if sanity['ping_average'] == 0 else str(sanity['ping_average'])

    sql_string = 'INSERT INTO data(time_needed, ping_average, time_start, dbm, ssid_fk, bssid_fk) VALUES(' + str(float("{0:.2f}".format(time_needed))) + ', ' + str(ping_average) + ', ' + str(int(sanity['time_start'])) + ', ' + str(sanity['dbm']) + ', ' + str(ssid_id) + ', ' + str(bssid_id) + ')'

    print(sql_string)

    try:
        entries = c.execute(sql_string)
    except sqlite3.Error as e:
        print('sql error: ' + e)
        return True

    commit(db_conn)

def checkEntry(db_conn, table, column, search):
    c = db_conn.cursor()

    sql_string = 'SELECT id FROM ' + table + ' WHERE ' + column + '="' + search + '"'
    try:
        entries = c.execute(sql_string)
    except sqlite3.Error as e:
        print('sql error: ' + e)
        return True

    for entry in entries.fetchall():
        return entry[0]

    commit(db_conn)

    return False

def insertSingle(db_conn, table, column, value):
    c = db_conn.cursor()

    sql_string = 'INSERT INTO ' + table + '(' + column + ')' + ' VALUES("' + str(value) + '")'

    try:
        entries = c.execute(sql_string)
    except sqlite3.Error as e:
        print('sql error: ' + e)
        return True

    commit(db_conn)

    return False

def commit(db_conn):
    db_conn.commit()
