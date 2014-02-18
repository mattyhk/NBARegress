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
  bottom = 0.5 * (home + away)

  return (top / bottom)

def plotDistanceBySituation(player):
  