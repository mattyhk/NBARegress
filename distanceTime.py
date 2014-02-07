import csv
import sys
import numpy
import math
from pylab import *
import plotShots

# Plot distance vs time
# Distance on y Axis - max value of 
def plotDistanceByTime(player):

  XINTERVALLENGTH = 5.0
  XMAX = 60.0
  YINTERVALLENGTH = 3.0
  YMAX = 30.0

  MARKERSIZE = 5000

  (xMids, yMids, buckets) = plotShots.makeBuckets(XINTERVALLENGTH, YINTERVALLENGTH, XMAX, YMAX)

  maxTotal = 0

  # Each bucket contains two elements
  # Number of made shots
  # Total number of shots
  for shot in player.made:
    if shot.time >= XMAX:
      xInt = len(buckets) - 1
    else:
      xInt = math.floor(shot.time / XINTERVALLENGTH)
    
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
    if shot.time >= XMAX:
      xInt = len(buckets) - 1
    else:
      xInt = math.floor(shot.time / XINTERVALLENGTH)
    
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
  lims = xlim()
  xlim(-5, lims[1])
  xlabel("Elapsed Game Time")
  ylabel("Distance From Basket")
  suptitle("Shot Distance vs Game Time for " + str(player.name))
  cb = colorbar()
  cb.set_label("FG %")
  cb.set_ticks([0, 1.00])
  show()