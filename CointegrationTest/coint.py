import numpy as np
from pandas_datareader import data as pdr
import datetime
from datetime import date
from operator import itemgetter
from statsmodels.tsa.stattools import coint
import yfinance as yf
yf.pdr_override()


def main():
    # set starting variables (only need to manuably set tickers)
    endDate = date.today()
    startDate = endDate - datetime.timedelta(days=5 * 365)
    tickers = ['SMH', 'ARKK', 'XLK', 'QQQ', 'AAPL', 'MSFT',
               'TSLA', 'ORCL', 'QCOM', 'AMD', 'UBER', 'SQ']

    # get data for each ticker
    data = pdr.get_data_yahoo(tickers, start=startDate, end=endDate)
    prices = data["Adj Close"].dropna(axis='columns')

    # set up data for test
    keysList = prices.keys()
    pValMax = 0.2
    pairsList = []

    print(f"\n{str(len(keysList))} tickers span a valid backtest with {int((len(keysList) * (len(keysList) - 1)) / 2)} possible pair(s).")

    # run cointegration test on all possible pairs
    for i in range(len(keysList)):
        for j in range(i + 1, len(keysList)):
            result = coint(keysList[i], keysList[j])
            pvalue = result[1]

            if(pvalue < pValMax):
                corr = np.corrcoef(keysList[i], keysList[j])
                pairsList.append(
                    (keysList[i], keysList[j], pvalue, corr[0][1]))

    pairsList = sorted(pairsList, key=itemgetter(3), reverse=True)
    print(f"{len(pairsList)} possible cointegrated pairs with p-values less than {str(pValMax)}:")

    # print out valid pairs with sufficient p-value
    for pair in pairsList:
        print(f"\n {pair[0]} and {pair[1]}:")
        print(f"p-value = {round(pair[2], 4)}")
        print(f"correlation coefficient = {round(pair[3], 4)}")


if __name__ == '__main__':
    main()
