from kelly import Kelly


def main():
    probability = input("Enter the Expected Probability of Winning: ")
    risk = input("Enter the Potential Risk: ")
    reward = input("Enter the Potential Reward: ")
    runs = input("Enter the Number of Consecutive Bets: ")

    sim = Kelly(probability, risk, reward, runs)

    print(f"\nWin Probability: {sim.get_probability() * 100}%")
    print(f"Risk Reward Ratio: {round(sim.get_ratio(), 4)}")
    print(f"Optimal Kelly Size: {round(sim.get_kelly(), 4) * 100}%")

    sim.run_monte_carlo(sim.get_kelly(), 10000)

    print(f"\nμ: {round(sim.get_mean(), 4)}")
    print(f"σ: {round(sim.get_sigma(), 4)}")
    print(f"{round(sim.get_walks() * 100, 4)}% Profitable Walks")


if __name__ == '__main__':
    main()