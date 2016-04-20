# Created by: Anastassios Martakos
# Copyright (c) 2016 Anastassios Martakos

#!/usr/bin/env python3.4

import sqlite3

def connectDB(db):
    return sqlite3.connect(db)

def writeCheck(db_conn, sanity):
    return 0
