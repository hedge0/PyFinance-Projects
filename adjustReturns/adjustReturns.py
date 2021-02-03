import math
import numpy as np
import pandas as pd
from pandas_datareader import data as pdr
import datetime
from datetime import date
from operator import itemgetter
import yfinance as yf
yf.pdr_override()

#initial variables, including dates and tickers (tickers and startDate need to be manually adjusted)
endDate = date.today()
startDate = endDate - datetime.timedelta(days = 365 * 1)
payload = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
df = payload[0]
tickers = df['Symbol'].values.tolist()

#get price data for specified ticker
data = pdr.get_data_yahoo(tickers, start = startDate, end = endDate)
prices = data["Adj Close"].dropna(axis = 'columns')
prices.sort_index(ascending = False, inplace = True)

keysList = prices.keys()
volList = []

#calcuate specific values such as annual volatility and annual return
for key in keysList:
	vol = (prices[key] - prices[key].shift(-1)) / prices[key].shift(-1)
	dailyVol = np.std(vol)
	annualVol = (dailyVol * math.sqrt(len(vol))) * 100
	annualReturn = ((prices[key][0] / prices[key][-1]) - 1) * 100
	ratio = annualReturn / annualVol
	volList.append([key, annualVol, annualReturn, ratio])

#sort list by ratio
sortedList = sorted(volList, key = itemgetter(3), reverse=True)
print("")

#display results in order from best performing to worst performing securities by annual return adjusted by volatility
for item in sortedList:
	print(str(item[0]) + " has a return of: " + str(round(item[2], 2)) + "%")
	print("When adjusted for volatility: " + str(round(item[1], 2)) + "%, the ratio is : " + str(round(item[3], 2)), end = '\n\n')
