import csv
import sys
import numpy
import math
from pylab import *
import plotShots

# Plot distance vs game situation
def situation(homeScore, awayScore):
  home = float(homeScore)
  away = float(awayScore)
  top = math.fabs(home - away) + 0.5
  bottom = 0.5 * (home + away) + 0.1
  return math.log(bottom / top)

def plotDistanceBySituation(player):
  XINTERVALLENGTH = 0.5
  XMIN = -2.0
  XMAX = 5.5
  YINTERVALLENGTH = 3.0
  YMAX = 30.0

  MARKERSIZE = 4000

  (xMids, yMids, buckets) = plotShots.makeBuckets(XINTERVALLENGTH, YINTERVALLENGTH, XMAX, YMAX, XMIN)

  maxTotal = 0

  for shot in player.made:
    score = shot.score.split('-')
    awayScore = float(score[0])
    homeScore = float(score[1])
    sit = situation(homeScore, awayScore)

    for i in range(len(xMids)):
      if sit < (XMIN + (i + 1) * XINTERVALLENGTH):
        xInt = i
        break

    if shot.distance >= YMAX:
      yInt = len(buckets[0]) - 1
    else:
      yInt = math.floor(shot.distance / YINTERVALLENGTH)

    xInt = int(xInt)
    yInt = int(yInt)

    buckets[xInt][yInt][0] += 1
    buckets[xInt][yInt][1] += 1

    if buckets[xInt][yInt][1] > maxTotal:
      maxTotal = buckets[xInt][yInt][1]

  for shot in player.missed:
    score = shot.score.split('-')
    awayScore = float(score[0])
    homeScore = float(score[1])
    sit = situation(homeScore, awayScore)

    for i in range(len(xMids)):
      if sit < (XMIN + (i + 1) * XINTERVALLENGTH):
        xInt = i
        break

    if shot.distance >= YMAX:
      yInt = len(buckets[0]) - 1
    else:
      yInt = math.floor(shot.distance / YINTERVALLENGTH)

    xInt = int(xInt)
    yInt = int(yInt)
    buckets[xInt][yInt][1] += 1
    if buckets[xInt][yInt][1] > maxTotal:
      maxTotal = buckets[xInt][yInt][1]

  percentages = []
  shotTotals = []

  # Find Field Goal Percentage for Each Bucket
  # First Element of the bucket = FG%
  # Add the FG% to the percentages list
  # Add normalised shot total to the shotTotals list
  for xInt in buckets:
    for bucket in xInt:
      if bucket[1] != 0:
        bucket[0] = float(bucket[0]) / bucket[1]


      # normTotal = (float(bucket[1]) / maxTotal) * MARKERSIZE
      normTotal = (float(bucket[1]) / maxTotal) ** 2 * MARKERSIZE
      percentages.append(bucket[0])
      shotTotals.append(normTotal)

  # The actual points plotted are the centers of each bucket
  # yMid for every xMid
  xVals = []
  yVals = []
  for x in xMids:
    xValues = [x] * len(yMids)
    xVals.extend(xValues)
    yVals.extend(yMids)

  # Get a colourmap for the FG percentages
  # Percentages are reflected via the gradient of the marker
  # The darker it is, the higher the percentage
  colourMap = cm.jet

  figure()
  sct = scatter(xVals, yVals, s=shotTotals, c=percentages, cmap=colourMap)
  sct.set_alpha(0.75)
  xlabel("Situation Factor")
  lims = xlim()
  xlim(XMIN - 0.5, XMAX + 0.5)
  ylabel("Distance From Basket")
  suptitle("Shot Distance vs Situation Factor for " + str(player.name))
  cb = colorbar(sct)
  cb.set_label("FG %", labelpad = 5)
  cb.set_ticks([0, 1])
  cb.set_ticklabels(['0', '1'])
  show()