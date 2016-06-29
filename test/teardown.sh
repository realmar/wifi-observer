#!/bin/bash

BASE='/opt/wifi-observer'

rm $BASE/wifi-observer.db.mock
rm $BASE/test/temp/*
touch $BASE/test/temp/.no_delete
