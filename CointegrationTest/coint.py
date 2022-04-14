from numpy import corrcoef
from statsmodels.tsa.stattools import coint
from operator import itemgetter
from datetime import date, timedelta
from pandas_datareader import data as pdr
import yfinance as yf
yf.pdr_override()


def main():
    # set tickers to call from yahoo finance api
    tickers = ['SMH', 'ARKK', 'XLK', 'QQQ', 'AAPL', 'MSFT',
               'TSLA', 'ORCL', 'QCOM', 'AMD', 'UBER', 'SQ']
    prices = getPrices(tickers)
    keysList = prices.keys()
    pairsList = []
    print(f"\n{str(len(keysList))} tickers span a valid backtest with {int((len(keysList) * (len(keysList) - 1)) / 2)} possible pair(s).")

    # run cointegration test on all possible pairs
    for i in range(len(keysList)):
        for j in range(i + 1, len(keysList)):
            result = coint(prices[keysList[i]], prices[keysList[j]])
            if(result[1] < 0.25):
                corr = corrcoef(prices[keysList[i]], prices[keysList[j]])
                pairsList.append(
                    (keysList[i], keysList[j], result[1], corr[0][1]))

    pairsList = sorted(pairsList, key=itemgetter(3), reverse=True)
    print(f"{len(pairsList)} possible cointegrated pair(s) with p-value(s) less than {str(0.25)}:")

    # print out valid pairs with sufficient p-value
    for pair in pairsList:
        print(f"\n {pair[0]} and {pair[1]}:")
        print(f"p-value = {round(pair[2], 4)}")
        print(f"correlation coefficient = {round(pair[3], 4)}")


# query data for every ticker and parse data
def getPrices(tickers):
    prices = pdr.get_data_yahoo(tickers, start=date.today(
    )-timedelta(days=5*365), end=date.today())["Adj Close"].dropna(axis='columns')
    return prices


if __name__ == '__main__':
    main()
