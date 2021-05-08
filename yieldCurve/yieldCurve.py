import pandas as pd
from pandas_datareader import data as pdr
import matplotlib.pyplot as plt
import datetime
from datetime import date
import quandl

#Paste your api key here to unlock data from quandl, remember to remove key if code is public
apiKey = ""

#starting variables
today = date.today()
endDate = today
startDate = "2000-01-01"

#get yields data for 2 and 10 year
yields = quandl.get('FRED/T10Y2Y', trim_start = startDate, trim_end = today, authtoken = apiKey)
yields = yields["Value"]

keysList = yields.keys()
keySize = len(keysList)

inverted = False
notInverted = False

#graph yield curve along with arrows for sell points after inversions
for i in range(keySize):
	if(not inverted and (yields[keysList[i]] < 0)):
		notInverted = False
		inverted = True
	if(not notInverted and inverted and (yields[keysList[i]] > 0.25)):
		notInverted = True
		inverted = False
		plt.scatter(keysList[i], yields[keysList[i]] + 0.01, label='skitscat', color='red', s=25, marker="v")
		print("Sell: " + str(keysList[i]))

#title and plot graph
yields.plot(figsize=(20,10)).axhline(y = 0, color = "black", lw = 1)
plt.title("2-10T Yield Curve")
plt.show()
