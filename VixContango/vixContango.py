import pandas as pd
from pandas_datareader import data as pdr
import numpy as np
import matplotlib.pyplot as plt
import datetime
from datetime import date
import quandl
import yfinance as yf
yf.pdr_override()

#Paste your api key here to unlock data from quandl, remember to remove key if code is public
apiKey = ""

#starting variables
endDate = date.today()
startDate = endDate - datetime.timedelta(days = 5 * 365)

#retrieve data
vixSpotData = pdr.get_data_yahoo('^VIX', start = startDate, end = endDate)
vixSpot = vixSpotData["Adj Close"]

vixFrontData = quandl.get('CHRIS/CBOE_VX1', trim_start = startDate, trim_end = endDate, authtoken = apiKey)
vixFront = vixFrontData["Settle"]

vixSecondData = quandl.get('CHRIS/CBOE_VX2', trim_start = startDate, trim_end = endDate, authtoken = apiKey)
vixSecond = vixSecondData["Settle"]

#create ratio for vix 
ratio = ((vixSpot / vixFront) * 0.7) + ((vixFront / vixSecond) * 0.3) - 1
mean = np.mean(ratio)
std = np.std(ratio)
upperBound = mean + (2.5 * std)
lowerBound = mean - (1.5 * std)

#plot results via matplotlib
fig, (ax1, ax2) = plt.subplots(2)
ax1.plot(ratio.keys(), ratio)
ax1.axhline(y = upperBound, color = "green", lw = 1)
ax1.axhline(y = lowerBound, color = "red", lw = 1)
ax1.axhline(y = mean, color = "black", lw = 1)
ax1.set_title("Contango / Backwardation Ratio")
ax2.plot(vixSpot.keys(), vixSpot)
ax2.set_title("VIX Spot Price")
plt.show()
