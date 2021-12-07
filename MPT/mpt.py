import math
import numpy as np
import pandas as pd
from pandas_datareader import data as pdr
import datetime
from datetime import date
import yfinance as yf
yf.pdr_override()

# initial variables, including dates, portfolio size, number of desired securities in portfolio, and tickers (tickers, port size, # of port securities, and startDate need to be manually adjusted)
endDate = date.today()
startDate = endDate - datetime.timedelta(days=365 * 2)
tickers = ['MSFT', 'TSLA', 'AMZN', 'AAPL']
portfolioSize = 100000.00

# get data for list of picked securities
data2 = pdr.get_data_yahoo(tickers, start=startDate, end=endDate)
prices = data2["Adj Close"]
covMatrix = prices.pct_change().apply(lambda x: np.log(1+x)).cov()
yearlyReturns = prices.resample('Y').last().pct_change().mean()

portRet = []
portVol = []
portWeights = []
numRuns = 10000

# run random weights on covariance matrix to find maximum return on volatility portfolio
for portfolio in range(numRuns):
    weights = np.random.random(len(prices.columns))
    weights = weights / np.sum(weights)
    portWeights.append(weights)
    portRet.append(np.dot(weights, yearlyReturns))
    portVol.append(np.sqrt(covMatrix.mul(weights, axis=0).mul(
        weights, axis=1).sum().sum()) * np.sqrt(252))

newData = {'Annualized Returns': portRet, 'Annualized Volatility': portVol}
for counter, symbol in enumerate(prices.columns.tolist()):
    newData[symbol] = [w[counter] for w in portWeights]

# get results for ideal portfolio
portfolios = pd.DataFrame(newData)
optimalPort = portfolios.iloc[(
    portfolios['Annualized Returns'] / portfolios['Annualized Volatility']).idxmax()]
newKeysList = optimalPort.keys()

ret = optimalPort['Annualized Returns']
vol = optimalPort['Annualized Volatility']

# print results and metrics
print(f"\nPortfolio Size = ${portfolioSize}")
print(f"{'Annualized Returns'}: {round(ret * 100, 2)}%")
print(f"{'Annualized Volatility'}: {round(vol * 100, 2)}%")
print(f"Sharpe Ratio: {round(ret / vol, 2)}\n")

for key in tickers:
    if(optimalPort[key]):
        percentPort = portfolioSize * optimalPort[key]
        currentPrice = yf.Ticker(key).info['regularMarketPrice']
        sharesNum = math.floor(percentPort / currentPrice)

        if(sharesNum > 0):
            print(f"{key} has a stock price of ${currentPrice}")
            print(
                f"Buy {sharesNum} shares of {key} at {round(optimalPort[key] * 100, 2)}%\n")