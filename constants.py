#!/usr/bin/env python3

import os
import configparser

"""
Constants File
"""

CONFIGFILE = os.path.join(os.path.dirname(__file__), 'config.ini')
LOGFILE = '/mnt/nhl_lights/nhl_lights.log'
SCRIPTPATH = os.path.abspath(__file__)


config = configparser.ConfigParser()
config.read(CONFIGFILE)

BASEURL = "https://statsapi.web.nhl.com/api/v1/"
NHLBASEURL = "https://statsapi.web.nhl.com/"
BRIDGEIP = config['hue']['ip']
HUEUSER = config['hue']['user']
BRIDGEAPI = 'http://{}/api/{}'.format(BRIDGEIP, HUEUSER)
CRONUSER = config['user']['user']
TEAMNAME = config['user']['teamname']
