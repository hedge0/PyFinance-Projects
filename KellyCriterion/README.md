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