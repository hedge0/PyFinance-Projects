import numpy as np
import pandas as pd
from pandas_datareader import data as pdr
import matplotlib.pyplot as plt
import datetime
from datetime import date
import yfinance as yf
yf.pdr_override()

#change strike date and ticker to adjust test
ticker = 'SPY'
strikeDate = '2021-02-05'

priceData = yf.Ticker(ticker)
optionData = priceData.option_chain(strikeDate)
callsData = optionData.calls
putsData = optionData.puts

sortedCallsData = callsData.sort_values(by=["impliedVolatility"])
sortedPutsData = putsData.sort_values(by=["impliedVolatility"])

print("Lowest IV among " + str(ticker) + " " + str(strikeDate) + " options:")
print("Call strike with lowest IV: " + str(sortedCallsData["strike"].head(1).item()) + " with IV = " + str(sortedCallsData["impliedVolatility"].head(1).item() * 100))
print("Put strike with lowest IV:  " + str(sortedPutsData["strike"].head(1).item()) + " with IV = " + str(sortedPutsData["impliedVolatility"].head(1).item() * 100))

fig, axs = plt.subplots(2)
fig.suptitle("Volatility Skew for " + str(ticker) + " " + str(strikeDate))
axs[0].plot(callsData["strike"], callsData["impliedVolatility"]*100)
axs[0].set_title("IV on calls")
axs[1].plot(putsData["strike"], putsData["impliedVolatility"]*100)
axs[1].set_title("IV on puts")
plt.show()