import sys
import random
import numpy as np

#check that string can be converted to float
def checkFloat(val):
	try:
		float(val)
	except ValueError:
		sys.exit("Not a Float")

	return float(val)

#check that string can be converted to int
def checkInt(val):
	try:
		int(val)
	except ValueError:
		sys.exit("Not an Int")

	return int(val)

class Kelly:
	def __init__(self, probability, risk, reward, runs):

		probability = checkFloat(probability)
		risk = checkFloat(risk)
		reward = checkFloat(reward)
		runs = checkInt(runs)

		ratio = reward / risk
		kelly = probability - ((1 - probability) / ratio)
		if(kelly <= 0):
			sys.exit("Suggested betting size is less than or equal to 0 and should not be taken")

		self.probability = probability
		self.risk = risk
		self.reward = reward
		self.ratio = ratio
		self.kelly = kelly
		self.runs = runs
		self.kellySim = self.monteCarlo(True)
		self.fullSim = self.monteCarlo(False)
		self.kellyMean = np.mean(self.kellySim)
		self.fullMean = np.mean(self.fullSim)
		self.kellySigma = np.std(self.kellySim)
		self.fullSigma = np.std(self.fullSim)
		self.kellyWalks = self.getProfitableWalks(self.kellySim)
		self.fullWalks = self.getProfitableWalks(self.fullSim)
	
	#run simulation equal to number of random walks
	def monteCarlo(self, simType):
		walks = 10000
		results = []
		for i in range(walks):
			randomWalk = []
			randomWalk.append(1)
			for i in range(1, self.runs + 1):
				prev = randomWalk[i-1]
				if simType:
					randomWalk.append(self.kellyVal(prev))
				else:
					randomWalk.append(self.fullVal(prev))
			results.append(randomWalk[-1])
		return results

	#compute new value using kelly
	def kellyVal(self, prev):
		if random.random() < self.probability:
			kellyVal = (self.kelly * prev) * (1 + self.reward)
			otherVal = (1 - self.kelly) * prev
			totalVal = kellyVal + otherVal
		else:
			kellyVal = (self.kelly * prev) * (1 - self.risk)
			otherVal = (1 - self.kelly) * prev
			totalVal = kellyVal + otherVal
		return totalVal

	#compute new value using full
	def fullVal(self, prev):
		if random.random() < self.probability:
			totalVal = prev * (1 + self.reward)
		else:
			totalVal = prev * (1 - self.risk)
		return totalVal

	#get percent of random walks that were profitable
	def getProfitableWalks(self, results):
		count = 0
		for value in results:
			if value > 1:
				count += 1
		prof = (count / len(results))
		return prof

	#get probability
	def getProbability(self):
		return self.probability

	#get risk
	def getRisk(self):
		return self.risk

	#get reward
	def getReward(self):
		return self.reward

	#get ratio
	def getRatio(self):
		return self.ratio
	
	#get kelly
	def getKelly(self):
		return self.kelly

	#get number of consecutive runs
	def getRuns(self):
		return self.runs

	#get kellyMean
	def getKellyMean(self):
		return self.kellyMean

	#get fullMean
	def getFullMean(self):
		return self.fullMean

	#get kellySigma
	def getKellySigma(self):
		return self.kellySigma	

	#get fullSigma
	def getFullSigma(self):
		return self.fullSigma

	#get kellyWalks
	def getKellyWalks(self):
		return self.kellyWalks	

	#get fullWalks
	def getFullWalks(self):
		return self.fullWalks