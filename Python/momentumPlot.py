import csv
import sys
import math
from pylab import *
import plotShots

# Reads a player csv file
# For each game, calculates the fg% of first three quarters, and fg% of remaining
# Plots the two against one another 
def readPlayerFile(f):
  name = f.name.split('/')
  name = name[-1]
  name = name.split('.csv')
  name = name[0]

  player = plotShots.Player(name)

  reader = csv.reader(f, delimiter = ',')

  beginFG = []
  endFG = []

  gameShots = []
  date = ''

  firstLine = True

  for row in reader:
    if firstLine:
      firstLine = False
      continue
    made, shot = plotShots.readRow(row, player)

    if shot.date == date:
      gameShots.append(shot)

    else:
      date = shot.date
      if len(gameShots) > 10:
        (begin, end) = calcFG(gameShots)
        beginFG.append(begin)
        endFG.append(end)
      gameShots = []
      gameShots.append(shot)

  if len(gameShots) > 10:
    (begin, end) = calcFG(gameShots)
    beginFG.append(begin)
    endFG.append(end)

  return beginFG, endFG, name

# Calculates the FG% for a given game
def calcFG(shots):

  beginNumTaken = 0
  beginNumMade = 0
  endNumTaken = 0
  endNumMade = 0

  for shot in shots:
    if shot.quarter < 4:
      beginNumTaken += 1
      if shot.made:
        beginNumMade += 1
    else:
      endNumTaken += 1
      if shot.made:
        endNumMade += 1

  if beginNumTaken == 0:
    beginFG = 0
  else:
    beginFG = float(beginNumMade)/float(beginNumTaken)

  if endNumMade == 0:
    endFG = 0
  else:
    endFG = float(endNumMade)/float(endNumTaken)

  return beginFG, endFG

# Plots the fg% of individual games
def plotMomentum(beginFG, endFG, name):
  figure()
  sct = scatter(beginFG, endFG)
  xlabel("FG% of First Three Quarters", fontsize = 35)
  ylabel("FG% of Fourth Quarter and Overtime", fontsize = 35)
  suptitle("Momentum Plot for " + name, fontsize = 45)
  show()

def main():
  with open(sys.argv[1], 'rb') as f:
    beginFG, endFG, name = readPlayerFile(f)
    plotMomentum(beginFG, endFG, name)

if __name__ == '__main__':
  main()

