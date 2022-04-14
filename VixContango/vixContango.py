from pandas_datareader import data as pdr
from numpy import mean, std
from matplotlib.pyplot import subplots, show
from datetime import date, timedelta
from quandl import get
import yfinance as yf
yf.pdr_override()
apiKey = ""


def main():

    # retrieve data
    vixSpot = getPricesYahoo('^VIX')
    vixFront = getPricesQuandl('CHRIS/CBOE_VX1')
    vixSecond = getPricesQuandl('CHRIS/CBOE_VX2')

    # create ratio for vix
    ratio = ((vixSpot / vixFront) * 0.7) + ((vixFront / vixSecond) * 0.3) - 1
    mu = mean(ratio)
    stdev = std(ratio)
    upperBound = mu + (2.5 * stdev)
    lowerBound = mu - (1.5 * stdev)

    # plot results via matplotlib
    fig, (ax1, ax2) = subplots(2)
    ax1.plot(ratio.keys(), ratio)
    ax1.axhline(y=upperBound, color="green", lw=1)
    ax1.axhline(y=lowerBound, color="red", lw=1)
    ax1.axhline(y=mu, color="black", lw=1)
    ax1.set_title("Contango / Backwardation Ratio")
    ax2.plot(vixSpot.keys(), vixSpot)
    ax2.set_title("VIX Spot Price")
    show()


# query data from for every ticker and parse data (yahoo api)
def getPricesYahoo(tickers):
    data = pdr.get_data_yahoo(tickers, start=date.today(
    ) - timedelta(days=5 * 365), end=date.today())
    prices = data["Adj Close"]
    return prices


# query data from for every ticker and parse data (quandl api)
def getPricesQuandl(tickers):
    data = get(tickers, trim_start=date.today() -
               timedelta(days=5 * 365), trim_end=date.today(), authtoken=apiKey)
    prices = data["Settle"]
    return prices


if __name__ == '__main__':
    main()
