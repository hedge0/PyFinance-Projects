package main

import (
	"fmt"
	"math"
	"math/rand"
	"os"
	"strconv"
)

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

func (this *Kelly) Init(probability float64, risk float64, reward float64, runs int) {
	this.probability = probability
	this.risk = risk
	this.reward = reward
	this.runs = runs
	this.ratio = this.reward / this.risk
	this.kelly = this.probability - ((1 - this.probability) / this.ratio)
}

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

func (this *Kelly) GetRatio() float64 {
	return this.ratio
}

func (this *Kelly) GetKelly() float64 {
	return this.kelly
}

func (this *Kelly) GetMean() float64 {
	return this.mean
}

func (this *Kelly) GetSigma() float64 {
	return this.sigma
}

func (this *Kelly) GetProfitability() float64 {
	return this.profitability
}

func (this *Kelly) _TotalValue(val float64, prev float64) float64 {
	var total float64
	if rand.Float64() < this.probability {
		total = (1+this.reward)*(val*prev) + (1-val)*prev
	} else {
		total = (1-this.risk)*(val*prev) + (1-val)*prev
	}
	return total
}

func (this *Kelly) _SetMean(results []float64) float64 {
	total := 0.0
	for _, number := range results {
		total += number
	}
	return (total / float64(len(results)))
}

func (this *Kelly) _SetSigma(results []float64) float64 {
	total := 0.0
	mean := this.mean
	for _, number := range results {
		total += math.Pow((number - mean), 2)
	}
	return math.Sqrt(total / float64(len(results)))
}

func (this *Kelly) _SetProfitability(results []float64) float64 {
	filtered := make([]float64, 0)
	for _, number := range results {
		if number > 1 {
			filtered = append(filtered, number)
		}
	}
	return float64(len(filtered)) / float64(len(results))
}
