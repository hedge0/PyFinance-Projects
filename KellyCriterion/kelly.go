package main

import (
	"fmt"
	"math"
	"math/rand"
	"os"
	"strconv"
)

/**
 * Main function for the Kelly Criterion Monte Carlo simulation.
 * Prompts the user for probability, risk, reward, and number of runs, then
 * calculates the optimal Kelly size and performs Monte Carlo simulation.
 */
func main() {
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

	kelly := new(Kelly)
	kelly.Init(probability, risk, reward, runs)
	kelly.RunMonteCarlo(kelly.GetKelly(), 10000)
	fmt.Printf("\nRisk Reward Ratio: %f\n", kelly.GetRatio())
	fmt.Printf("Optimal Kelly Size: %f\n", kelly.GetKelly())
	fmt.Printf("μ: %f\n", kelly.GetMean())
	fmt.Printf("σ: %f\n", kelly.GetSigma())
	fmt.Printf("%f%% Profitable Walks\n", kelly.GetProfitability()*100)
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
 * - result: Slice storing the results of Monte Carlo simulations.
 * - mean: Mean value of the simulation outcomes.
 * - sigma: Standard deviation of the simulation outcomes.
 * - profitability: Percentage of profitable outcomes from the simulation.
 */
type Kelly struct {
	probability   float64
	risk          float64
	reward        float64
	runs          int
	ratio         float64
	kelly         float64
	result        []float64
	mean          float64
	sigma         float64
	profitability float64
}

/**
 * Initializes the Kelly struct with the given probability, risk, reward, and number of runs.
 *
 * @param probability - Expected probability of winning.
 * @param risk - Potential risk percentage.
 * @param reward - Potential reward percentage.
 * @param runs - Number of consecutive bets.
 */
func (this *Kelly) Init(probability float64, risk float64, reward float64, runs int) {
	this.probability = probability
	this.risk = risk
	this.reward = reward
	this.runs = runs
	this.ratio = this.reward / this.risk
	this.kelly = this.probability - ((1 - this.probability) / this.ratio)
}

/**
 * Performs a Monte Carlo simulation to estimate the mean, standard deviation, and profitability of the strategy.
 *
 * @param val - Optimal Kelly size.
 * @param iterations - Number of iterations for the Monte Carlo simulation.
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
}

/**
 * Get the reward-to-risk ratio.
 *
 * @return ratio - Reward-to-risk ratio.
 */
func (this *Kelly) GetRatio() float64 {
	return this.ratio
}

/**
 * Get the optimal Kelly size.
 *
 * @return kelly - Optimal Kelly size.
 */
func (this *Kelly) GetKelly() float64 {
	return this.kelly
}

/**
 * Get the mean of the Monte Carlo simulation outcomes.
 *
 * @return mean - Mean value of the simulation results.
 */
func (this *Kelly) GetMean() float64 {
	return this.mean
}

/**
 * Get the standard deviation (sigma) of the Monte Carlo simulation outcomes.
 *
 * @return sigma - Standard deviation of the simulation results.
 */
func (this *Kelly) GetSigma() float64 {
	return this.sigma
}

/**
 * Get the percentage of profitable outcomes from the Monte Carlo simulation.
 *
 * @return profitability - Percentage of profitable walks.
 */
func (this *Kelly) GetProfitability() float64 {
	return this.profitability
}

/**
 * Helper function to calculate the total value of a bet in the random walk.
 *
 * @param val - Kelly fraction.
 * @param prev - Previous total value.
 * @return total - Updated total value based on win or loss.
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
 * Helper function to calculate the mean of simulation results.
 *
 * @param results - Slice containing the results of the Monte Carlo simulation.
 * @return mean - Calculated mean value.
 */
func (this *Kelly) _SetMean(results []float64) float64 {
	total := 0.0
	for _, number := range results {
		total += number
	}
	return (total / float64(len(results)))
}

/**
 * Helper function to calculate the standard deviation (sigma) of simulation results.
 *
 * @param results - Slice containing the results of the Monte Carlo simulation.
 * @return sigma - Calculated standard deviation.
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
 * Helper function to calculate the profitability percentage from the Monte Carlo simulation.
 *
 * @param results - Slice containing the results of the Monte Carlo simulation.
 * @return profitability - Percentage of outcomes where the value is greater than 1.
 */
func (this *Kelly) _SetProfitability(results []float64) float64 {
	filtered := make([]float64, 0)
	for _, number := range results {
		if number > 1 {
			filtered = append(filtered, number)
		}
	}
	return float64(len(filtered)) / float64(len(results))
}
