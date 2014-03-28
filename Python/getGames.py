# very kludgy fix to solve issue importing numpy
import sys
sys.path.reverse()
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime, date
import csv

# years = [2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013]
years = [2014]
teams = pd.read_csv('teams.csv', index_col=0, sep='\t')
# print teams
# {0} = prefix_1, {1} = year, {2} = prefix_2
BASE_URL = 'http://espn.go.com/nba/team/schedule/_/name/{0}/year/{1}/{2}'
BASE_GAME_URL = 'http://espn.go.com/nba/playbyplay?gameId={0}&period=0'

# couldn't figure out how to select data using the dataframe
teamDict = {}
with open('teams.csv', 'rb') as csvfile:
  csvTeams = csv.reader(csvfile, delimiter = '\t')
  for name, prefix_1, prefix_2, url in csvTeams:
    teamDict[prefix_2] = name


game_id = []
dates = []
home_team = []
home_team_score = []
visit_team = []
visit_team_score = []
overtime = []

# year = 2006
for year in years:
  print 'year is now ' + str(year)
  for index, row in teams.iterrows():
    _team = index
    r = requests.get(BASE_URL.format(row['prefix_1'], year, row['prefix_2']))
    table = BeautifulSoup(r.text).table
    for row in table.find_all('tr')[1:]:
      columns = row.find_all('td')
      try:
        _id = columns[2].a['href'].split('?id=')[1]
        _home = True if columns[1].li.text == 'vs' else False
        _other_team = columns[1].find_all('a')[1]['href']
        _other_team = _other_team.split('/')[-1:][0]
        _other_team = teamDict[_other_team]
        _score = columns[2].a.text.split(' ')[0].split('-')
        _extratime = True if len(columns[2].a.text.split(' ')) == 2 and columns[2].a.text.split(' ')[1] == 'OT' else False
        _won = True if columns[2].span.text == 'W' else False

        game_id.append(_id)
        overtime.append(_extratime)
        home_team.append(_team if _home else _other_team)
        visit_team.append(_team if not _home else _other_team)
        try:
          d = datetime.strptime(columns[0].text, '%a, %b %d')
          dates.append(date(year, d.month, d.day))
        except Exception as e:
          #Handling leap years
          d = date(year, 2, 28)
          dates.append(d)

        if _home:
          if _won:
            home_team_score.append(_score[0])
            visit_team_score.append(_score[1])

          else:
            home_team_score.append(_score[1])
            visit_team_score.append(_score[0])

        else:
          if _won:
            home_team_score.append(_score[1])
            visit_team_score.append(_score[0])

          else:
            home_team_score.append(_score[0])
            visit_team_score.append(_score[1])

      except Exception as e:
        pass

dic = {'id': game_id, 'date': dates, 'home_team': home_team, 'visit_team': visit_team,
        'home_team_score': home_team_score, 'visit_team_score': visit_team_score, 'overtime': overtime}


games = pd.DataFrame(dic).drop_duplicates(cols='id').set_index('id')

# games.to_csv('games.csv')
games.to_csv('2014games.csv')
