from math import floor
from numpy import random, dot, sum, log, sqrt
from pandas import DataFrame
from pandas_datareader import data as pdr
from datetime import date, timedelta
import yfinance as yf
yf.pdr_override()


def main():
    # initial variables, including dates, portfolio size, number of desired securities in portfolio, and tickers (tickers, port size, # of port securities, and startDate need to be manually adjusted)
    tickers = ['MSFT', 'TSLA', 'AMZN', 'AAPL']
    prices = getPrices(tickers)
    covMatrix = prices.pct_change().apply(lambda x: log(1+x)).cov()
    yearlyReturns = prices.resample('Y').last().pct_change().mean()
    portRet = []
    portVol = []
    portWeights = []
    portfolioSize = 100000.00
    numRuns = 10000

    # run random weights on covariance matrix to find maximum return on volatility portfolio
    for i in range(numRuns):
        weights = random.random(len(prices.columns))
        weights = weights / sum(weights)
        portWeights.append(weights)
        portRet.append(dot(weights, yearlyReturns))
        portVol.append(sqrt(covMatrix.mul(weights, axis=0).mul(
            weights, axis=1).sum().sum()) * sqrt(252))
    newData = {'Annualized Returns': portRet, 'Annualized Volatility': portVol}
    for counter, symbol in enumerate(prices.columns.tolist()):
        newData[symbol] = [w[counter] for w in portWeights]

    # get results for ideal portfolio
    portfolios = DataFrame(newData)
    optimalPort = portfolios.iloc[(
        portfolios['Annualized Returns'] / portfolios['Annualized Volatility']).idxmax()]
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
            sharesNum = floor(percentPort / currentPrice)
            if(sharesNum > 0):
                print(f"{key} has a stock price of ${currentPrice}")
                print(
                    f"Buy {sharesNum} shares of {key} at {round(optimalPort[key] * 100, 2)}%\n")


# query data for every ticker and parse data
def getPrices(tickers):
    data = pdr.get_data_yahoo(tickers, start=date.today(
    ) - timedelta(days=2 * 365), end=date.today())
    prices = data["Adj Close"]
    return prices


if __name__ == '__main__':
    main()
