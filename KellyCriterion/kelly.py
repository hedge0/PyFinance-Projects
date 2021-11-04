import sys
import random
import numpy as np

class Kelly:
	def __init__(self, probability, risk, reward, runs):

		probability = self._check_float(probability)
		risk = self._check_float(risk)
		reward = self._check_float(reward)
		runs = self._check_int(runs)

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
		self.kellySim = self._monte_carlo(True)
		self.fullSim = self._monte_carlo(False)
		self.kellyMean = np.mean(self.kellySim)
		self.fullMean = np.mean(self.fullSim)
		self.kellySigma = np.std(self.kellySim)
		self.fullSigma = np.std(self.fullSim)
		self.kellyWalks = self._get_profitable_walks(self.kellySim)
		self.fullWalks = self._get_profitable_walks(self.fullSim)
	
	#check that string can be converted to float
	def _check_float(self, val):
		try:
			float(val)
		except ValueError:
			sys.exit("Not a Float")

		return float(val)

	#check that string can be converted to int
	def _check_int(self, val):
		try:
			int(val)
		except ValueError:
			sys.exit("Not an Int")

		return int(val)

	#run simulation equal to number of random walks
	def _monte_carlo(self, simType):
		walks = 10000
		results = []
		for i in range(walks):
			randomWalk = []
			randomWalk.append(1)
			for i in range(1, self.runs + 1):
				prev = randomWalk[i-1]
				if simType:
					randomWalk.append(self._kelly_val(prev))
				else:
					randomWalk.append(self._full_val(prev))
			results.append(randomWalk[-1])
		return results

	#compute new value using kelly
	def _kelly_val(self, prev):
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
	def _full_val(self, prev):
		if random.random() < self.probability:
			totalVal = prev * (1 + self.reward)
		else:
			totalVal = prev * (1 - self.risk)
		return totalVal

	#get percent of random walks that were profitable
	def _get_profitable_walks(self, results):
		count = 0
		for value in results:
			if value > 1:
				count += 1
		prof = (count / len(results))
		return prof

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