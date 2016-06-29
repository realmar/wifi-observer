import yaml

def loadConfig(path):
    file = open(path, 'r')
    config = yaml.load(file)
    file.close()

    return config

def buildSanity():
    return {'errors': [{'code' : 'CTRL-EVENT-EAP-FAILURE', 'id' : 0}], 'dbm': '-60', 'time_needed_conn': 0.0040204524993896484, 'ping_average': '3.332', 'time_needed_dhcp': 0.17487239837646484, 'bssid': 'a0:48:1c:35:16:80', 'ssid': 'eth-5', 'time_start': 1467116849.632759}
