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

def getAPbyName(db_conn, column, id):
    sql_string = "SELECT " + column + " FROM " + column + "s WHERE id=" + str(id)
    entries = executeSQL(db_conn, sql_string)
    for entry in entries.fetchall():
        return entry[0]

def getStats(db_path):
    db_conn = connectDB(db_path)

    DATE = 0
    SSID = 1
    BSSID = 2
    ID_COUNT = 3
    DHCP_NULL = 4
    CONN_NULL = 5

    # stats data structure
    # { <date> :    { <type> : { <name> {
    #                                       <total_checks> : <int>
    #                                       <conn_null_count> : <int>
    #                                       <dhcp_null_count : <int>
    #                                   }
    #                           }
    #               }
    # }
    #
    # type can be:  total
    #               ssid
    #               bssid

    stats = {}

    # glob stat data structure is the same as stats
    # just without the <date>

    glob_stats = {}

    types = [ 'ssid', 'bssid' ]

    sql_string = 'select date(time_start, "unixepoch", "localtime", "start of day") as time_start_coll , ssid_fk,bssid_fk,count(id),time_needed_dhcp IS NULL as time_needed_dhcp_null,time_needed_conn IS NULL as time_needed_conn_null from data group by ssid_fk,bssid_fk, time_needed_dhcp IS NULL, time_needed_conn IS NULL, date(time_start, "unixepoch", "localtime", "start of day") order by datetime(time_start, "unixepoch", "localtime", "start of day")'
    entries = executeSQL(db_conn, sql_string)
    for entry in entries.fetchall():
        for type in types:
            try: stats[entry[DATE]]
            except: stats[entry[DATE]] = {}

            try: stats[entry[DATE]][type]
            except: stats[entry[DATE]][type] = {}

            name = getAPbyName(db_conn, type, entry[SSID])
            try: stats[entry[DATE]][type][name]
            except: stats[entry[DATE]][type][name] = {}
            try: stats[entry[DATE]][type][name]['total_checks']
            except: stats[entry[DATE]][type][name]['total_checks'] = 0
            stats[entry[DATE]][type][name]['total_checks'] += entry[ID_COUNT]
            try: stats[entry[DATE]][type][name]['conn_null_count']
            except: stats[entry[DATE]][type][name]['conn_null_count'] = 0
            try: stats[entry[DATE]][type][name]['dhcp_null_count']
            except: stats[entry[DATE]][type][name]['dhcp_null_count'] = 0
            stats[entry[DATE]][type][name]['conn_null_count'] += entry[ID_COUNT] if entry[CONN_NULL] == 1 else 0
            stats[entry[DATE]][type][name]['dhcp_null_count'] += entry[ID_COUNT] if entry[DHCP_NULL] == 1 else 0

            try: stats[entry[DATE]]['total']
            except: stats[entry[DATE]]['total'] = {}
            try: stats[entry[DATE]]['total']['total']
            except: stats[entry[DATE]]['total']['total'] = {}
            try: stats[entry[DATE]]['total']['total']['total_checks']
            except: stats[entry[DATE]]['total']['total']['total_checks'] = 0
            stats[entry[DATE]]['total']['total']['total_checks'] += entry[ID_COUNT]
            try: stats[entry[DATE]]['total']['total']['conn_null_count']
            except: stats[entry[DATE]]['total']['total']['conn_null_count'] = 0
            try: stats[entry[DATE]]['total']['total']['dhcp_null_count']
            except: stats[entry[DATE]]['total']['total']['dhcp_null_count'] = 0
            stats[entry[DATE]]['total']['total']['conn_null_count'] += entry[ID_COUNT] if entry[CONN_NULL] == 1 else 0
            stats[entry[DATE]]['total']['total']['dhcp_null_count'] += entry[ID_COUNT] if entry[DHCP_NULL] == 1 else 0

            try: glob_stats[type]
            except: glob_stats[type] = {}
            try: glob_stats[type]['total']
            except: glob_stats[type]['total'] = {}
            try: glob_stats[type]['total']['total_checks']
            except: glob_stats[type]['total']['total_checks'] = 0
            glob_stats[type]['total']['total_checks'] += entry[ID_COUNT]
            try: glob_stats[type]['total']['conn_null_count']
            except: glob_stats[type]['total']['conn_null_count'] = 0
            try: glob_stats[type]['total']['dhcp_null_count']
            except: glob_stats[type]['total']['dhcp_null_count'] = 0
            glob_stats[type]['total']['conn_null_count'] += entry[ID_COUNT] if entry[CONN_NULL] == 1 else 0
            glob_stats[type]['total']['dhcp_null_count'] += entry[ID_COUNT] if entry[DHCP_NULL] == 1 else 0

            try: glob_stats['total']
            except: glob_stats['total'] = {}
            try: glob_stats['total']['total']
            except: glob_stats['total']['total'] = {}
            try: glob_stats['total']['total']['total_checks']
            except: glob_stats['total']['total']['total_checks'] = 0
            glob_stats['total']['total']['total_checks'] += entry[ID_COUNT]
            try: glob_stats['total']['total']['conn_null_count']
            except: glob_stats['total']['total']['conn_null_count'] = 0
            try: glob_stats['total']['total']['dhcp_null_count']
            except: glob_stats['total']['total']['dhcp_null_count'] = 0
            glob_stats['total']['total']['conn_null_count'] += entry[ID_COUNT] if entry[CONN_NULL] == 1 else 0
            glob_stats['total']['total']['dhcp_null_count'] += entry[ID_COUNT] if entry[DHCP_NULL] == 1 else 0

    return [stats, glob_stats]

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
