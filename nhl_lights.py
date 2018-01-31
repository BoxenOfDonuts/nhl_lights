#!/usr/bin/python3.6

"""
Flashes Hue lights when your team scores

Author:
Version: .5
Modified 01/30/18
Python Version: 3.6
"""

import requests
import datetime
import pytz
import argparse
import dateutil.parser
from crontab import CronTab
from time import sleep
from phue import Bridge

BASEURL = "https://statsapi.web.nhl.com/api/v1/"
NHLBASEURL = "https://statsapi.web.nhl.com/"
travel = None
CRONUSER = ''
TEAMNAME = 'St. Louis Blues'
lights = Bridge('')

#now = "2018-01-25"
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

class Bulbinfo(object):
    def get_settings(self, on, sat, bri, hue):
        self.on = on
        self.sat = sat
        self.bri = bri
        self.hue = hue

        self.info = {'on': on, 'sat': sat, 'bri': bri, 'hue': hue}

    def flash_lights(self):
        self.goal_flash = {'alert':'select'}

def build_argparse():
    parser = argparse.ArgumentParser(description='Flashes Hue lights when your team scores',prog='nhl_lights')
    parser.add_argument('-LGB', '--LetsGoBlues', action='store_true', help='Flag is used when game is about to start')
    args = parser.parse_args()

    return args


def checkgames(travel):
    try:
        r = requests.get("{0}schedule?startDate={1}&endDate={1}".format(BASEURL,now))
        if r.json()['totalItems'] == 0:
            print('no NHL games today')
            exit()
        dict = r.json()['dates'][0]['games']
        for l in dict:
            if l['teams']['away']['team']['name'] == TEAMNAME:
                travel = 'away'
                game_url = l['link']
                game_time = l['gameDate']
                print('team is away and link is: {}'.format(game_url))
            elif l['teams']['home']['team']['name'] == TEAMNAME:
                travel = 'home'
                game_url = l['link']
                game_time = l['gameDate']
                print('team is home and link is: {}'.format(game_url))
    except requests.exceptions.RequestException as e:
        print('Error getting games for today: {}'.format(e))

    if travel and not args.LetsGoBlues:
        game_date_obj = dateutil.parser.parse(game_time)
        game_time_cst = game_date_obj.astimezone(cst)

        write_cron(game_time_cst) ## needed if crontabbing
        print('Game Later Tonight')
        exit()
    elif travel and args.LetsGoBlues:
        GM.travel = travel
        GM.url = game_url
        delete_cron()
    else:
        print('No game today, checking tomorrow')
        exit()


def game_state(url):
    # abstract == live during game
    # detailed == In Progress
    # coded game stat & code == 3
    try:
        r = requests.get(NHLBASEURL + url)
        game_status = r.json()['gameData']['status']['abstractGameState']
        GM.state = game_status
    except requests.exceptions.RequestException as e:
        print('Error: {}'.format(e))

def game_score(url,state):
    try:
        r = requests.get(NHLBASEURL + url)
        GM.state = r.json()['gameData']['status']['abstractGameState']
        score = r.json()['liveData']['boxscore']['teams'][state]['teamStats']['teamSkaterStats']['goals']
    except requests.exceptions.RequestException as e:
        print('Error: {}'.format(e))

    if score > GM.score:
        print('GOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOAAAAAALLLLLLLLLLLLLL')
        # do hue blinking lights
        GM.score = score
    elif score < GM.score:
        print('something wrong or they took back a goal')
        GM.score = score
    else:
        pass

def write_cron(date):
    cron = CronTab(user=CRONUSER)
    job = cron.new(command='python3 /home/joel/python/dev/xyz.py -LGB',comment='nhl lights - delete me')
    job.setall(date) # sets all to the datetime object)
    cron.write()


def delete_cron():
    cron=CronTab(user=CRONUSER)
    jobs = cron.find_comment('nhl lights - delete me')
    for job in jobs:
        cron.remove(job)
    cron.write()


def main():
    checkgames(travel)
    while GM.state != 'Live': # still guessing on that tag
        game_status(GM.url)
        sleep(60)
    while GM.state == 'Live': # still guessing on that tag
        game_score(GM.url,GM.travel)
        sleep(5)
    if GM.state == 'Final':
        print('game is over')


args = build_argparse()
GM = GeneralManager()

if __name__ == '__main__':
    main()
