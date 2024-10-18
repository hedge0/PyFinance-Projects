package main

import (
	"fmt"
	"math"
	"math/rand"
	"os"
	"strconv"
	"time"

	"gonum.org/v1/gonum/stat"
)

/**
 * Main function for the Kelly Criterion Monte Carlo simulation.
 * Prompts the user for probability, risk, reward, number of runs, and maximum risk limit.
 * Calculates the optimal Kelly size, performs Monte Carlo simulation, and outputs results
 * including the Sharpe Ratio and confidence intervals.
 */
func main() {
	rand.Seed(time.Now().UnixNano())

	var input string
	fmt.Print("Enter the Expected Probability of Winning: ")
	fmt.Scanln(&input)
	probability, _ := strconv.ParseFloat(input, 64)

	fmt.Print("Enter the Potential Risk: ")
	fmt.Scanln(&input)
	risk, _ := strconv.ParseFloat(input, 64)

	fmt.Print("Enter the Potential Reward: ")
	fmt.Scanln(&input)
	reward, _ := strconv.ParseFloat(input, 64)

	fmt.Print("Enter the Number of Consecutive Bets: ")
	fmt.Scanln(&input)
	runs, _ := strconv.Atoi(input)

	fmt.Print("Enter the Maximum Risk Limit (as a percentage of capital, e.g., 0.2 for 20%): ")
	fmt.Scanln(&input)
	maxRiskLimit, _ := strconv.ParseFloat(input, 64)

	fmt.Print("Enter the Number of Iterations for the Monte Carlo Simulation: ")
	fmt.Scanln(&input)
	iterations, _ := strconv.Atoi(input)

	kelly := new(Kelly)
	kelly.Init(probability, risk, reward, runs, maxRiskLimit)
	kelly.RunMonteCarlo(kelly.GetKelly(), iterations)

	// Display Results
	fmt.Printf("\nRisk Reward Ratio: %f\n", kelly.GetRatio())
	fmt.Printf("Optimal Kelly Size: %f\n", kelly.GetKelly())
	fmt.Printf("μ (Mean): %f\n", kelly.GetMean())
	fmt.Printf("σ (Standard Deviation): %f\n", kelly.GetSigma())
	fmt.Printf("%f%% Profitable Walks\n", kelly.GetProfitability()*100)
	fmt.Printf("Sharpe Ratio: %f\n", kelly.GetSharpeRatio())
	low, high := kelly.GetConfidenceInterval(0.95)
	fmt.Printf("95%% Confidence Interval for Final Value: [%f, %f]\n", low, high)
}

/**
 * Kelly struct represents the Kelly criterion parameters and Monte Carlo simulation results.
 * Fields:
 * - probability: The expected probability of winning.
 * - risk: The potential risk percentage.
 * - reward: The potential reward percentage.
 * - runs: Number of consecutive bets (steps in the simulation).
 * - ratio: Reward-to-risk ratio.
 * - kelly: Optimal Kelly size for the given parameters.
 * - maxRiskLimit: The maximum percentage of capital allowed to be risked.
 * - result: Slice storing the results of Monte Carlo simulations.
 * - mean: Mean value of the simulation outcomes.
 * - sigma: Standard deviation of the simulation outcomes.
 * - profitability: Percentage of profitable outcomes from the simulation.
 * - sharpeRatio: Risk-adjusted return metric (Sharpe Ratio) for the simulation.
 */
type Kelly struct {
	probability   float64
	risk          float64
	reward        float64
	runs          int
	ratio         float64
	kelly         float64
	maxRiskLimit  float64
	result        []float64
	mean          float64
	sigma         float64
	profitability float64
	sharpeRatio   float64
}

/**
 * Initializes the Kelly struct with the given parameters and maximum risk limit.
 * The Kelly size is adjusted to not exceed the maximum risk limit.
 *
 * @param probability - The expected probability of winning.
 * @param risk - The potential loss on a losing bet (expressed as a percentage).
 * @param reward - The potential gain on a winning bet (expressed as a percentage).
 * @param runs - The number of consecutive bets for the simulation.
 * @param maxRiskLimit - The maximum percentage of capital to risk.
 */
func (this *Kelly) Init(probability float64, risk float64, reward float64, runs int, maxRiskLimit float64) {
	this.probability = probability
	this.risk = risk
	this.reward = reward
	this.runs = runs
	this.maxRiskLimit = maxRiskLimit
	this.ratio = this.reward / this.risk

	kellySize := this.probability - ((1 - this.probability) / this.ratio)
	// Apply the risk limit to the Kelly size
	if kellySize > maxRiskLimit {
		this.kelly = maxRiskLimit
	} else {
		this.kelly = kellySize
	}
}

/**
 * Performs a Monte Carlo simulation with the given Kelly size and number of iterations.
 * Simulates multiple random walks to determine statistical metrics including the mean,
 * standard deviation, profitability, and Sharpe ratio.
 *
 * @param val - The optimal Kelly size (fraction of capital to bet).
 * @param iterations - The number of Monte Carlo simulation runs.
 */
func (this *Kelly) RunMonteCarlo(val float64, iterations int) {
	if val < 0 {
		os.Exit(1)
	}
	results := make([]float64, 0)
	for i := 0; i < iterations; i++ {
		randomWalk := []float64{1}
		for i := 1; i < this.runs; i++ {
			randomWalk = append(randomWalk, this._TotalValue(val, randomWalk[i-1]))
		}
		results = append(results, randomWalk[len(randomWalk)-1])
	}
	this.result = results
	this.mean = this._SetMean(results)
	this.sigma = this._SetSigma(results)
	this.profitability = this._SetProfitability(results)
	this.sharpeRatio = this._SetSharpeRatio(results)
}

/**
 * Get the reward-to-risk ratio, calculated from the risk and reward percentages.
 *
 * @return float64 - The reward-to-risk ratio.
 */
func (this *Kelly) GetRatio() float64 {
	return this.ratio
}

/**
 * Get the optimal Kelly size (fraction of capital to bet), adjusted for the risk limit.
 *
 * @return float64 - The adjusted Kelly size.
 */
func (this *Kelly) GetKelly() float64 {
	return this.kelly
}

/**
 * Get the mean of the Monte Carlo simulation outcomes.
 *
 * @return float64 - The mean value of the final simulation results.
 */
func (this *Kelly) GetMean() float64 {
	return this.mean
}

/**
 * Get the standard deviation (sigma) of the Monte Carlo simulation outcomes.
 *
 * @return float64 - The standard deviation of the final simulation results.
 */
func (this *Kelly) GetSigma() float64 {
	return this.sigma
}

/**
 * Get the percentage of profitable outcomes from the Monte Carlo simulation.
 *
 * @return float64 - The percentage of profitable outcomes.
 */
func (this *Kelly) GetProfitability() float64 {
	return this.profitability
}

/**
 * Get the Sharpe ratio, calculated as the mean return divided by the standard deviation of returns.
 * A higher Sharpe ratio indicates better risk-adjusted performance.
 *
 * @return float64 - The Sharpe ratio.
 */
func (this *Kelly) GetSharpeRatio() float64 {
	return this.sharpeRatio
}

/**
 * Calculate the confidence interval for the final values of the simulation.
 * ConfidenceLevel should be between 0 and 1 (e.g., 0.95 for a 95% confidence interval).
 *
 * @param confidenceLevel - The desired confidence level for the interval.
 * @return float64, float64 - The lower and upper bounds of the confidence interval.
 */
func (this *Kelly) GetConfidenceInterval(confidenceLevel float64) (float64, float64) {
	low, high := stat.Empirical(confidenceLevel, this.result, nil)
	return low, high
}

/**
 * Helper function to calculate the total value of a bet in the random walk.
 * Updates the capital based on a win or loss outcome, determined by the probability of winning.
 *
 * @param val - The Kelly fraction (percentage of capital to bet).
 * @param prev - The previous total value (capital from the previous round).
 * @return float64 - The updated total value (capital) after applying the bet outcome.
 */
func (this *Kelly) _TotalValue(val float64, prev float64) float64 {
	var total float64
	if rand.Float64() < this.probability {
		total = (1+this.reward)*(val*prev) + (1-val)*prev
	} else {
		total = (1-this.risk)*(val*prev) + (1-val)*prev
	}
	return total
}

/**
 * Helper function to calculate the mean of the simulation results.
 * The mean represents the average final capital value across all Monte Carlo simulations.
 *
 * @param results []float64 - The final values from each Monte Carlo simulation run.
 * @return float64 - The mean (average) final value.
 */
func (this *Kelly) _SetMean(results []float64) float64 {
	total := 0.0
	for _, number := range results {
		total += number
	}
	return total / float64(len(results))
}

/**
 * Helper function to calculate the standard deviation (sigma) of the simulation results.
 * Standard deviation is a measure of the dispersion of final values around the mean.
 *
 * @param results []float64 - The final values from each Monte Carlo simulation run.
 * @return float64 - The standard deviation of the final values.
 */
func (this *Kelly) _SetSigma(results []float64) float64 {
	total := 0.0
	mean := this.mean
	for _, number := range results {
		total += math.Pow((number - mean), 2)
	}
	return math.Sqrt(total / float64(len(results)))
}

/**
 * Helper function to calculate the percentage of profitable outcomes.
 * A profitable outcome is defined as a final value greater than 1 (the starting capital).
 *
 * @param results []float64 - The final values from each Monte Carlo simulation run.
 * @return float64 - The percentage of profitable runs.
 */
func (this *Kelly) _SetProfitability(results []float64) float64 {
	profitable := 0
	for _, number := range results {
		if number > 1 {
			profitable++
		}
	}
	return float64(profitable) / float64(len(results))
}

/**
 * Helper function to calculate the Sharpe ratio for the simulation outcomes.
 * The Sharpe ratio is the mean return divided by the standard deviation, representing
 * risk-adjusted performance.
 *
 * @param results []float64 - The final values from each Monte Carlo simulation run.
 * @return float64 - The Sharpe ratio of the outcomes.
 */
func (this *Kelly) _SetSharpeRatio(results []float64) float64 {
	meanReturn := this.mean - 1 // mean excess return (assuming starting value of 1)
	if this.sigma == 0 {
		return 0
	}
	return meanReturn / this.sigma
}
