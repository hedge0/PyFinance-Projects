import math
import numpy as np
import pandas as pd
from pandas_datareader import data as pdr
import datetime
from datetime import date
from wallstreet import Stock
import yfinance as yf
yf.pdr_override()

#initial variables, including dates, portfolio size, number of desired securities in portfolio, and tickers (tickers, port size, # of port securities, and startDate need to be manually adjusted)
endDate = date.today()
startDate = endDate - datetime.timedelta(days = 365 * 2)
tickers = ['RH', 'LAD', 'SYNA', 'WSO', 'MASI', 'TREX', 'AVLR', 'ZNGA', 'PEN', 'PLTR', 'DKNG', 'AZPN', 'HUBB', 'TECH']
portfolioSize = 100000.00

#get data for list of picked securities
data2 = pdr.get_data_yahoo(tickers, start = startDate, end = endDate)
prices = data2["Adj Close"]
covMatrix = prices.pct_change().apply(lambda x: np.log(1+x)).cov()
yearlyReturns = prices.resample('Y').last().pct_change().mean()

portRet = [] 
portVol = [] 
portWeights = []
numAssets = len(prices.columns)
numRuns = 10000

#run random weights on covariance matrix to find maximum return on volatility portfolio
for portfolio in range(numRuns):
	weights = np.random.random(numAssets)
	weights = weights / np.sum(weights)
	portWeights.append(weights)
	portRet.append(np.dot(weights, yearlyReturns))
	portVol.append(np.sqrt(covMatrix.mul(weights, axis = 0).mul(weights, axis = 1).sum().sum()) * np.sqrt(252))

newData = {'Annualized Returns':portRet, 'Annualized Volatility':portVol}
for counter, symbol in enumerate(prices.columns.tolist()):
    newData[symbol] = [w[counter] for w in portWeights]

#get results for ideal portfolio
portfolios = pd.DataFrame(newData)
optimalPort = portfolios.iloc[(portfolios['Annualized Returns'] / portfolios['Annualized Volatility']).idxmax()]
newKeysList = optimalPort.keys()

#print results and metrics
print("\nPortfolio Size = $" + str(portfolioSize))
count = 0
newReturn = 0
newVol = 0

for key in newKeysList:
	if(count == 0):
		newReturn = optimalPort[key]
		print(str(key) + ": " + str(round(optimalPort[key] * 100, 2)) + "%")
		count += 1
	elif(count == 1):
		newVol = optimalPort[key]
		print(str(key) + ": " + str(round(optimalPort[key] * 100, 2)) + "%")
		print("Sharpe Ratio: " + str(round(newReturn / newVol, 2)))
		count += 1
	else:
		percentPort = portfolioSize * optimalPort[key]
		currentPrice = Stock(key).price
		sharesNum = math.floor(percentPort / currentPrice)

		if(count == 2):
			print("")
			count += 1
		
		if(sharesNum > 0):
			print(str(key) + " has a stock price of $" + str(currentPrice))
			print("Buy " + str(sharesNum) + " shares of " + str(key) + " at " + str(round(optimalPort[key] * 100, 2)) + "%")