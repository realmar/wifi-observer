#!/bin/bash

# BASE='/opt/wifi-observer'

export PATH=$BASE/test/mockup:$PATH
sqlite3 $BASE/wifi-observer.db.mock < $BASE/wifi-observer.db.sql
