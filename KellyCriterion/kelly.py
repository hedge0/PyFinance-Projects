from sys import exit
from random import random
from numpy import mean, std
from collections import deque

class Kelly:

	def __init__(self, probability, risk, reward, runs):

		probability = self._check_float(probability)
		risk = self._check_float(risk)
		reward = self._check_float(reward)
		runs = self._check_int(runs)

		ratio = reward / risk
		kelly = probability - ((1 - probability) / ratio)
		
		if(kelly <= 0):
			exit("Suggested betting size is less than or equal to 0 and should not be taken")

		self.probability = probability
		self.risk = risk
		self.reward = reward
		self.ratio = ratio
		self.kelly = kelly
		self.runs = runs
		self.kellySim = self._monte_carlo(self.kelly)
		self.fullSim = self._monte_carlo(1)
		self.kellyMean = mean(self.kellySim)
		self.fullMean = mean(self.fullSim)
		self.kellySigma = std(self.kellySim)
		self.fullSigma = std(self.fullSim)
		self.kellyWalks = self._get_profitable_walks(self.kellySim)
		self.fullWalks = self._get_profitable_walks(self.fullSim)
	
	#check that string can be converted to float
	def _check_float(self, val):
		try:
			float(val)
		except ValueError:
			exit("Not a Float")

		return float(val)

	#check that string can be converted to int
	def _check_int(self, val):
		try:
			int(val)
		except ValueError:
			exit("Not an Int")

		return int(val)

	#run simulation equal to number of random walks
	def _monte_carlo(self, val):
		results = []
		for i in range(10000):
			randomWalk = deque()
			randomWalk.append(1)
			for i in range(1, self.runs + 1):
				randomWalk.append(self._total_val(randomWalk[i-1], val))
			results.append(randomWalk[-1])
		return results

	#compute new value for random walk
	def _total_val(self, prev, val):
		if random() < self.probability:
			totalVal = (1 + self.reward) * (val * prev) + (1 - val) * prev
		else:
			totalVal = (1 - self.risk) * (val * prev) + (1 - val) * prev
		return totalVal

	#get percent of random walks that were profitable
	def _get_profitable_walks(self, results):
		return len(list(filter(lambda x: x > 1, results))) / len(results)

	#get probability
	def get_probability(self):
		return self.probability

	#get risk
	def get_risk(self):
		return self.risk

	#get reward
	def get_reward(self):
		return self.reward

	#get ratio
	def get_ratio(self):
		return self.ratio
	
	#get kelly
	def get_kelly(self):
		return self.kelly

	#get number of consecutive runs
	def get_runs(self):
		return self.runs

	#get kellyMean
	def get_kelly_mean(self):
		return self.kellyMean

	#get fullMean
	def get_full_mean(self):
		return self.fullMean

	#get kellySigma
	def get_kelly_sigma(self):
		return self.kellySigma	

	#get fullSigma
	def get_full_sigma(self):
		return self.fullSigma

	#get kellyWalks
	def get_kelly_walks(self):
		return self.kellyWalks	

	#get fullWalks
	def get_full_walks(self):
		return self.fullWalks