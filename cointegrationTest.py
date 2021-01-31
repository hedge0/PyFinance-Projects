import numpy as np
import pandas as pd
from pandas_datareader import data as pdr
import matplotlib.pyplot as plt
import datetime
from datetime import date
import statsmodels
from statsmodels.tsa.stattools import coint
from pykalman import KalmanFilter
from math import sqrt
import yfinance as yf
yf.pdr_override()

#set starting variables (only need to manuably set tickers)
today = date.today()
fiveYearsAgo = today - datetime.timedelta(days = 5 * 365)
endDate = today
startDate = fiveYearsAgo
tickers = ['SLV', 'GDX', 'GLD', 'IAU', 'GDXJ', 'GLDM', 'XME', 'SIVR', 'BAR', 'SIL', 'SLVP']

#get data for each ticker
data = pdr.get_data_yahoo(tickers, start = startDate, end = endDate)
prices = data["Adj Close"].dropna(axis='columns')

#set up data for test
keysList = prices.keys()
keySize = len(keysList)
uniquePairs = (keySize * (keySize - 1)) / 2
pValMax = 0.05
pairsList = []

print('\n' + str(keySize) + " tickers span a valid backtest with " + str(int(uniquePairs)) + " possible pair(s).", end = '\n\n')

#run cointegration test on all possible pairs
for i in range(keySize):
    for j in range(i + 1, keySize):
    	stock1 = prices[keysList[i]]
    	stock2 = prices[keysList[j]]
    	result = coint(stock1, stock2)
    	pvalue = result[1]
    	
    	if(pvalue < pValMax):
    		pairsList.append((keysList[i], keysList[j], pvalue))

print(str(len(pairsList)) + " possible cointegrated pairs with p-values less than " + str(pValMax) + ":")

#print out valid pairs with sufficient p-value
for pair in pairsList:
	print(str(pair[0]) + " and " + str(pair[1]) + " have p-value = " + str(pair[2]))