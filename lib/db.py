# Created by: Anastassios Martakos
# Copyright (c) 2016 Anastassios Martakos

#!/usr/bin/env python3.4

import sqlite3

def connectDB(db):
    return sqlite3.connect(db)

def writeCheck(db_conn, sanity, timeouts):
    bssid_id = sanity['bssid']

    if bssid_id != 'NULL':
        if(not checkEntry(db_conn, 'bssids', 'bssid', sanity['bssid'])):
            insertSingle(db_conn, 'bssids', 'bssid', sanity['bssid'])
        bssid_id = checkEntry(db_conn, 'bssids', 'bssid', sanity['bssid'])

    if(not checkEntry(db_conn, 'ssids', 'ssid', sanity['ssid'])):
        insertSingle(db_conn, 'ssids', 'ssid', sanity['ssid'])
    ssid_id = checkEntry(db_conn, 'ssids', 'ssid', sanity['ssid'])

    time_needed_conn = 'NULL' if sanity['time_needed_conn'] > timeouts['conn'] else sanity['time_needed_conn']
    time_needed_dhcp = 'NULL' if sanity['time_needed_dhcp'] > timeouts['dhcp'] or time_needed_conn == 'NULL' else sanity['time_needed_dhcp']
    ping_average = 'NULL' if sanity['ping_average'] == 0 else str(sanity['ping_average'])

    if time_needed_conn != 'NULL':
        time_needed_conn = str("{0:.2f}".format(float(time_needed_conn)))
    if time_needed_dhcp != 'NULL':
        time_needed_dhcp = str("{0:.2f}".format(float(time_needed_dhcp)))

    sql_string = 'INSERT INTO data(time_needed_conn, time_needed_dhcp, ping_average, time_start, dbm, ssid_fk, bssid_fk) VALUES(' + str(time_needed_conn) + ', ' + str(time_needed_dhcp) + ', ' + str(ping_average) + ', ' + str(int(sanity['time_start'])) + ', ' + str(sanity['dbm']) + ', ' + str(ssid_id) + ', ' + str(bssid_id) + ')'

    entries = executeSQL(db_conn, sql_string)

    commit(db_conn)

def checkEntry(db_conn, table, column, search):
    sql_string = 'SELECT id FROM ' + table + ' WHERE ' + column + '="' + search + '"'
    entries = executeSQL(db_conn, sql_string)

    for entry in entries.fetchall():
        return entry[0]

    commit(db_conn)

    return False

def insertSingle(db_conn, table, column, value):
    sql_string = 'INSERT INTO ' + table + '(' + column + ')' + ' VALUES("' + str(value) + '")'
    entries = executeSQL(db_conn, sql_string)
    commit(db_conn)

    return False

def getUniqueDates(db_path):
    db_conn = connectDB(db_path)

    ret_val = []
    sql_string = 'SELECT DISTINCT date(time_start, "unixepoch", "localtime") FROM data'
    entries = executeSQL(db_conn, sql_string)

    for entry in entries.fetchall():
        ret_val.append({'date' : entry[0]})

    return ret_val

def getGlobStats(db_path):
    db_conn = connectDB(db_path)

    ret_val = {}
    ret_val['ssids'] = getGlob(db_conn, 'ssid')
    ret_val['bssids'] = getGlob(db_conn, 'bssid')
    ret_val['total'] = []
    ret_val['total'].append({'type' : 'total', 'name' : 'total', 'data' : { 'total' : 0, 'conn_failed' : 0, 'dhcp_failed' : 0 }})

    for stat in ret_val['ssids']:
        ret_val['total'][0]['data']['total'] += stat['data']['total']
        ret_val['total'][0]['data']['conn_failed'] += stat['data']['conn_failed']
        ret_val['total'][0]['data']['dhcp_failed'] += stat['data']['dhcp_failed']

    return ret_val

def getAPbyName(db_conn, column, id):
    sql_string = "SELECT " + column + " FROM " + column + "s WHERE id=" + str(id)
    entries = executeSQL(db_conn, sql_string)
    for entry in entries.fetchall():
        return entry[0]

def getGlob(db_conn, collumn):
    ret_val = []

    curr_obj = getAllIDs(db_conn, collumn + 's')

    for obj in curr_obj:
        tmp = {}

        tmp['type'] = collumn
        tmp['name'] = getAPbyName(db_conn, collumn, obj)
        tmp['data'] = {}

        sql_string = "SELECT COUNT(id) FROM data WHERE " + collumn + "_fk=" + str(obj)
        entries = executeSQL(db_conn, sql_string)
        for entry in entries.fetchall():
            tmp['data']['total'] = entry[0]

        sql_string = "SELECT COUNT(id) FROM data WHERE time_needed_conn IS NULL AND " + collumn + "_fk=" + str(obj)
        entries = executeSQL(db_conn, sql_string)
        for entry in entries.fetchall():
            tmp['data']['conn_failed'] = entry[0]

        sql_string = "SELECT COUNT(id) FROM data WHERE time_needed_dhcp IS NULL AND " + collumn + "_fk=" + str(obj)
        entries = executeSQL(db_conn, sql_string)
        for entry in entries.fetchall():
            tmp['data']['dhcp_failed'] = entry[0]

        ret_val.append(tmp)

    return ret_val

def getAllIDs(db_conn, table):
    ret_val = []

    sql_string = "SELECT id FROM " + table
    entries = executeSQL(db_conn, sql_string)
    for entry in entries.fetchall():
        ret_val.append(entry[0])

    return ret_val

def getSingleStat(db_conn, date, collumn):
    ret_val = []

    curr_obj = getAllIDs(db_conn, collumn + 's')

    for obj in curr_obj:
        tmp = {}

        tmp['type'] = collumn
        tmp['name'] = getAPbyName(db_conn, collumn, obj)
        tmp['data'] = {}

        sql_string = 'SELECT COUNT(id) FROM data WHERE datetime(time_start, "unixepoch", "localtime") > datetime("' + date + '", "localtime", "start of day") AND datetime(time_start, "unixepoch", "localtime") < datetime("' + date + '", "localtime", "start of day", "+24 hours") AND ' + collumn + "_fk=" + str(obj)
        entries = executeSQL(db_conn, sql_string)
        for entry in entries.fetchall():
            tmp['data']['total'] = entry[0]

        sql_string = 'SELECT COUNT(id) FROM data WHERE datetime(time_start, "unixepoch", "localtime") > datetime("' + date + '", "localtime", "start of day") AND datetime(time_start, "unixepoch", "localtime") < datetime("' + date + '", "localtime", "start of day", "+24 hours") AND time_needed_conn IS NULL AND ' + collumn + "_fk=" + str(obj)
        entries = executeSQL(db_conn, sql_string)
        for entry in entries.fetchall():
            tmp['data']['conn_failed'] = entry[0]

        sql_string = 'SELECT COUNT(id) FROM data WHERE datetime(time_start, "unixepoch", "localtime") > datetime("' + date + '", "localtime", "start of day") AND datetime(time_start, "unixepoch", "localtime") < datetime("' + date + '", "localtime", "start of day", "+24 hours") AND time_needed_dhcp IS NULL AND ' + collumn + "_fk=" + str(obj)
        entries = executeSQL(db_conn, sql_string)
        for entry in entries.fetchall():
            tmp['data']['dhcp_failed'] = entry[0]

        ret_val.append(tmp)

    return ret_val


def getStat(db_path, date):
    db_conn = connectDB(db_path)

    ret_val = {}
    ret_val['ssids'] = getSingleStat(db_conn, date, 'ssid')
    ret_val['bssids'] = getSingleStat(db_conn, date, 'bssid')
    ret_val['total'] = []
    ret_val['total'].append({'type' : 'total', 'name' : 'total', 'data' : { 'total' : 0, 'conn_failed' : 0, 'dhcp_failed' : 0 }})

    for stat in ret_val['ssids']:
        ret_val['total'][0]['data']['total'] += stat['data']['total']
        ret_val['total'][0]['data']['conn_failed'] += stat['data']['conn_failed']
        ret_val['total'][0]['data']['dhcp_failed'] += stat['data']['dhcp_failed']

    return ret_val

def commit(db_conn):
    db_conn.commit()

def executeSQL(db_conn, sql_string):
    c = db_conn.cursor()

    try:
        entries = c.execute(sql_string)
    except sqlite3.Error as e:
        print('sql error: ' + e)
        return True

    return entries
