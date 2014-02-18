import csv
import sys
import numpy
import math
from pylab import *
from scipy import stats
import plotShots
import os

# Calculate the FG % given number of shots taken and made
def calcFG(taken, made):
  return (float(made) / float(taken))

# Go through a player's shot file, calculating per game field goal percentages
# Calculates the FG % for the first three quarters, and then the FG % for the remaining fourth (and overtime if needed)
# Any games in which the player did not attempt any shots in either the first three quarters or last
# are disregarded.
# The Aim is to run a linear regression on the different FG % and see if there is a correlation
# Creates a training set by only adding every other game to a players shot set
def calcTrainingSets(f):
  name = f.name.split('/')
  name = name[-1]
  name = name.split('.')
  name = name[0]  

  player = plotShots.Player(name)
  reader = csv.reader(f, delimiter = ',')
  firstLine = True
  
  date = ''
  xTraining = []
  yTraining = []
  xData = []
  yData = []
  beginTaken = 0
  beginMade = 0
  endTaken = 0
  endMade = 0

  newGame = False

  counter = 0

  for row in reader:
    # skip the first line
    if firstLine:
      firstLine = False
      continue

    (made, shot) = plotShots.readRow(row, player)
    if shot.shotType == 'free throw':
      continue
    made = bool(made)

    # Same Game
    if shot.date == date:
      if made:
        if shot.quarter <= 3:
          beginTaken += 1
          beginMade += 1
        else:
          endTaken += 1
          endMade += 1
      else:
        if shot.quarter <= 3:
          beginTaken += 1
        else:
          endTaken += 1

    # New Game
    # Caclculate percentages of previous game
    # Disregard games with no shots taken in either the first 3 quarters or last quarter
    # Restart shot counters, and update date. Account for new shot
    else:     
      if beginTaken != 0 and endTaken != 0:
        if counter % 2 == 0:
          xTraining.append(calcFG(beginTaken, beginMade))
          yTraining.append(calcFG(endTaken, endMade))
        else:
          xData.append(calcFG(beginTaken, beginMade))
          yData.append(calcFG(endTaken, endMade))
        counter += 1
      beginTaken = 0
      endTaken = 0
      beginMade = 0
      endMade = 0
      date = shot.date
      if made:
        if shot.quarter <= 3:
          beginTaken += 1
          beginMade += 1
        else:
          endTaken += 1
          endMade += 1
      else:
        if shot.quarter <= 3:
          beginTaken += 1
        else:
          endTaken += 1

  # figure()
  # sct = scatter(xTraining, yTraining)
  # suptitle(name + ' Field Goal Percentages')
  # xlabel('First Three Quarters')
  # ylabel('Fourth Quarter and Overtime')
  # grid('on')
  # show()

  return (name, xTraining, yTraining)

# Go through every player and display their p value
def main():
  players = {}
  path = "/Users/Matthew/Documents/MIT/UAP - Basketball/Players/" 
  for filename in os.listdir(path):
    if filename == '.DS_Store':
      continue
    with open(path + filename, 'rb') as f:
        (name, trainBeginFG, trainEndFG) = calcTrainingSets(f)
    if len(trainBeginFG) == 0:
      continue
    (slope, intercept, rValue, pValue, stdErr) = stats.linregress(trainBeginFG, trainEndFG)
    players[name] = [pValue, slope, intercept, rValue, stdErr, len(trainBeginFG)]

  filename = 'linRegressPValues.csv'
  with open(filename, 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter = ',')
    writer.writerow(['player', 'pValue', 'slope', 'intercept', 'rValue', 'stdErr', 'numDataPoints'])
    for player in players:
      try:
        # print 'writing ' + str(player) +' with values ' + str(players[player][0]) + ' ' +str(players[player][1])
        writer.writerow([player] + players[player])
      except:
        pass

  # with open(sys.argv[1], 'rb') as f:
  #   (name, trainBeginFG, trainEndFG) = calcTrainingSets(f)

  # slope, intercept, rValue, pValue, stdErr = stats.linregress(trainBeginFG, trainEndFG)

  # print name
  # print pValue
  

if __name__ == '__main__':
  main()  
