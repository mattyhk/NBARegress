import csv
import sys
import numpy
from pylab import *

class Shot(object):
	# A shot has serveral fields: distance, time, type, made, point, point differential
	def __init__(self, num, date, time, team, opposition, quarter, scoreDiff, shotType, home, overtime, distance):
		self.id = num
		self.date = date
		self.time = time
		self.team = team
		self.homeGame = home
		self.opposition = opposition
		self.quarter = quarter
		self.scoreDiff = scoreDiff
		self.shotType = shotType
		self.overtime = overtime
		self.distance = distance


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

def readRow(row):
	try:
		#print row
		(num, date, team, opposition, quarter) = (row[0], row[1], row[2], row[4], row[5])
	except:
		print row
		raise
	quarter = quarter.replace('st','').replace('nd','').replace('rd','').replace('th','')
	overtime = False
	if quarter == 'OT':
		overtime = True
		quarter = 4.0 + 5.0/12.0
	elif quarter == '2OT':
		overtime = True
		quarter = 4.0 + 10.0/12.0
	else:
		quarter = float(quarter)
	if row[3] == '@':
		home = False
	else:
		home = True
	time = row[6].split(':')
	time = (quarter * 12.0 * 60.0 - (60.0 * float(time[0]) + float(time[1]))) / 60.0  
	scoreLine = row[7]
	splitScoreLine = scoreLine.split()
	if splitScoreLine[1] == 'down':
		scoreDiff = -1.0 * float(splitScoreLine[2])
	elif splitScoreLine[1] == 'up':
		scoreDiff = float(splitScoreLine[2])
	else:
		scoreDiff = 0
	typeLine = row[8]
	splitTypeLine = typeLine.split()
	if splitTypeLine[2] == 'misses':
		made = False
	else:
		made = True
	if splitTypeLine[3] == '2-pt':
		shotType = 2
	else:
		shotType = 3

	if splitTypeLine[6] == 'rim':
		distance = 0.5
	else:
		distance = float(splitTypeLine[6])
	shot = Shot(num, date, time, team, opposition, quarter, scoreDiff, shotType, home, overtime, distance)
	return(made, shot)

def plotTimeAgainstShotDistance(player):
	madeShots = player.made
	missedShots = player.missed
	
	madeDistances = []
	madeTimes = []
	missedDistances = []
	missedTimes = []
	for shots in player.made:
		madeDistances.append(shots.distance)
		madeTimes.append(shots.time)
	for shots in player.missed:
		missedDistances.append(shots.distance)
		missedTimes.append(shots.time)

	figure()
	suptitle('Shot Distance against Time')
	plot(madeTimes, madeDistances, 'bo', label = 'made shots')
	plot(missedTimes, missedDistances, 'rx', label = 'missed shots')
	legend()
	show()

def plotTimeAgainstPointDiff(player):
	madeShots = player.made
	missedShots = player.missed

	madeDiffs = []
	madeTimes = []
	missedDiffs = []
	missedTimes = []

	for shots in player.made:
		madeDiffs.append(shots.scoreDiff)
		madeTimes.append(shots.time)
	for shots in player.missed:
		missedDiffs.append(shots.scoreDiff)
		missedTimes.append(shots.time)

	figure()
	suptitle('Point Differential against Time')
	plot(madeTimes, madeDiffs, 'bo', label = 'made shots')
	plot(missedTimes, missedDiffs, 'rx', label = 'missed shots')
	legend()
	show()

def plotScoreDiffAgainstShootingPercentage(player):
	madeShots = player.made
	missedShots = player.missed

	scoreDiffs = []
	diffs = {}

	shotPercentage = []

	for shots in player.made:
		scoreDiff = shots.scoreDiff
		if scoreDiff not in diffs:
			scoreDiffs.append(scoreDiff)
			diffs[scoreDiff] = [0,0]
			diffs[scoreDiff][0] += 1
		else:
			diffs[scoreDiff][0] += 1

	for shots in player.missed:
		scoreDiff = shots.scoreDiff
		if scoreDiff not in diffs:
			scoreDiffs.append(scoreDiff)
			diffs[scoreDiff] = [0,0]
			diffs[scoreDiff][1] += 1
		else:
			diffs[scoreDiff][1] += 1

	for diff in scoreDiffs:
		numMade = diffs[diff][0]
		numMissed = diffs[diff][1]
		total = numMade + numMissed
		percentage = float(numMade) / float(total)
		shotPercentage.append(percentage)

	figure()
	suptitle('Shot Percentage against Score Differential')
	plot(scoreDiffs, shotPercentage, 'bo', label = 'shooting percentages')
	show()

def plotShotDistanceAgainstScoreDiff(player):
	madeShots = player.made
	missedShots = player.missed

	madeDiffs = []
	madeDistances = []
	missedDiffs = []
	missedDistances = []

	for shots in madeShots:
		madeDistances.append(shots.distance)
		madeDiffs.append(shots.scoreDiff)

	for shots in missedShots:
		missedDistances.append(shots.distance)
		missedDiffs.append(shots.scoreDiff)

	figure()
	suptitle('Shot Distances against Score Differentials')
	plot(madeDiffs, madeDistances, 'bo', label = 'made shots')
	plot(missedDiffs, missedDistances, 'rx', label = 'missed shots')
	show()

f = open(sys.argv[1], 'rb')
player = Player("M. Ellis")
try:
	reader = csv.reader(f)
	for row in reader:
		#print row
		if row[0] == "Rk":
			pass
		else:
			(made, shot) = readRow(row)
			if made:
				player.addMadeShot(shot)
			else:
				player.addMissedShot(shot)

	plotTimeAgainstShotDistance(player)
	plotTimeAgainstPointDiff(player)
	plotScoreDiffAgainstShootingPercentage(player)
	plotShotDistanceAgainstScoreDiff(player)

finally:
	f.close
			



