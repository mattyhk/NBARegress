import csv
import sys
import numpy
import math
from pylab import *
from scipy import stats
import plotShots

# Calculate the FG % given number of shots taken and made
def calcFG(taken, made):
  return (float(made) / float(taken))

# Go through a player's shot file, calculating per game field goal percentages
# Calculates the FG % for the first three quarters, and then the FG % for the remaining fourth (and overtime if needed)
# Any games in which the player did not attempt any shots in either the first three quarters or last
# are disregarded.
def main():
  with open(sys.argv[1], 'rb') as f:
    name = f.name.split('/')
    name = name[1]
    name = name.split('.')
    name = name[0]  

    player = plotShots.Player(name)
    reader = csv.reader(f, delimiter = ',')
    firstLine = True
    
    date = ''
    trainBeginFG = []
    trainEndFG = []
    dataBeginFG = []
    dataEndFG = []
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

      else:
        # Disregard games with no shots taken in either the first 3 quarters or last quarter
        if beginTaken != 0 and endTaken != 0:
          if counter % 2 == 0:
            trainBeginFG.append(calcFG(beginTaken, beginMade))
            trainEndFG.append(calcFG(endTaken, endMade))
          else:
            dataBeginFG.append(calcFG(beginTaken, beginMade))
            dataEndFG.append(calcFG(endTaken, endMade))
          counter += 1
          beginTaken = 0
          endTaken = 0
          beginMade = 0
          endMade = 0
          date = shot.date
        else:
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
  # sct = scatter(trainBeginFG, trainEndFG)
  # suptitle(name + ' Field Goal Percentages')
  # xlabel('First Three Quarters')
  # ylabel('Fourth Quarter and Overtime')
  # grid('on')
  # show()

  slope, intercept, rValue, pValue, stdErr = stats.linregress(trainBeginFG, trainEndFG)

  print pValue


if __name__ == '__main__':
  main()  

