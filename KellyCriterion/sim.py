from kelly import Kelly

probability = input("Enter the Expected Probability of Winning: ")
risk = input("Enter the Potential Risk: ")
reward = input("Enter the Potential Reward: ")
runs = input("Enter the Number of Consecutive Bets: ")

sim = Kelly(probability, risk, reward, runs)

print(f"\nWin Probability: {sim.getProbability() * 100}%")
print(f"Risk Reward Ratio: {round(sim.getRatio(), 4)}")
print(f"Optimal Kelly Size: {round(sim.getKelly(), 4) * 100}%")

print(f"\nKelly μ: {round(sim.getKellyMean(), 4)}")
print(f"Kelly σ: {round(sim.getKellySigma(), 4)}")
print(f"{round(sim.getKellyWalks() * 100, 4)}% Profitable Walks")

print(f"\nFull μ: {round(sim.getFullMean(), 4)}")
print(f"Full σ: {round(sim.getFullSigma(), 4)}")
print(f"{round(sim.getFullWalks() * 100, 4)}% Profitable Walks")