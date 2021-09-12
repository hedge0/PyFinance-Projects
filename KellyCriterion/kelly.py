import random
import numpy as np

#enter values here for criterion
winProbability = 0.85
#if 25 cents won per dollar bet, enter 0.25
winAmount = 0.1
#if 25 cents lost per dollar bet, enter 0.25
lossAmount = 0.5
numRuns = 100

riskRewardRatio = winAmount / lossAmount
kelly = winProbability - ((1 - winProbability) / riskRewardRatio)
print("Win Probability: " + str(winProbability * 100) + "%")
print("Risk / Reward Ratio: " + str(round(riskRewardRatio, 4)))
print("Optimal percent recommended by Kelly Criterion: " + str(round(kelly, 4) * 100) + "%")

if(kelly <= 0):
	print("Kelly Criterion has suggested a betting size less than or equal to 0, and thus the bet should not be taken")
	exit()

simRuns = 10000
startingAmount = 1
finalKelly = []
finalComp = []

print("\nMonte Carlo Simulation of " + str(simRuns) + " Runs:")

for i in range(simRuns):
	simAmount = []
	simAmount.append(startingAmount)

	for i in range(1, numRuns + 1):
		lastAmount = simAmount[i-1]

		if random.random() < winProbability:
			kellyVal = (kelly * lastAmount) * (1 + winAmount)
			otherVal = (1 - kelly) * lastAmount
			totalVal = kellyVal + otherVal
			simAmount.append(totalVal)
		else:
			kellyVal = (kelly * lastAmount) * (1 - lossAmount)
			otherVal = (1 - kelly) * lastAmount
			totalVal = kellyVal + otherVal
			simAmount.append(totalVal)
	finalKelly.append(simAmount[-1])

profitableKelly = 0

for value in finalKelly:
	if value > startingAmount:
		profitableKelly += 1

meanKelly = np.mean(finalKelly) 
sigmaKelly = np.std(finalKelly) 

print("\nThe mean price after " + str(numRuns) + " Kelly bets is: " + str(round(meanKelly, 4)))
print("Kelly betting has a standard deviation of: " + str(round(sigmaKelly, 4)))
print(str(round((profitableKelly / len(finalKelly)) * 100, 4)) + "%" + " of Kelly random walks were profitable")

for i in range(simRuns):
	compAmount = []
	compAmount.append(startingAmount)

	for i in range(1, numRuns + 1):
		lastAmount = compAmount[i-1]

		if random.random() < winProbability:
			totalVal = lastAmount * (1 + winAmount)
			compAmount.append(totalVal)
		else:
			totalVal = lastAmount * (1 - lossAmount)
			compAmount.append(totalVal)
	finalComp.append(compAmount[-1])

profitableComp = 0

for value in finalComp:
	if value > startingAmount:
		profitableComp += 1

meanComp = np.mean(finalComp) 
sigmaComp = np.std(finalComp) 

print("\nThe mean price after " + str(numRuns) + " All-In bets is: " + str(round(meanComp, 4)))
print("All-In betting has a standard deviation of: " + str(round(sigmaComp, 4)))
print(str(round((profitableComp / len(finalComp)) * 100, 4)) + "%" + " of All-In random walks were profitable")
