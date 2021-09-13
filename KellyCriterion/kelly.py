import sys
import random
import numpy as np

def checkFloat(val):
	try:
		float(val)
	except ValueError:
		sys.exit("Not a Float")

def checkInt(val):
	try:
		int(val)
	except ValueError:
		sys.exit("Not an Int")

def getProbability():
	probability = input("Enter the Expected Probability of Winning: ")
	checkFloat(probability)
	probability = float(probability)
	return probability

def getRatio():
	reward = input("Enter the Potential Reward: ")
	checkFloat(reward)
	reward = float(reward)
	risk = input("Enter the Potential Risk: ")
	checkFloat(risk)
	risk = float(risk)
	ratio = reward / risk
	return reward, risk, ratio

def getRuns():
	runs = input("Enter the Number of Consecutive Bets: ")
	checkInt(runs)
	runs = int(runs)
	return runs

def getKelly(probability, ratio):
	kelly = probability - ((1 - probability) / ratio)
	if(kelly <= 0):
		sys.exit("Suggested betting size is less than or equal to 0 and should not be taken")
	return kelly

def getStats(results):
	mean = np.mean(results) 
	sigma = np.std(results)
	return mean, sigma

def kellyVal(probability, reward, risk, kelly, prev):
	if random.random() < probability:
		kellyVal = (kelly * prev) * (1 + reward)
		otherVal = (1 - kelly) * prev
		totalVal = kellyVal + otherVal
	else:
		kellyVal = (kelly * prev) * (1 - risk)
		otherVal = (1 - kelly) * prev
		totalVal = kellyVal + otherVal
	return totalVal

def fullVal(probability, reward, risk, prev):
	if random.random() < probability:
		totalVal = prev * (1 + reward)
	else:
		totalVal = prev * (1 - risk)
	return totalVal

def monteCarlo(probability, reward, risk, walks, runs, kelly = 0):
	results = []
	for i in range(walks):
		randomWalk = []
		randomWalk.append(1)
		for i in range(1, runs + 1):
			prev = randomWalk[i-1]
			if kelly > 0:
				randomWalk.append(kellyVal(probability, reward, risk, kelly, prev))
			else:
				randomWalk.append(fullVal(probability, reward, risk, prev))
		results.append(randomWalk[-1])
	return results

def getProfitableWalks(results):
	count = 0
	for value in results:
		if value > 1:
			count += 1
	prof = (count / len(results))
	return prof

def runSim(probability, reward, risk, walks, runs, kelly = 0):
	if kelly > 0:
		bet = "Kelly"
	else:
		bet = "All-In"

	results = monteCarlo(probability, reward, risk, walks, runs, kelly)
	prof = getProfitableWalks(results)
	mean, sigma = getStats(results)

	print("\n" + bet + " μ: " + str(round(mean, 4)))
	print(bet + " σ: " + str(round(sigma, 4)))
	print(str(round(prof * 100, 4)) + "%" + " Profitable Walks")

probability = getProbability()
reward, risk, ratio = getRatio()
runs = getRuns()
walks = 10000
kelly = getKelly(probability, ratio)

print("\nWin Probability: " + str(probability * 100) + "%")
print("Risk Reward Ratio: " + str(round(ratio, 4)))
print("Optimal Kelly Size: " + str(round(kelly, 4) * 100) + "%")

runSim(probability, reward, risk, walks, runs, kelly)
runSim(probability, reward, risk, walks, runs)