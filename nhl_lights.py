#!/usr/bin/python3.6

import requests
import datetime
import pytz
import dateutil.parser
from crontab import CronTab

BASEURL = "https://statsapi.web.nhl.com/api/v1/"
NHLBASEURL = "https://statsapi.web.nhl.com/"
TEAM_NEXT_GAME = "?expand=team.schedule.next"
BLUES = "19"
blues_next_game = "https://statsapi.web.nhl.com/api/v1/teams/19?expand=team.schedule.next"


'''
https://stackoverflow.com/questions/415511/how-to-get-current-time-in-python?rq=1
    go down to Aaron Hall's answer

https://statsapi.web.nhl.com/api/v1/schedule?expand=schedule.linescore&site=en_nhl
    gets the line scores for today's games
https://statsapi.web.nhl.com/api/v1/schedule?expand=schedule.scoringplays&site=en_nhl
    gets all the info for the goals scored in today's games
https://statsapi.web.nhl.com/api/v1/schedule?gamePk=2015020819&expand=schedule.broadcasts,schedule.teams,schedule.linescore,schedule.game.content.media.epg,schedule.scoringplays,schedule.ticket,schedule.decisions,team.leaders&leaderCategories=points,goals,assists&site=en_nhl
    cut the expand quiries to what you want

class TeamBuilding(object):
    def __init__(self):
        self.awayteam = None
        self.hometeam = None

    def do_something(self):
        pass

class Iter(TeamBuilding):
    def get_teams(self, json, place):
        self.json = json
        self.place = place

        self.awayteam = json['dates'][0]['games'][place]['teams']['away']['team']['name']
        self.hometeam = json['dates'][0]['games'][place]['teams']['away']['team']['name']


r = requests.get(BASEURL + "schedule?startDate=2018-01-24&endDate=2018-01-24")

dict = r.json()['dates'][0]['games']
for l in dict:
    print("Away: {}".format(l['teams']['away']['team']['name']))
    print("Home: {}".format(l['teams']['home']['team']['name']))


a = Iter()
for x in range(0,len(r.json()['dates'][0]['games'])):
    a.get_teams(r.json(),x)

print(a.team)
 ### /proof of concept stuff ###

#### nhl is in utc ** crying of happiniess ###


now = datetime.datetime.today().strftime("%Y-%m-%d")
now2 = datetime.datetime.today().isoformat(timespec='seconds')
utc_now = datetime.datetime.utcnow().isoformat(timespec='seconds')


r = requests.get(blues_next_game)

game_date = r.json()['teams'][0]['nextGameSchedule']['dates'][0]['date']
game_url = r.json()['teams'][0]['nextGameSchedule']['dates'][0]['games'][0]['link']
game_date_utc = r.json()['teams'][0]['nextGameSchedule']['dates'][0]['games'][0]['gameDate']

if utc_now[:10] == game_date:
    print("match!")
    r = requests.get(NHLBASEURL + game_url)

    r.json()

game_status = r.json()['gameData']['status']['abstractGameState']
home_team = r.json()['gameData']['teams']['home']['abbreviation']
away_team = r.json()['gameData']['teams']['away']['abbreviation']

'''
class CronManager(object):
    def __init__(self,user):
        self.user = user
        self.cron = CronTab(user=True)
    def write_cron(self, date):
        # you can set to datetime
        # job.setall(datetime(2000, 4, 2, 10, 2))
        self.cron = cron
        self.job = job
        job = cron.new(command="python3 /home/joel/python/dev/xyz.py")
        job.minute.on(time.minute)
        job.hour.on(time.hour)
        job.day.on(time.day)
        job.month.on(time.month)
        job.enable()
        #cron.write()

    def delete_cron(self, job):
        self.job = job
        self.cron.remove(job)


state = None

now = '2018-01-30'
#now = datetime.datetime.today().strftime("%Y-%m-%d")
now2 = datetime.datetime.today().isoformat(timespec='seconds')
utc_now = datetime.datetime.utcnow().isoformat(timespec='seconds')
utc_now2 = datetime.datetime.now(pytz.utc)
cst = pytz.timezone('US/Central')

def checkgames(state):
    r = requests.get("{0}schedule?startDate={1}&endDate={1}".format(BASEURL,now))

    dict = r.json()['dates'][0]['games']
    for l in dict:
        if l['teams']['away']['team']['name'] == 'St. Louis Blues':
            state = 'away'
            game_url = l['link']
            game_time = l['gameDate']
            print('team is away and link is: {}'.format(game_url))
        elif l['teams']['home']['team']['name'] == 'St. Louis Blues':
            state = 'home'
            game_url = l['link']
            game_time = l['gameDate']
            print('team is home and link is: {}'.format(game_url))

    if state:
        game_date_obj = dateutil.parser.parse(game_time)
        game_time_cst = game_date_obj.astimezone(cst)

        sleep_time = (game_date_obj - utc_now2).total_seconds() ## needed if sleeping
        write_cron(game_time_cst) ## needed if crontabbing

    else:
        print('No game today, checking tomorrow')



    print(sleep_time)
    #if state != None:
    #    gametoday(game_url,state)

def gametime(game_url):
    r = requests.get(NHLBASEURL + game_url)
    gametime()

def gametoday(game_url,state):
    r = requests.get(NHLBASEURL + game_url)
    game_status = r.json()['gameData']['status']['abstractGameState']
    score = r.json()['liveData']['boxscore']['teams'][state]['teamStats']['teamSkaterStats']['goals']

def write_cron(time)
    cron = CronTab(user='joel')
    job = cron.new(command="python3 /home/joel/python/dev/xyz.py")
    job.minute.on(time.minute)
    job.hour.on(time.hour)
    job.day.on(time.day)
    job.month.on(time.month)
    job.enable()
    cron.write()

    return job


def main():
    checkgames(state)


if __name__ == '__main__':
    main()





