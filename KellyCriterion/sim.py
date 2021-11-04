from kelly import Kelly

probability = input("Enter the Expected Probability of Winning: ")
risk = input("Enter the Potential Risk: ")
reward = input("Enter the Potential Reward: ")
runs = input("Enter the Number of Consecutive Bets: ")

sim = Kelly(probability, risk, reward, runs)

print(f"\nWin Probability: {sim.get_probability() * 100}%")
print(f"Risk Reward Ratio: {round(sim.get_ratio(), 4)}")
print(f"Optimal Kelly Size: {round(sim.get_kelly(), 4) * 100}%")

print(f"\nKelly μ: {round(sim.get_kelly_mean(), 4)}")
print(f"Kelly σ: {round(sim.get_kelly_sigma(), 4)}")
print(f"{round(sim.get_kelly_walks() * 100, 4)}% Profitable Walks")

print(f"\nFull μ: {round(sim.get_full_mean(), 4)}")
print(f"Full σ: {round(sim.get_full_sigma(), 4)}")
print(f"{round(sim.get_full_walks() * 100, 4)}% Profitable Walks")