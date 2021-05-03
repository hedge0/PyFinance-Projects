import numpy as np
import pandas as pd
from pandas_datareader import data as pdr
import datetime
from datetime import date
from operator import itemgetter
import statsmodels
from statsmodels.tsa.stattools import coint
import yfinance as yf
yf.pdr_override()

#set starting variables (only need to manuably set tickers)
endDate = date.today()
startDate = endDate - datetime.timedelta(days = 5 * 365)
tickers = ['SMH', 'ARKK', 'XLK', 'QQQ', 'AAPL', 'MSFT', 'TSLA', 'ORCL', 'QCOM', 'AMD', 'UBER', 'SQ']

#get data for each ticker
data = pdr.get_data_yahoo(tickers, start = startDate, end = endDate)
prices = data["Adj Close"].dropna(axis='columns')

#set up data for test
keysList = prices.keys()
keySize = len(keysList)
uniquePairs = (keySize * (keySize - 1)) / 2
pValMax = 0.5
pairsList = []

print("\n" + str(keySize) + " tickers span a valid backtest with " + str(int(uniquePairs)) + " possible pair(s).")

#run cointegration test on all possible pairs
for i in range(keySize):
    for j in range(i + 1, keySize):
    	stock1 = prices[keysList[i]]
    	stock2 = prices[keysList[j]]
    	result = coint(stock1, stock2)
    	pvalue = result[1]
    	
    	if(pvalue < pValMax):
    		corr = np.corrcoef(stock1, stock2)
    		pairsList.append((keysList[i], keysList[j], pvalue, corr[0][1]))

pairsList = sorted(pairsList, key = itemgetter(3), reverse = True)

print(str(len(pairsList)) + " possible cointegrated pairs with p-values less than " + str(pValMax) + ":")

#print out valid pairs with sufficient p-value
for pair in pairsList:
	print("\n" + str(pair[0]) + " and " + str(pair[1]) + ":")
	print("p-value = " + str(round(pair[2], 4)))
	print("correlation coefficient = " + str(round(pair[3], 4)))
