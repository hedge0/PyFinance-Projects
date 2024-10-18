# Kelly Criterion Bet Sizing Program

This program helps users calculate the optimal betting size based on the **Kelly Criterion** formula, which is commonly used to maximize long-term growth in scenarios involving repeated bets. The program uses user input for the probability of winning, the amount of money gained on a win, and the amount of money lost on a loss, and outputs the ideal bet size as a percentage of your available capital.

The Kelly Criterion is designed to find a balance between risk and reward, taking advantage of the **law of large numbers** to maximize profits over many trials. If the calculated optimal betting size is negative, it suggests that making the bet is a losing proposition in the long term.

## Features

- **Input**: 
  - Probability of winning (`p`)
  - Potential gain on a win (`reward`)
  - Potential loss on a loss (`risk`)
  - Number of consecutive bets (`n`)

- **Output**: 
  - The optimal betting size (as a percentage of available capital) using the Kelly Criterion formula.
  - Risk-reward ratio.
  - Monte Carlo simulation to estimate the mean, standard deviation, and probability of profitability across `n` consecutive bets.

## Kelly Criterion Formula

The formula used to calculate the optimal betting size is:

f* = p - [(1 - p) / (reward / risk)]

Where:
- `f*` is the fraction of your available capital to bet.
- `p` is the probability of winning.
- `reward` is the amount of money gained on a win (relative to the amount bet).
- `risk` is the amount of money lost on a loss (relative to the amount bet).

### Example

If you have a 60% probability of winning, will gain 1.5 times your bet on a win, and lose 1 time your bet on a loss, the Kelly Criterion will output the optimal bet size as a percentage of your total bankroll. If the result is negative, it suggests avoiding the bet as it is expected to lose in the long term.

## Installation

1. Make sure you have **Go** installed on your system. You can download it from [https://golang.org/dl/](https://golang.org/dl/).
2. Clone the repository or download the script file:

`git clone https://github.com/your-repo/kelly-criterion-bet-sizing.git`

3. Navigate to the directory and run the program:

`cd kelly-criterion-bet-sizing go run main.go`

## Usage

1. When running the program, you will be prompted to input the following values:
   - **Expected Probability of Winning** (e.g., `0.6` for 60%).
   - **Potential Risk** (the amount of money lost on a loss).
   - **Potential Reward** (the amount of money gained on a win).
   - **Number of Consecutive Bets** to simulate (e.g., `100`).

2. The program will calculate and display:
   - The **Risk-Reward Ratio**.
   - The **Optimal Kelly Size** (the fraction of your capital to bet).
   - The **Mean** and **Standard Deviation** of the results based on a Monte Carlo simulation.
   - The **Percentage of Profitable Bets** from the simulation.

3. You can use the **Optimal Kelly Size** as a guideline for determining how much capital to risk under the specified conditions. A negative result suggests that the bet is unfavorable and should be avoided for long-term profitability.

## Considerations

- The Kelly Criterion is best suited for **repeated bets** and aims to maximize long-term growth. It may not be ideal for short-term strategies with a high degree of uncertainty.
- While the Kelly Criterion can offer the optimal bet size mathematically, individual risk tolerance and market conditions should always be considered before making financial decisions.
- A **negative Kelly size** suggests the bet has a negative expectation and should likely be avoided.

## Example Calculation

For example, if:
- The **probability of winning** is 60% (or `p = 0.6`),
- The **reward** on a win is 1.5 times the bet amount,
- The **risk** on a loss is equal to the amount bet,

The Kelly Criterion formula would return a positive bet size, suggesting that the bet is favorable in the long term. However, if the calculated size is negative, it indicates that the bet is not statistically profitable in the long run.
