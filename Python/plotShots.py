# Plots heat maps for different predictor variables against one another for individual players

import csv
import sys
import numpy
import math
from pylab import *
import distanceTime
import distancePointdiff
import distanceSituation

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


def readRow(row, player):
  
  try:
    (date, gameTime, team, opp, quarter, score, diff, shotType, home, distance, made, gameWon) = row
  except:
    print row

  overtime = False

  # FIX FOR BUG INTRODUCED BY getShots.py
  # gameTime was not being set correctly
  if int(quarter) > 4:
    overtime = True
    orgTime = (4.0 + ((float(quarter) - 4.0) * 5.0/12.0)) * 5.0 * 60.0 - 60.0 * float(gameTime)
    gameTime = ((4.0 + ((float(quarter) - 4.0) * 5.0/12.0)) * 12.0 * 60.0 - orgTime) / 60.0
  
  if made == 'True':
    shotMade = True
  else:
    shotMade = False

  shot = Shot(date, float(gameTime), team, opp, int(quarter), score, float(diff), shotType, home, overtime, float(distance), player.name, shotMade, gameWon)

  return (shotMade, shot) 

# Split graph up into grid to bucket shots
# xAxis split into intervals of length xInterval in the range xMin to xMax
# yAxis split into intervals of length yInterval in the range yMin to yMax
# Create a list of length numXIntervals of empty lists
# Create a list of the mid values for each xInterval and for each yInterval
def makeBuckets(xIntervalLength, yIntervalLength, xMax, yMax, xMin = 0, yMin = 0):
  buckets = []
  xMids = []
  yMids = []

  xRange = (xMax - xMin)
  numXIntervals = math.ceil(float(xRange) / xIntervalLength)

  yRange = int(yMax - yMin)
  numYIntervals = math.ceil(float(yRange) / yIntervalLength)
  
  buckets = [[[0, 0] for y in range(int(numYIntervals))] for x in range(int(numXIntervals))]
  for i in range(int(numXIntervals)):
    xMids.append(((i * xIntervalLength) + (xIntervalLength / 2.0)) + xMin)
  for i in range(int(numYIntervals)):
    yMids.append((i * yIntervalLength) + (yIntervalLength / 2.0) + yMin)

  return (xMids, yMids, buckets)


def main():
  with open(sys.argv[1], 'rb') as f:
    # Get the player name
    name = f.name.split('/')
    name = name[-1]
    name = name.split('.')
    name = name[0]

    player = Player(name)  
    reader = csv.reader(f, delimiter = ',')
    firstLine = True
    for row in reader:
      if firstLine:
        firstLine = False
        continue
      (made, shot) = readRow(row, player)
      if shot.shotType == 'free throw':
        continue
      made = bool(made)
      if made:
        player.addMadeShot(shot)
      else:
        player.addMissedShot(shot)

  distanceSituation.plotDistanceBySituation(player)
  distancePointdiff.plotDistanceByPointDiff(player)
  distanceTime.plotDistanceByTime(player)


if __name__ == '__main__':
  main()


  





