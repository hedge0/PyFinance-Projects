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
startDate = "1999-01-01"

#get yields data for 2 and 10 year
yields = quandl.get('USTREASURY/YIELD', trim_start = startDate, trim_end = today, authtoken = apiKey)
twoYear = yields['2 YR']
tenYear = yields['10 YR']

#create yield curve from 2-10 year yields
FRR2_10 = (5 * tenYear - twoYear) / (4 * tenYear)
keysList = FRR2_10.keys()
keySize = len(keysList)

inverted = False
notInverted = False

#graph yield curve along with arrows for sell points after inversions
for i in range(keySize):
	if(not inverted and (FRR2_10[keysList[i]] < 1)):
		notInverted = False
		inverted = True
	if(not notInverted and inverted and (FRR2_10[keysList[i]] > 1.025)):
		notInverted = True
		inverted = False
		plt.scatter(keysList[i], FRR2_10[keysList[i]] + 0.01, label='skitscat', color='red', s=25, marker="v")
		print("Sell: " + str(keysList[i]))

#title and plot graph
FRR2_10.plot(figsize=(20,10)).axhline(y = 1, color = "black", lw = 1)
plt.title("2-10T Yield Curve")
plt.show()
