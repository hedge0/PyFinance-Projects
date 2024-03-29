from math import floor
from numpy import random, dot, sum, log, sqrt
from pandas import DataFrame
from pandas_datareader import data as pdr
from datetime import date, timedelta
import yfinance as yf
yf.pdr_override()

class MPT:
    def __init__(self, tickers, years):
        self.tickers = tickers
        self.prices = self._getPrices(tickers, years)
        self.covMatrix = self.prices.pct_change().cov()
        self.yearlyReturns = self.prices.resample('Y').last().pct_change().mean()
        self.optimalPort = None
        self.ret = None
        self.vol = None
        self.sharpe = None

    # simulate random weights on covariance matrix to find maximum return on volatility portfolio
    def runSimulation(self, runs):
        portRet = []
        portVol = []
        portWeights = []
        for _ in range(runs):
            weights = random.random(len(self.prices.columns))
            weights = weights / sum(weights)
            portWeights.append(weights)
            portRet.append(dot(weights, self.yearlyReturns))
            portVol.append(sqrt(self.covMatrix.mul(weights, axis=0).mul(
                weights, axis=1).sum().sum()) * sqrt(252))
        results = {'Annualized Returns': portRet, 'Annualized Volatility': portVol}
        for counter, symbol in enumerate(self.prices.columns.tolist()):
            results[symbol] = [w[counter] for w in portWeights]
        ports = DataFrame(results)
        self.optimalPort = ports.iloc[(
            ports['Annualized Returns'] / ports['Annualized Volatility']).idxmax()].to_dict()
        self.ret = self.optimalPort['Annualized Returns']
        self.vol = self.optimalPort['Annualized Volatility']
        self.sharpe = self.ret / self.vol
        del self.optimalPort['Annualized Returns']
        del self.optimalPort['Annualized Volatility']

    # get optimal portfolio
    def getPortfolio(self):
        return self.optimalPort

    # get annual return of portfolio
    def getReturn(self):
        return self.ret

    # get annual volatility of portfolio
    def getVolatility(self):
        return self.vol

    # get sharpe ratio
    def getSharpe(self):
        return self.sharpe

    # query data for every ticker and parse data
    def _getPrices(self, tickers, years):
        prices = pdr.get_data_yahoo(tickers, start=date.today(
        )-timedelta(days=years*365), end=date.today())["Adj Close"]
        return prices
        