from sys import exit
from matplotlib.pyplot import plot, title, show
from numpy import random, mean, std, var, insert, busday_count, log
from datetime import date, timedelta
from pandas_datareader import data as pdr
import yfinance as yf
yf.pdr_override()


def main():
    # initial variables manually entered by user
    ticker, data = getTicker()
    strikeDate = getDate(data.options)
    prices = getPrices(ticker)
    prices.sort_index(ascending=False, inplace=True)

    # variables for simulation
    numDays = busday_count(date.today(), strikeDate) + 1
    numRuns = 10000
    startPrice = data.info['regularMarketPrice']
    dailyVol = std(prices.pct_change().apply(
        lambda x: log(1+x)))
    annualDrift = log(prices[0]) - \
        log(prices[-1])
    dailyDrift = annualDrift / len(prices)
    dailyDriftMean = dailyDrift - (0.5 * dailyVol * dailyVol)

    # get price data for options
    optionData = data.option_chain(strikeDate)
    callsData = optionData.calls
    putsData = optionData.puts

    # display simulation variables
    print(f"Simulation Variables for {ticker}:")
    print(f"Strike Date: {strikeDate}")
    print(f"Days till Expiry: {numDays}")
    print(f"Runs: {numRuns}")
    print(f"Start Price: {round(startPrice, 2)}")
    print(f"Daily Volatility: {round(dailyVol, 6)}")
    print(f"Daily Drift: {round(dailyDriftMean, 6)}", end='\n\n')

    # create 2d array of random daily volatility values and insert starting price
    random.seed(random.randint(1, 10))
    tempSimPrices = random.randn(
        numRuns, numDays) * dailyVol + dailyDriftMean
    simPrices = insert(tempSimPrices, 0, startPrice, axis=1)

    # calculate simulation values from 2d array of random daily volatility values
    for i in range(numRuns):
        for j in range(1, numDays + 1):
            simPrices[i][j] = (simPrices[i][j] + 1) * simPrices[i][j - 1]
    finalPrices = []

    # plot simulation results
    for sim in simPrices:
        plot(sim)
        finalPrices.append(sim[-1])

    # calculate simulation results
    mu = mean(finalPrices)
    sigma = std(finalPrices)
    variance = var(finalPrices)

    # display metrics, plus option values
    print("Normal Distribution of Strikes and Metrics:")
    print(f"μ: {round(mu, 2)}")
    print(f"σ: {round(sigma, 2)}")
    print(f"σ2: {round(variance, 2)}")
    strike(mu, sigma, 3, callsData, True)
    strike(mu, sigma, 2, callsData, True)
    strike(mu, sigma, 1, callsData, True)
    strike(mu, sigma, 0, callsData, True)
    strike(mu, sigma, 0, putsData, False)
    strike(mu, sigma, 1, putsData, False)
    strike(mu, sigma, 2, putsData, False)
    strike(mu, sigma, 3, putsData, False)

    # label and display graph for simulation
    title(ticker)
    show()


# produce stats for given strike
def strike(mean, sigma, multiplier, optionsChain, optionType):
    if(optionType):
        call = mean + (sigma * multiplier)
        callStrike = optionsChain.iloc[(
            optionsChain["strike"]-call).abs().argsort()[:1]]
        print(f"+{multiplier}σ Strike: " + str(callStrike["strike"].item()) + " Call Price: " + str(
            optionsChain["lastPrice"].iloc[callStrike["strike"].index.item()]))
    else:
        put = mean - (sigma * multiplier)
        putStrike = optionsChain.iloc[(
            optionsChain["strike"]-put).abs().argsort()[:1]]
        print(f"-{multiplier}σ Strike: " + str(putStrike["strike"].item()) + " Put Price: " + str(
            optionsChain["lastPrice"].iloc[putStrike["strike"].index.item()]))


# query data for every ticker and parse data
def getPrices(tickers):
    data = pdr.get_data_yahoo(tickers, start=date.today(
    ) - timedelta(days=180), end=date.today())
    prices = data["Adj Close"]
    return prices


# get ticker from user
def getTicker():
    ticker = input("Enter your Ticker: ")
    data = yf.Ticker(ticker)
    if not data.options:
        exit("Invalid Ticker")
    return ticker, data


# get date from user
def getDate(dates):
    for date in dates:
        print(date)
    date = input("Enter your Expiration Date: ")
    if date not in dates:
        exit("Invalid Date")
    return date


if __name__ == '__main__':
    main()
