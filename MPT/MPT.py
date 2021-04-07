import math
import numpy as np
import pandas as pd
from pandas_datareader import data as pdr
import datetime
from datetime import date
from operator import itemgetter
from wallstreet import Stock
import yfinance as yf
yf.pdr_override()

#initial variables, including dates, portfolio size, number of desired securities in portfolio, and tickers (tickers, port size, # of port securities, and startDate need to be manually adjusted)
endDate = date.today()
startDate = endDate - datetime.timedelta(days = 365 * 2)
tickers = ['MMM', 'ABT', 'ABBV', 'ABMD', 'ACN', 'ATVI', 'ADBE', 'AMD', 'AAP', 'AES', 'AFL', 'A', 'APD', 'AKAM', 'ALK', 'ALB', 'ARE', 'ALXN', 'ALGN', 'ALLE', 'LNT', 'ALL', 'GOOGL', 'GOOG', 'MO', 'AMZN', 'AMCR', 'AEE', 'AAL', 'AEP', 'AXP', 'AIG', 'AMT', 'AWK', 'AMP', 'ABC', 'AME', 'AMGN', 'APH', 'ADI', 'ANSS', 'ANTM', 'AON', 'AOS', 'APA', 'AAPL', 'AMAT', 'APTV', 'ADM', 'ANET', 'AJG', 'AIZ', 'T', 'ATO', 'ADSK', 'ADP', 'AZO', 'AVB', 'AVY', 'BKR', 'BLL', 'BAC', 'BK', 'BAX', 'BDX', 'BBY', 'BIO', 'BIIB', 'BLK', 'BA', 'BKNG', 'BWA', 'BXP', 'BSX', 'BMY', 'AVGO', 'BR', 'CHRW', 'COG', 'CDNS', 'CPB', 'COF', 'CAH', 'KMX', 'CCL', 'CARR', 'CTLT', 'CAT', 'CBOE', 'CBRE', 'CDW', 'CE', 'CNC', 'CNP', 'CERN', 'CF', 'SCHW', 'CHTR', 'CVX', 'CMG', 'CB', 'CHD', 'CI', 'CINF', 'CTAS', 'CSCO', 'C', 'CFG', 'CTXS', 'CLX', 'CME', 'CMS', 'KO', 'CTSH', 'CL', 'CMCSA', 'CMA', 'CAG', 'COP', 'ED', 'STZ', 'COO', 'CPRT', 'GLW', 'CTVA', 'COST', 'CCI', 'CSX', 'CMI', 'CVS', 'DHI', 'DHR', 'DRI', 'DVA', 'DE', 'DAL', 'XRAY', 'DVN', 'DXCM', 'FANG', 'DLR', 'DFS', 'DISCA', 'DISCK', 'DISH', 'DG', 'DLTR', 'D', 'DPZ', 'DOV', 'DOW', 'DTE', 'DUK', 'DRE', 'DD', 'DXC', 'EMN', 'ETN', 'EBAY', 'ECL', 'EIX', 'EW', 'EA', 'EMR', 'ENPH', 'ETR', 'EOG', 'EFX', 'EQIX', 'EQR', 'ESS', 'EL', 'ETSY', 'EVRG', 'ES', 'RE', 'EXC', 'EXPE', 'EXPD', 'EXR', 'XOM', 'FFIV', 'FB', 'FAST', 'FRT', 'FDX', 'FIS', 'FITB', 'FE', 'FRC', 'FISV', 'FLT', 'FLIR', 'FLS', 'FMC', 'F', 'FTNT', 'FTV', 'FBHS', 'BEN', 'FCX', 'GPS', 'GRMN', 'IT', 'GD', 'GE', 'GIS', 'GM', 'GPC', 'GILD', 'GL', 'GPN', 'GS', 'GWW', 'HAL', 'HBI', 'HIG', 'HAS', 'HCA', 'PEAK', 'HSIC', 'HSY', 'HES', 'HPE', 'HLT', 'HFC', 'HOLX', 'HD', 'HON', 'HRL', 'HST', 'HWM', 'HPQ', 'HUM', 'HBAN', 'HII', 'IEX', 'IDXX', 'INFO', 'ITW', 'ILMN', 'INCY', 'IR', 'INTC', 'ICE', 'IBM', 'IP', 'IPG', 'IFF', 'INTU', 'ISRG', 'IVZ', 'IPGP', 'IQV', 'IRM', 'JKHY', 'J', 'JBHT', 'SJM', 'JNJ', 'JCI', 'JPM', 'JNPR', 'KSU', 'K', 'KEY', 'KEYS', 'KMB', 'KIM', 'KMI', 'KLAC', 'KHC', 'KR', 'LB', 'LHX', 'LH', 'LRCX', 'LW', 'LVS', 'LEG', 'LDOS', 'LEN', 'LLY', 'LNC', 'LIN', 'LYV', 'LKQ', 'LMT', 'L', 'LOW', 'LUMN', 'LYB', 'MTB', 'MRO', 'MPC', 'MKTX', 'MAR', 'MMC', 'MLM', 'MAS', 'MA', 'MKC', 'MXIM', 'MCD', 'MCK', 'MDT', 'MRK', 'MET', 'MTD', 'MGM', 'MCHP', 'MU', 'MSFT', 'MAA', 'MHK', 'TAP', 'MDLZ', 'MNST', 'MCO', 'MS', 'MOS', 'MSI', 'MSCI', 'NDAQ', 'NTAP', 'NFLX', 'NWL', 'NEM', 'NWSA', 'NWS', 'NEE', 'NLSN', 'NKE', 'NI', 'NSC', 'NTRS', 'NOC', 'NLOK', 'NCLH', 'NOV', 'NRG', 'NUE', 'NVDA', 'NVR', 'ORLY', 'OXY', 'ODFL', 'OMC', 'OKE', 'ORCL', 'OTIS', 'PCAR', 'PKG', 'PH', 'PAYX', 'PAYC', 'PYPL', 'PNR', 'PBCT', 'PEP', 'PKI', 'PRGO', 'PFE', 'PM', 'PSX', 'PNW', 'PXD', 'PNC', 'POOL', 'PPG', 'PPL', 'PFG', 'PG', 'PGR', 'PLD', 'PRU', 'PEG', 'PSA', 'PHM', 'PVH', 'QRVO', 'PWR', 'QCOM', 'DGX', 'RL', 'RJF', 'RTX', 'O', 'REG', 'REGN', 'RF', 'RSG', 'RMD', 'RHI', 'ROK', 'ROL', 'ROP', 'ROST', 'RCL', 'SPGI', 'CRM', 'SBAC', 'SLB', 'STX', 'SEE', 'SRE', 'NOW', 'SHW', 'SPG', 'SWKS', 'SLG', 'SNA', 'SO', 'LUV', 'SWK', 'SBUX', 'STT', 'STE', 'SYK', 'SIVB', 'SYF', 'SNPS', 'SYY', 'TMUS', 'TROW', 'TTWO', 'TPR', 'TGT', 'TEL', 'FTI', 'TDY', 'TFX', 'TER', 'TSLA', 'TXN', 'TXT', 'TMO', 'TJX', 'TSCO', 'TT', 'TDG', 'TRV', 'TRMB', 'TFC', 'TWTR', 'TYL', 'TSN', 'UDR', 'ULTA', 'USB', 'UAA', 'UA', 'UNP', 'UAL', 'UNH', 'UPS', 'URI', 'UHS', 'UNM', 'VLO', 'VAR', 'VTR', 'VRSN', 'VRSK', 'VZ', 'VRTX', 'VFC', 'VIAC', 'VTRS', 'V', 'VNT', 'VNO', 'VMC', 'WRB', 'WAB', 'WMT', 'WBA', 'DIS', 'WM', 'WAT', 'WEC', 'WFC', 'WELL', 'WST', 'WDC', 'WU', 'WY', 'WHR', 'WMB', 'WLTW', 'WYNN', 'XEL', 'XRX', 'XLNX', 'XYL', 'YUM', 'ZBRA', 'ZBH', 'ZION', 'ZTS']
portfolioSize = 100000.00
portfolioDiversity = 15

#get price data for specified ticker
data = pdr.get_data_yahoo(tickers, start = startDate, end = endDate)
prices = data["Adj Close"].dropna(axis = 'columns')
prices.sort_index(ascending = False, inplace = True)

keysList = prices.keys()
volList = []

#calcuate specific values such as annual volatility and annual return for benchmark such as spy
benchmark = pdr.get_data_yahoo('SPY', start = startDate, end = endDate)
benchmarkPrices = benchmark["Adj Close"]
benchmarkPrices.sort_index(ascending = False, inplace = True)

benchVol = benchmarkPrices.pct_change().apply(lambda x: np.log(1+x))
benchDailyVol = np.std(benchVol)
benchAnnualVol = (benchDailyVol * math.sqrt(len(benchVol))) * 100
benchAnnualReturn = (np.log(benchmarkPrices[0]) - np.log(benchmarkPrices[-1])) * 100
benchRatio = benchAnnualReturn / benchAnnualVol
volList.append(['SPY', benchRatio])

#calcuate specific values such as annual volatility and annual return
for key in keysList:
	vol = prices[key].pct_change().apply(lambda x: np.log(1+x))
	dailyVol = np.std(vol)
	annualVol = (dailyVol * math.sqrt(len(vol))) * 100

	if(annualVol < 75):
		annualReturn = (np.log(prices[key][0]) - np.log(prices[key][-1])) * 100
		ratio = annualReturn / annualVol

		if(ratio > benchRatio):
			volList.append([key, ratio])

#sort list by ratio
sortedList = sorted(volList, key = itemgetter(1), reverse = True)
newTickers = []
benchBool = False

#display results in order from best performing to worst performing securities by annual return adjusted by volatility
for item in sortedList:
	if(str(item[0]) == 'SPY'):
		benchBool = True
	if(len(newTickers) < portfolioDiversity and benchBool == False):
		newTickers.append(str(item[0]))

#get data for list of picked securities
data2 = pdr.get_data_yahoo(newTickers, start = startDate, end = endDate)
prices = data2["Adj Close"]
covMatrix = prices.pct_change().apply(lambda x: np.log(1+x)).cov()
yearlyReturns = prices.resample('Y').last().pct_change().mean()

portRet = [] 
portVol = [] 
portWeights = []
numAssets = len(prices.columns)
numRuns = 100000

#run random weights on covariance matrix to find maximum return on volatility portfolio
for portfolio in range(numRuns):
	weights = np.random.random(numAssets)
	weights = weights / np.sum(weights)
	portWeights.append(weights)
	portRet.append(np.dot(weights, yearlyReturns))
	annualSD = np.sqrt(covMatrix.mul(weights, axis = 0).mul(weights, axis = 1).sum().sum()) * np.sqrt(252)
	portVol.append(annualSD)

newData = {'Returns':portRet, 'Volatility':portVol}
for counter, symbol in enumerate(prices.columns.tolist()):
    newData[symbol] = [w[counter] for w in portWeights]

#get results for ideal portfolio
rf = 0.01
portfolios = pd.DataFrame(newData)
optimalPort = portfolios.iloc[((portfolios['Returns']-rf) / portfolios['Volatility']).idxmax()]
newKeysList = optimalPort.keys()

#print results and metrics
print("\nPortfolio Size = $" + str(portfolioSize))
count = 0
newReturn = 0
newVol = 0

for key in newKeysList:
	if(count == 0):
		newReturn = optimalPort[key]
		print(str(key) + ": " + str(round(optimalPort[key] * 100, 2)) + "%")
		count += 1
	elif(count == 1):
		newVol = optimalPort[key]
		print(str(key) + ": " + str(round(optimalPort[key] * 100, 2)) + "%")
		print("Sharpe Ratio: " + str(round(newReturn / newVol, 2)))
		count += 1
	else:
		percentPort = portfolioSize * optimalPort[key]
		currentPrice = Stock(key).price
		sharesNum = math.floor(percentPort / currentPrice)

		if(count == 2):
			print("")
			count += 1
		
		if(sharesNum > 0):
			print(str(key) + " has a stock price of $" + str(currentPrice))
			print("Buy " + str(sharesNum) + " shares of " + str(key) + " at " + str(round(optimalPort[key] * 100, 2)) + "%")
