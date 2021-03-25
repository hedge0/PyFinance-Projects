#enter values here for criterion
winProbability = 0.65
winAmount = 1.2
lossAmount = 0.85

winLossRatio = winAmount / lossAmount
kelly = winProbability - ((1 - winProbability) / winLossRatio)
print("Win Probability: " + str(winProbability * 100) + "%")
print("Win / Loss Ratio: " + str(round(winLossRatio, 4)))
print("Optimal percent recommended by Kelly Criterion: " + str(round(kelly, 4) * 100) + "%")