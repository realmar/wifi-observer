import os, sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from lib.exceptions import *

from nose.tools import raises

def test_InvalidConfig():
    ic = InvalidConfig('sampletext')
    assert ic.__str__() == 'Invalid Configuration: sampletext'
    assert ic.value == 'sampletext'
