import math
import random
import numpy as np
import pandas as pd
from pandas_datareader import data as pdr
import matplotlib.pyplot as plt
import datetime
from datetime import date
import yfinance as yf
yf.pdr_override()

#initial variables, including dates and ticker (ticker, startDate, and strikeDate need to be manually adjusted)
endDate = date.today()
startDate = endDate - datetime.timedelta(days = 50)
ticker = 'SPY'
strikeDate = '2021-02-05'

#get price data for specified ticker and calculate annual volatility from it
prices = pdr.get_data_yahoo(ticker, start = startDate, end = endDate)
prices.sort_index(ascending=False, inplace=True)
prices['returns'] = (prices["Adj Close"] - prices["Adj Close"].shift(-1)) / prices["Adj Close"].shift(-1)

#variables for simulation
futureDay = strikeDate
numDays = np.busday_count(endDate, futureDay) + 1
numRuns = 10000
startPrice = prices["Adj Close"][0]
dailyVol = np.std(prices.returns)

#get price data for options
priceData = yf.Ticker(ticker)
optionData = priceData.option_chain(futureDay)
callsData = optionData.calls
putsData = optionData.puts

#display simulation variables
print("Simulation Variables for " + ticker + ":")
print("Strike date: " + str(futureDay))
print("Days till expiry: " + str(numDays))
print("Runs: " + str(numRuns))
print("Start price: " + str(round(startPrice, 2)))
print("Daily volatility: " + str(round(dailyVol, 5)), end = '\n\n\n')

#create 2d array of random daily volatility values and insert starting price
np.random.seed(random.randint(1, 10))
tempSimPrices = np.random.randn(numRuns, numDays) * dailyVol
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

threeSigCall = mean + sigma * 3
threeSigCallStrike = callsData.iloc[(callsData["strike"]-threeSigCall).abs().argsort()[:1]]
print("3 Sigma+ strike: " + str(threeSigCallStrike["strike"].item()) + "   with call option price = " + str(callsData["lastPrice"].iloc[threeSigCallStrike["strike"].index.item()]))

twoSigCall = mean + sigma * 2
twoSigCallStrike = callsData.iloc[(callsData["strike"]-twoSigCall).abs().argsort()[:1]]
print("2 Sigma+ strike: " + str(twoSigCallStrike["strike"].item()) + "   with call option price = " + str(callsData["lastPrice"].iloc[twoSigCallStrike["strike"].index.item()]))

oneSigCall = mean + sigma
oneSigCallStrike = callsData.iloc[(callsData["strike"]-oneSigCall).abs().argsort()[:1]]
print("1 Sigma+ strike: " + str(oneSigCallStrike["strike"].item()) + "   with call option price = " + str(callsData["lastPrice"].iloc[oneSigCallStrike["strike"].index.item()]))

oneSigPut = mean - sigma
oneSigPutStrike = putsData.iloc[(putsData["strike"]-oneSigPut).abs().argsort()[:1]]
print("1 Sigma- strike: " + str(oneSigPutStrike["strike"].item()) + "   with put option price = " + str(putsData["lastPrice"].iloc[oneSigPutStrike["strike"].index.item()]))

twoSigPut = mean - sigma * 2
twoSigPutStrike = putsData.iloc[(putsData["strike"]-twoSigPut).abs().argsort()[:1]]
print("2 Sigma- strike: " + str(twoSigPutStrike["strike"].item()) + "   with put option price = " + str(putsData["lastPrice"].iloc[twoSigPutStrike["strike"].index.item()]))

threeSigPut = mean - sigma * 3
threeSigPutStrike = putsData.iloc[(putsData["strike"]-threeSigPut).abs().argsort()[:1]]
print("3 Sigma- strike: " + str(threeSigPutStrike["strike"].item()) + "   with put option price = " + str(putsData["lastPrice"].iloc[threeSigPutStrike["strike"].index.item()]))

#label and display graph for simulation
plt.title(ticker)
plt.show()