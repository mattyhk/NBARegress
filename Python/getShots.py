# very kludgy fix to solve issue importing numpy
import sys
import re
sys.path.reverse()
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
from datetime import datetime, date
import csv
import urllib2

playerShotDict = {}

class Shot(object):
  # A shot has serveral fields: distance, time, type, made, point, point differential
  def __init__(self, date, time, team, opposition, quarter, score, scoreDiff, shotType, home, overtime, distance, player, made, gameWon):
    # self.id = num
    self.date = date
    self.time = time
    self.team = team
    self.homeGame = home
    self.opposition = opposition
    self.quarter = quarter
    self.score = score
    self.scoreDiff = scoreDiff
    self.shotType = shotType
    self.overtime = overtime
    self.distance = distance
    self.player = player
    self.made = made
    self.gameWon = gameWon

class Player(object):
  # A player has two attributes: made shots and missed shots
  # Each attribute is an array of shot objects
  def __init__(self, name):
    self.made = []
    self.missed = []
    self.name = name

  def addMadeShot(self, shot):
    self.made.append(shot)

  def addMissedShot(self, shot):
    self.missed.append(shot)



# Given a game id, goes through the page collecting all the shots 
def getShotsForPage(id, homeTeam, awayTeam, gameDate, homeScore, awayScore):
  gameUrl = 'http://espn.go.com/nba/playbyplay?gameId=' + str(id) + '&period=0'
  page = urllib2.urlopen(gameUrl)
  soup = bs(page)
  pattern = re.compile("^(odd|even)$")
  rows = soup.find_all('tr', class_ = pattern)
  parseGameRows(rows, homeTeam, awayTeam, gameDate, homeScore, awayScore)



# Given all the rows, parse each of them and create a shot object
def parseGameRows(rows, homeTeam, awayTeam, gameDate, homeScore, awayScore):
  quarter = 1
  homeWon = homeScore > awayScore

  for play in rows:
    
    # Check if the play is an official play - timeout, start of quarter, end etc.
    # If play signifies the end of the quarter, increment quarter
    if len(play) == 2:
      officialPlay = play.contents[1].text
      splitPlay = officialPlay.split()
      try:
        if splitPlay[0] == "End":
          quarter += 1
      except:
        print 'error is ' + str(officialPlay)

    # Check if play is an official play for games after 2006-2007

    else:
      time = play.contents[0].text
      score = play.contents[2].text
      splitScore = score.split('-')
      scoreDiff = int(splitScore[1]) - int(splitScore[0])
      # Check if its a home team play or away
      # Some arbitrary length string - html contains some random characters - non empty
      if len(play.contents[1].text) < 10:
        home = True
        parsePlay(play.contents[3].text, home, score, quarter, time, scoreDiff, homeTeam, awayTeam, gameDate, homeWon)

      else:
        awayWon = not homeWon
        home = False
        scoreDiff = -scoreDiff
        parsePlay(play.contents[1].text, home, score, quarter, time, scoreDiff, awayTeam, homeTeam, gameDate, awayWon)




# Given a non official play, parse it to extract shot information, if it is a shot
def parsePlay(play, home, score, quarter, time, scoreDiff, team, opposition, gameDate, gameWon):
  global playerShotDict
  shotPattern = re.compile('(.*)(made|makes|missed|misses)(.*)')
  match = re.match(shotPattern, play) 
  if match:
    name = match.group(1).rstrip()
    if name not in playerShotDict:
      playerShotDict[name] = []

    if match.group(2) == 'made' or match.group(2) == 'makes':
      made = True
    else:
      made = False
    try:
      shot = createShot(match.group(3).lstrip(), home, score, made, name, quarter, time, scoreDiff, team, opposition, gameDate, gameWon)
      playerShotDict[name].append(shot)
    except:
      return


# Check for different types of shots. Create Shot object

# 2005-2006 Format:
# Jumper, Free Throw, Layup, Tip Shot, Shot, Running Jumper, Three Point Jumper, hook shot
# Formats:
# Jumper: made/missed (x ft) (running) (three point) jumper.
# Free Throw: made/missed (Technical) Free Throw (x of x).
# Layup: made/missed (driving) layup.
# Shot: made/missed (x ft) (hook|tip|two point) shot

# Format for play by play changed after 2006 season:
# Jumper: makes/misses (x-foot) (three point) jumper
# Free Throw: makes/misses (technical) free throw (x of x)
# Shot: makes/misses (x-foot) (tip|hook|two point) shot 
# Layup: makes/misses (driving) layup
# Dunk: makes/misses (slam|driving) dunk


# If Distance is not specified in play by play:
# Free Throw - 15
# Jumper (Two Point) - 0 (Disregard - no distance assumption) 
# Jumper (Three Point) - 23
# Tip Shot - 1
# Shot (hook|two point) - 1 
# Layup - 0
# Dunk - 0

def createShot(shotString, home, score, made, player, quarter, time, scoreDiff, team, opposition, gameDate, gameWon):
  overtime = quarter > 4
  shotString = shotString.lower()
  defaultDistances = {'free throw': 15, 'layup': 0, 'dunk': 0, 'three point jumper': 23, 'two point jumper': 1, 'hook shot': 1, 'tip shot': 0, 'two point shot': 1}
  timeInMinutes = adjustTime(time, quarter)
  scoreDiff -= 2
  
  if "free throw" in shotString:
    scoreDiff += 1
    shotType = "free throw"
    distance = defaultDistances[shotType]

  elif "layup" in shotString:
    shotType = "layup"
    distance = defaultDistances[shotType]

  elif "dunk" in shotString:
    shotType = "dunk"
    distance = defaultDistances[shotType]

  else:
    # Check if the distance was given
    _hasDistance = False
    distancePattern = re.compile('(\d+)(.*)')
    distanceMatch = re.match(distancePattern, shotString)
    if distanceMatch:
      distance = int(distanceMatch.group(1))
      _hasDistance = True

    if "jumper" in shotString:
      if "three point" in shotString:
        shotType = "three point jumper"
        scoreDiff -= 1
        if not _hasDistance:
          distance = defaultDistances[shotType]
      else:
        shotType = "two point jumper"
        if not _hasDistance:
          distance = defaultDistances[shotType]
        
    # Shot
    elif "shot" in shotString:
      if "hook" in shotString:
        shotType = "hook shot"
        if not _hasDistance:
          distance = defaultDistances[shotType]

      elif "tip" in shotString:
        shotType = "tip shot"
        distance = defaultDistances[shotType]

      else:
        shotType = "two point shot"
        if not _hasDistance:
          distance = defaultDistances[shotType]

    elif "three pointer" in shotString:
      shotType = "three point jumper"
      scoreDiff -= 1
      if not _hasDistance:
        distance = defaultDistances[shotType]

    else:
      if _hasDistance:
        shotType = "unknown"
        if distance > 23:
          scoreDiff -= 1
      else:
        print "Should not be here with " + shotString
        raise Exception

  # print 'Shot happened at ' + str(timeInMinutes) + " with score diff of " + str(scoreDiff)
  # print "Creating a " + str(made) + " shot with details: distance = " + str(distance) + " type = " + shotType + " quarter = " + str(quarter)+ " by player = " + player + " and score is " + score
  shot = Shot(gameDate, timeInMinutes, team, opposition, quarter, score, scoreDiff, shotType, home, overtime, distance, player, made, gameWon)
  return shot


# Given a time string in the form 12:00, and the quarter, calculate the minutes elapsed
def adjustTime(time, quarter):
  # if quarter < 5:
  #   QUARTERLENGTH = 12.0
  # else:
  #   QUARTERLENGTH = 5.0

  QUARTERLENGTH = 12.0
  time = time.split(':')

  if quarter > 4:
    elapsedQuarters = 4.0 + ((quarter - 4) * 5.0/12.0)
  else:
    elapsedQuarters = quarter

  timeMinute = (elapsedQuarters * QUARTERLENGTH * 60.0 - (60.0 * float(time[0]) + float(time[1]))) / 60.0
  return timeMinute

def createCsv(player, shots):
  filename = 'TestPlayers/' + player + '.csv'
  with open(filename, 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(['date', 'gameTime', 'team', 'opp', 'quarter', 'score', 'scoreDiff', 'shotType', 'home', 'distance', 'made', 'gameWon'])
    for shot in shots:
      try:
        writer.writerow([shot.date, shot.time, shot.team, shot.opposition, shot.quarter, shot.score, shot.scoreDiff, shot.shotType, shot.homeGame, shot.distance, shot.made, shot.gameWon])
      except:
        pass



def main():
  gameids = []
  homeTeam = []
  awayTeam = []
  gameDate = []
  homeScore = []
  awayScore = []
  errorIndices = []
  with open('2014games.csv', 'rb') as csvfile:
    gameReader = csv.DictReader(csvfile, delimiter = ',')
    for row in gameReader:
      gameids.append(row['id'])
      homeTeam.append(row['home_team'])
      awayTeam.append(row['visit_team'])
      gameDate.append(row['date'])
      homeScore.append(row['home_team_score'])
      awayScore.append(row['visit_team_score'])

  for i in range(len(gameids)):
    print '>>>>>>>>>>>>>>>>>>>>> newGame ' + 'with id ' + str(gameids[i]) + ' <<<<<<<<<<<<<<<<<<<<<<<<<<<<'
    try:
      getShotsForPage(gameids[i], homeTeam[i], awayTeam[i], gameDate[i], homeScore[i], awayScore[i])
    except urllib2.HTTPError, e:
      if e.code == 503:
        errorIndices.append(i)
      else:
        raise

  print '>>>>>>>>>>>>>>>>>>>>>>>>>>> Finished Getting Games <<<<<<<<<<<<<<<<<<<<<<<<<<<<'
  while len(errorIndices) > 0:
    for index in errorIndices:
      print '>>>>>>>>>>>>>>>>>>>> Trying again for ' + str(gameids[index]) + ' <<<<<<<<<<<<<<<<<<<<<<<<<<<<<'
      try:
        getShotsForPage(gameids[i], homeTeam[i], awayTeam[i], gameDate[i], homeScore[i], awayScore[i])
        print 'Succesfull'
        errorIndices.remove(index)
      except urllib2.HTTPError, e:
        if e.code == 503:
          errorIndices.append(i)
        else:
          raise

  for player in playerShotDict:  
    createCsv(player, playerShotDict[player])
  
if __name__ == '__main__':
  main()



  

