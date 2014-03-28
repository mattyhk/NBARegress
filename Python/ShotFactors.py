# Creates a new CSV file for each player with suitable data (i.e. enough shots taken in a game)
# Transforms the text factors for each fourth quarter shot into numerical values
# Includes Game Factors, Historical Features, and Shot Features for each fourth quarter and beyond shot
# Game Factors: Home/Away, Situation Factor
# Historical Factors: FG% in first three quarters, Average Intershot Time of all shots taken in first three quarters
# Average Intershot Time of made shots, Number of made shots, Number of shots taken
# Shot Features: Distance

import csv
import sys
import os
import math
import plotShots

# ((homeScore - awayScore) + 0.5) / (0.5 * (homeScore + awayScore))
def situationFactor(homeScore, awayScore):
  home = float(homeScore)
  away = float(awayScore)
  top = math.fabs(home - away) + 0.5
  bottom = 0.5 * (home + away) + 0.1
  return math.log(bottom / top)


# Factors for each shot are:
# Home/Away = [1,-1]
# Situation Factor
# First 3 periods FG%
# Average shot taken interval (First three quarters) (If none taken, interval is 36)
# Average made shot interval (First three quarters) (If none made, interval is 36)
# Number of Shots
# Number of Shots made
# Distance of the shot
def createFactors(gameShots):
  factors = []
  homeAway = 1
  fgPercentage = 0.0
  takenInterval = 0
  madeInterval = 0
  numShots = 0.0
  numMade = 0.0
  previousShotMade = 0.0
  previousShotTaken = 0.0
  date = 'No shots taken in game'
  for shot in gameShots:
    date = shot.date
    # If the shot is a free throw, skip
    if shot.shotType == 'free throw':
      continue
    
    # If the shot is in a quarter after the third, create a row corresponding to the shot
    if shot.quarter > 3:

      if shot.homeGame == 'False':
        homeAway = 0
      score = shot.score.split('-')
      awayScore = float(score[0])
      homeScore = float(score[1])
      if shot.made:
        made = 1
        # Get the game situation before taking the shot
        if shot.shotType == 'three point jumper':
          if shot.homeGame:
            homeScore -= 3
          else:
            awayScore -= 3
        else:
          if shot.homeGame:
            homeScore -= 2
          else:
            awayScore -= 2   
      else:
        made = 0

      sitFac = situationFactor(homeScore, awayScore)

      if numShots == 0.0:
        takenInterval = 36.0
        madeInterval = 36.0
        fgPercentage = 0.0

      else:
        fgPercentage = float(numMade) / float(numShots)

      if numMade == 0.0:
        madeInterval = 36.0

      factors.append([shot.date, made, homeAway, sitFac, fgPercentage, takenInterval, madeInterval, numShots, numMade, shot.distance + 0.5])

      # The shot is in the first three periods
      # Update numShots, numMade, takenInterval, and madeInterval
      # Interval includes the time elapsed before taking/making the first shot
    else:
      if shot.made:
        currentTakenInterval = float(shot.time) - previousShotTaken
        currentMadeInterval = float(shot.time) - previousShotMade
        takenInterval = (takenInterval * numShots + currentTakenInterval) / (numShots + 1.0)
        madeInterval = (madeInterval * numMade + currentMadeInterval) / (numMade + 1.0)
        numShots += 1
        numMade += 1
        previousShotTaken = float(shot.time)
        previousShotMade = float(shot.time)

      else:
        currentTakenInterval = float(shot.time) - previousShotTaken
        takenInterval = (takenInterval * numShots + currentTakenInterval) / (numShots + 1.0)
        numShots += 1
        previousShotTaken = float(shot.time)

  return factors

# Create a 2D array of the factors for each fourth quarter shot
# Each element in the array is another array describing each shot
def readPlayerFile(f):
  name = f.name.split('/')
  name = name[-1]
  name = name.split('.csv')
  name = name[0]

  player = plotShots.Player(name)
  reader = csv.reader(f, delimiter = ',')

  gameShots = []
  date = ''
  shotFactors = []

  firstLine = True
  for row in reader:
    if firstLine:
      firstLine = False
      continue
    (made, shot) = plotShots.readRow(row, player)

    # Check if it is the same game
    # If it is, add shot
    # If not, calculate factors for all fourth quarter shots
    if shot.date == date:
      gameShots.append(shot)
      
    else:
      date = shot.date
      gameFactors = createFactors(gameShots)
      if len(gameFactors) > 0:
        shotFactors += gameFactors
      gameShots = []
      gameShots.append(shot)

  gameFactors = createFactors(gameShots)
  if len(gameFactors) > 0:
    shotFactors += gameFactors

  return (name, shotFactors)

# Create a new csv file 
# Each row is a shot taken in the fourth quarter
def writePlayerFile(player, factors):
  headers = ['date', 'made', 'location', 'situation', 'fgPercentage', 'takenInterval', 'madeInterval', 'numShots', 'numMade', 'distance']

  filename = 'Factors2/' + player + ' Factors.csv'
  with open(filename, 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter = ',')
    writer.writerow(headers)
    for factor in factors:
      try:
        writer.writerow(factor)
      except:
        pass

def main():
  path = "/Users/Matthew/Documents/MIT/UAP - Basketball/Players/"
  for filename in os.listdir(path):
    if filename == '.DS_Store':
      continue
    with open(path + filename, 'rb') as f:
      (name, shotFactors) = readPlayerFile(f)
      writePlayerFile(name, shotFactors)

  # with open(sys.argv[1], 'rb') as f:
  #   (name, shotFactors) = readPlayerFile(f)
  #   writePlayerFile(name, shotFactors)

if __name__ == '__main__':
  main()  






