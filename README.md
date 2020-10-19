# nhl_lights
Flash Hue Lights when your NHL team scores

# NHL API Documentation

[OpenAPI 3.0 specification file for the NHL API](https://github.com/erunion/sport-api-specifications/tree/master/nhl) thanks to @[erunion](https://github.com/erunion)

[Additional API Documentation](https://github.com/dword4/nhlapi)

### <a name="teams"></a>Teams

`GET https://statsapi.web.nhl.com/api/v1/teams` Returns a list of data about
all teams including their id, venue details, division, conference and franchise information.

`GET https://statsapi.web.nhl.com/api/v1/teams/ID` Returns the same information as above just
for a single team instead of the entire league.

### <a name="Getting Started"></a>Getting Started
1. Open the teams link above and search for the team you want to monitor. In the JSON response there is an ID value.
```
{
    "id" : 19,
    "name" : "St. Louis Blues",
    "link" : "/api/v1/teams/19",
    "venue" : {
      "id" : 5076,
      "name" : "Enterprise Center",
      "link" : "/api/v1/venues/5076",
      "city" : "St. Louis",
      "timeZone" : {
        "id" : "America/Chicago",
        "offset" : -5,
        "tz" : "CDT"
      }
```
Plug that ID number in the config file for the `teamname` value under user

2. The `user` field under user is the username of the account running the python. It updates the cron for the respecitve user

3. To create a user for the hue, see the offical documentation [here](https://developers.meethue.com/develop/get-started-2/)

4. The logging path is currently configured in the `constants.py` file. You can update it to whatever path you want the program to log to.
