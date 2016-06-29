#!/usr/bin/env python3

from setuptools import setup, find_packages
setup(
    name = "wifi-observer",
    version = "1",
    packages = find_packages(),
    test_suite = 'nose.collector'
)
