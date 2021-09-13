import sys
import random
import numpy as np
from pandas_datareader import data as pdr
import matplotlib.pyplot as plt
import datetime
from datetime import date
import yfinance as yf
yf.pdr_override()

#produce stats for given strike
def strike(mean, sigma, multiplier, optionsChain, optionType):
	if(optionType):
		call = mean + (sigma * multiplier)
		callStrike = optionsChain.iloc[(optionsChain["strike"]-call).abs().argsort()[:1]]
		print("+" + str(multiplier) + "σ Strike: " + str(callStrike["strike"].item()) + " Call Price: " + str(optionsChain["lastPrice"].iloc[callStrike["strike"].index.item()]))
	else:
		put = mean - (sigma * multiplier)
		putStrike = optionsChain.iloc[(optionsChain["strike"]-put).abs().argsort()[:1]]
		print("-" + str(multiplier) + "σ Strike: " + str(putStrike["strike"].item()) + " Put Price: " + str(optionsChain["lastPrice"].iloc[putStrike["strike"].index.item()]))

#get ticker from user
def getTicker():
    ticker = input("Enter your Ticker: ")
    data = yf.Ticker(ticker)
    if not data.options:
        sys.exit("Invalid Ticker")
    return ticker, data

#get date from user
def getDate(dates):
    for date in dates:
	    print(date)
    date = input("Enter your Expiration Date: ")
    if date not in dates:
	    sys.exit("Invalid Date")
    return date

#initial variables, including dates and ticker (ticker, startDate, and strikeDate need to be manually adjusted)
endDate = date.today()
startDate = endDate - datetime.timedelta(days = 180)
ticker, data = getTicker()
dates = data.options
strikeDate = getDate(dates)

#get price data for specified ticker and calculate annual volatility from it
prices = pdr.get_data_yahoo(ticker, start = startDate, end = endDate)
prices.sort_index(ascending=False, inplace=True)
prices['returns'] = prices["Adj Close"].pct_change().apply(lambda x: np.log(1+x))

#variables for simulation
numDays = np.busday_count(endDate, strikeDate) + 1
numRuns = 10000
startPrice = data.info['regularMarketPrice']
dailyVol = np.std(prices.returns)
annualDrift = np.log(prices["Adj Close"][0]) - np.log(prices["Adj Close"][-1])
dailyDrift = annualDrift / len(prices["Adj Close"])
dailyDriftMean = dailyDrift - (0.5 * dailyVol * dailyVol)

#get price data for options
optionData = data.option_chain(strikeDate)
callsData = optionData.calls
putsData = optionData.puts

#display simulation variables
print("Simulation Variables for " + str(ticker) + ":")
print("Strike Date: " + str(strikeDate))
print("Days till Expiry: " + str(numDays))
print("Runs: " + str(numRuns))
print("Start Price: " + str(round(startPrice, 2)))
print("Daily Volatility: " + str(round(dailyVol, 6)))
print("Daily Drift: " + str(round(dailyDriftMean, 6)), end = '\n\n')

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
print("Normal Distribution of Strikes and Metrics:")
print("μ: " + str(round(mean, 2)))
print("σ: " + str(round(sigma, 2)))
print("σ2: " + str(round(variance, 2)))

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
