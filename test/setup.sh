#!/bin/bash

# BASE='/opt/wifi-observer'

export PATH=$PATH:$BASE/test/mockup
sqlite3 $BASE/wifi-observer.db.mock < $BASE/wifi-observer.db.sql
