import pandas as pd
from pandas_datareader import data as pdr
import matplotlib.pyplot as plt
import datetime
from datetime import date
import yfinance as yf
yf.pdr_override()

today = date.today()
endDate = today
startDate = "2005-01-01"
ticker1 = 'SPY'
ticker2 = 'GLD'

stock1 = pdr.get_data_yahoo(ticker1, start = startDate, end = endDate)
stock2 = pdr.get_data_yahoo(ticker2, start = startDate, end = endDate)

stock1 = stock1["Adj Close"]
stock2 = stock2["Adj Close"]

fig, axs = plt.subplots(2)
fig.suptitle('Compare 2 Stocks')
axs[0].plot(stock1.index, stock1)
axs[0].set_title(str(ticker1))
axs[1].plot(stock2.index, stock2)
axs[1].set_title(str(ticker2))
plt.show()