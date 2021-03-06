import csv
import sys
import numpy
import math
from pylab import *
import plotShots

# Plot distance vs time
# Distance on y Axis - max value of 
def plotDistanceByPointDiff(player):

  XINTERVALLENGTH = 4.0
  XMIN = -22.0
  XMAX = 22.0
  YINTERVALLENGTH = 3.0
  YMAX = 30.0

  MARKERSIZE = 5000

  (xMids, yMids, buckets) = plotShots.makeBuckets(XINTERVALLENGTH, YINTERVALLENGTH, XMAX, YMAX, XMIN)

  maxTotal = 0

  # Each bucket contains two elements
  # Number of made shots
  # Total number of shots
  for shot in player.made:
    if shot.scoreDiff >= XMAX:
      xInt = len(buckets) - 1
    elif shot.scoreDiff <= XMIN:
      xInt = 0
    else:
      if shot.scoreDiff >= 0:
        xInt = math.ceil((float(len(buckets)) - 1.0) / 2.0) + math.floor((float(shot.scoreDiff) + (XMAX % XINTERVALLENGTH)) / float(XINTERVALLENGTH))
      else:
        xInt = math.floor((float(len(buckets)) - 1.0) / 2.0) + math.ceil((float(shot.scoreDiff) - (XMIN % XINTERVALLENGTH)) / float(XINTERVALLENGTH))
    
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
    if shot.scoreDiff >= XMAX:
      xInt = len(buckets) - 1
    elif shot.scoreDiff <= XMIN:
      xInt = 0
    else:
      if shot.scoreDiff >= 0:
        xInt = math.ceil((float(len(buckets)) - 1.0) / 2.0) + math.floor((float(shot.scoreDiff) + (XMAX % XINTERVALLENGTH)) / float(XINTERVALLENGTH))
      else:
        xInt = math.floor((float(len(buckets)) - 1.0) / 2.0) + math.ceil((float(shot.scoreDiff) - (XMIN % XINTERVALLENGTH)) / float(XINTERVALLENGTH))
    
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
  xlabel("Score Differential", fontsize=35)
  lims = xlim()
  xlim(XMIN - 5, XMAX + 5)
  ylabel("Distance From Basket", fontsize=35)
  suptitle("Shot Distance vs Score Differential for " + str(player.name), fontsize=45)
  cb = colorbar(sct)
  cb.set_label("FG %", labelpad = 5, fontsize=25)
  cb.set_ticks([0, 1])
  cb.set_ticklabels(['0', '1'])
  show()