package main

import (
	"fmt"
	"math"
	"math/rand"
	"os"
)

func main() {
	kelly := new(Kelly)
	kelly.Init(.6, .5, .9, 20)
	kelly.RunMonteCarlo(kelly.GetKelly(), 10000)
	fmt.Println(kelly.GetMean())
	fmt.Println(kelly.GetSigma())
	fmt.Println(kelly.GetProfitability())
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
	return math.Round(this.ratio*100) / 100
}

func (this *Kelly) GetKelly() float64 {
	return math.Round(this.kelly*100) / 100
}

func (this *Kelly) GetMean() float64 {
	return math.Round(this.mean*100) / 100
}

func (this *Kelly) GetSigma() float64 {
	return math.Round(this.sigma*100) / 100
}

func (this *Kelly) GetProfitability() float64 {
	return math.Round(this.profitability*10000) / 10000
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
	var total float64 = 0
	for _, number := range results {
		total += number
	}
	return (total / float64(len(results)))
}

func (this *Kelly) _SetSigma(results []float64) float64 {
	var total float64 = 0
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
