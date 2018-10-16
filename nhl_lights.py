#!/usr/bin/env python3

import requests
import datetime
import pytz
import argparse
import dateutil.parser
import logging
import constants
from crontab import CronTab
from time import sleep
from pythonjsonlogger import jsonlogger

#logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%I:%M:%S',level=logging.INFO, filename=constants.LOGFILE)
logger = logging.getLogger()
logHandler = logging.StreamHandler(filename=constants.LOGFILE)
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)

now = datetime.datetime.today().strftime("%Y-%m-%d")
cst = pytz.timezone('US/Central')

'''
https://stackoverflow.com/questions/415511/how-to-get-current-time-in-python?rq=1
    go down to Aaron Hall's answer

https://statsapi.web.nhl.com/api/v1/schedule?expand=schedule.linescore&site=en_nhl
    gets the line scores for today's games
https://statsapi.web.nhl.com/api/v1/schedule?expand=schedule.scoringplays&site=en_nhl
    gets all the info for the goals scored in today's games
https://statsapi.web.nhl.com/api/v1/schedule?gamePk=2015020819&expand=schedule.broadcasts,schedule.teams,schedule.linescore,schedule.game.content.media.epg,schedule.scoringplays,schedule.ticket,schedule.decisions,team.leaders&leaderCategories=points,goals,assists&site=en_nhl
    cut the expand quiries to what you want
'''


class GeneralManager(object):
    def __init__(self, url=None, travel=None, state='Preview'):
        self.url = url
        self.travel = travel
        self.state = state
        self.score = 0

'''
class Bulbinfo(object):
    def __init__(self):
        self.on = None
        self.info = None
        self.flash_color = None

    def get_settings(self):
        try:
            r = requests.get('{}/groups/1'.format(constants.BRIDGEAPI)).json()['action']
            self.on = r['on']
            self.info = {'sat': r['sat'], 'bri': r['bri'], 'hue': r['hue'], 'alert': 'none'}
        except requests.exceptions.RequestException as e:
            print('could not get current state: {}'.format(e))

    def flash_lights(self):
        self.flash_color = {'sat': 254, 'bri': 254, 'hue': 65084, 'alert': 'lselect'}
        try:
            r = requests.put('{}/groups/1/action'.format(constants.BRIDGEAPI), json=self.flash_color)
            sleep(2)
            r = requests.put('{}/groups/1/action'.format(constants.BRIDGEAPI), json=self.info)
        except requests.exceptions.RequestException as e:
            print('could not alert lights: {}'.format(e))
'''

def bulb_current():
    try:
        r = requests.get('{}/groups/1'.format(constants.BRIDGEAPI)).json()['action']
        if not r['on']:
            return False
        else:
            return {'sat': r['sat'], 'bri': r['bri'], 'hue': r['hue'], 'alert': 'none'}
    except requests.exceptions.RequestException as e:
        logger.error('Could not get current bulb state ', extra={'error': e})

def flash():
    a = bulb_current()
    flash_color = {'sat': 254, 'bri': 254, 'hue': 65084, 'alert': 'lselect'}
    if not a:
        logger.info('Lights off, not flashing')
    else:
        try:
            r = requests.put('{}/groups/1/action'.format(constants.BRIDGEAPI), json=flash_color)
            sleep(2)
            r = requests.put('{}/groups/1/action'.format(constants.BRIDGEAPI), json=a)
        except requests.exceptions.RequestException as e:
            logger.error('could not set lights to alert, error: {}', extra={'error': e})

def build_argparse():
    parser = argparse.ArgumentParser(description='Flashes Hue lights when your team scores', prog='nhl_lights')
    parser.add_argument('-LGB', '--LetsGoBlues', action='store_true', help='Flag is used when game is about to start')
    args = parser.parse_args()

    return args


def checkgames():
    try:
        r = requests.get("{0}schedule?startDate={1}&endDate={1}".format(constants.BASEURL,now))
        if r.json()['totalItems'] == 0:
            logger.info('no NHL games today')
            exit()
        dict = r.json()['dates'][0]['games']
        for l in dict:
            if l['teams']['away']['team']['name'] == constants.TEAMNAME:
                GM.travel = 'away'
                game_url = l['link']
                game_time = l['gameDate']
                GM.state = l['status']['abstractGameState']
                logger.info('team is away and link is: {}'.format(game_url))
            elif l['teams']['home']['team']['name'] == constants.TEAMNAME:
                GM.travel = 'home'
                game_url = l['link']
                game_time = l['gameDate']
                GM.state = l['status']['abstractGameState']
                logger.info('team is home and link is: {}'.format(game_url))
    except requests.exceptions.RequestException as e:
        logger.error('Error getting games for today: {}', extra={'error': e})

    if GM.travel and not args.LetsGoBlues:
        game_date_obj = dateutil.parser.parse(game_time)
        game_time_cst = game_date_obj.astimezone(cst)

        write_cron(game_time_cst) ## needed if crontabbing
        logger.info('Game Later Tonight')
        exit()
    elif GM.travel and args.LetsGoBlues:
        GM.url = game_url
        delete_cron()
    else:
        logger.info('No game today, checking tomorrow')
        exit()


def game_state(url):
    # abstract == live during game
    # detailed == In Progress
    # coded game stat & code == 3
    try:
        r = requests.get(constants.NHLBASEURL + url)
        game_status = r.json()['gameData']['status']['abstractGameState']
        GM.state = game_status
    except requests.exceptions.RequestException as e:
        logger.error('Error: {}', extra={'error': e})


def game_score(url,state):
    try:
        r = requests.get(constants.NHLBASEURL + url)
        GM.state = r.json()['gameData']['status']['abstractGameState']
        score = r.json()['liveData']['boxscore']['teams'][state]['teamStats']['teamSkaterStats']['goals']
    except requests.exceptions.RequestException as e:
        logger.error('Error', extra={'error': e})

    if score > GM.score:
        logger.info('GOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOAAAAAALLLLLLLLLLLLLL')
        flash()
        GM.score = score
    elif score < GM.score:
        logger.info('something wrong or they took back a goal')
        GM.score = score
    else:
        pass


def write_cron(date):
    cron = CronTab(user=constants.CRONUSER)
    job = cron.new(command='python {} -LGB'.format(constants.SCRIPTPATH), comment='nhl lights - delete me')
    job.setall(date) # sets all to the datetime object)
    cron.write()


def delete_cron():
    cron=CronTab(user=constants.CRONUSER)
    jobs = cron.find_comment('nhl lights - delete me')
    for job in jobs:
        cron.remove(job)
    cron.write()


def main():
    logger.info('Script Starting')
    checkgames()
    logger.info('Game state is {} on cron start'.format(GM.state), extra={'state': GM.state})
    while GM.state != 'Live' and GM.state != 'Final':
        game_state(GM.url)
        sleep(60)
    logger.info('Game switched to: {}'.format(GM.state), extra={'state': GM.state})
    while GM.state == 'Live':
        game_score(GM.url,GM.travel)
        sleep(5)
    if GM.state == 'Final':
        logger.info('Game is over')


args = build_argparse()
GM = GeneralManager()

if __name__ == '__main__':
    main()