import math
import random
import numpy as np
import pandas as pd
from pandas_datareader import data as pdr
import matplotlib.pyplot as plt
import datetime
from datetime import date
from wallstreet import Stock
import yfinance as yf
yf.pdr_override()

def strike(mean, sigma, multiplier, optionsChain, optionType):
	if(optionType):
		call = mean + (sigma * multiplier)
		callStrike = optionsChain.iloc[(optionsChain["strike"]-call).abs().argsort()[:1]]
		print(str(multiplier) + "*(+σ) strike: " + str(callStrike["strike"].item()) + "   with call option price = " + str(optionsChain["lastPrice"].iloc[callStrike["strike"].index.item()]))
	else:
		put = mean - (sigma * multiplier)
		putStrike = optionsChain.iloc[(optionsChain["strike"]-put).abs().argsort()[:1]]
		print(str(multiplier) + "*(-σ) strike: " + str(putStrike["strike"].item()) + "   with put option price = " + str(optionsChain["lastPrice"].iloc[putStrike["strike"].index.item()]))

#initial variables, including dates and ticker (ticker, startDate, and strikeDate need to be manually adjusted)
endDate = date.today()
startDate = endDate - datetime.timedelta(days = 180)
ticker = 'SPY'
strikeDate = '2021-05-26'

#get price data for specified ticker and calculate annual volatility from it
prices = pdr.get_data_yahoo(ticker, start = startDate, end = endDate)
prices.sort_index(ascending=False, inplace=True)
prices['returns'] = prices["Adj Close"].pct_change().apply(lambda x: np.log(1+x))

#variables for simulation
futureDay = strikeDate
numDays = np.busday_count(endDate, futureDay) + 1
numRuns = 10000
startPrice = Stock(ticker).price
dailyVol = np.std(prices.returns)
annualDrift = np.log(prices["Adj Close"][0]) - np.log(prices["Adj Close"][-1])
dailyDrift = annualDrift / len(prices["Adj Close"])
dailyDriftMean = dailyDrift - (0.5 * dailyVol * dailyVol)

#get price data for options
priceData = yf.Ticker(ticker)
optionData = priceData.option_chain(futureDay)
callsData = optionData.calls
putsData = optionData.puts

#display simulation variables
print("Simulation Variables for " + str(ticker) + ":")
print("Strike date: " + str(futureDay))
print("Days till expiry: " + str(numDays))
print("Runs: " + str(numRuns))
print("Start price: " + str(round(startPrice, 2)))
print("Daily volatility: " + str(round(dailyVol, 6)))
print("Daily drift: " + str(round(dailyDriftMean, 6)), end = '\n\n\n')

#create 2d array of random daily volatility values and insert starting price
np.random.seed(random.randint(1, 10))
tempSimPrices = np.random.randn(numRuns, numDays) * dailyVol + dailyDriftMean
simPrices = np.insert(tempSimPrices, 0, startPrice, axis = 1)

#calculate simulation values from 2d array of random daily volatility values
for i in range(numRuns):
	for j in range(1, numDays + 1):
		simPrices[i][j] = (simPrices[i][j] + 1) * simPrices[i][j - 1]

finalPrices = []

#plot simulation results
for sim in simPrices:
	plt.plot(sim)
	finalPrices.append(sim[-1])

#calculate simulation results
mean = np.mean(finalPrices) 
sigma = np.std(finalPrices) 
variance = np.var(finalPrices) 

#display metrics, plus option values
print("StDev Distribution of strikes and metrics:")
print("Mean: " + str(round(mean, 2)))
print("StDev: " + str(round(sigma, 2)))
print("Variance: " + str(round(variance, 2)))

strike(mean, sigma, 3, callsData, True)
strike(mean, sigma, 2, callsData, True)
strike(mean, sigma, 1, callsData, True)
strike(mean, sigma, 0, callsData, True)
strike(mean, sigma, 0, putsData, False)
strike(mean, sigma, 1, putsData, False)
strike(mean, sigma, 2, putsData, False)
strike(mean, sigma, 3, putsData, False)

#label and display graph for simulation
plt.title(ticker)
plt.show()
