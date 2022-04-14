from pykalman import KalmanFilter
from numpy import ones, eye, expand_dims, vstack, std, arange, array, exp, sqrt
from pandas import DataFrame, Series, to_datetime
from pandas_datareader import data as pdr
from datetime import date, timedelta
from mplfinance import figure, plot, show
import yfinance as yf
yf.pdr_override()


def main():
    plotSpread("NQ=F", "ES=F", 2)


def plotSpread(ticker1, ticker2, years, dt=1, mu=0, theta=1):
    fig = figure(figsize=(15, 10))
    axs = fig.add_subplot(1, 1, 1, style='yahoo')
    firstPrice = getPrices(ticker1, years)
    secondPrice = getPrices(ticker2, years)
    df1 = DataFrame({'secondPrice': secondPrice, 'firstPrice': firstPrice})
    df1.index = to_datetime(df1.index)
    state_means = regression(firstPrice, secondPrice)
    df1['hr'] = - state_means[:, 0]
    df1['spread'] = df1.secondPrice + (df1.firstPrice * df1.hr)
    df2 = DataFrame({'Open': df1['spread'].shift(periods=1), 'High': df1['spread'],
                     'Low': df1['spread'], 'Close': df1['spread'], 'Volume': df1['spread']})
    df2 = df2[1:]
    sigma = std(df1['spread'])
    ts = arange(0, len(df1['spread'].values), dt)
    var = array([sigma**2 / (2 * theta) *
                 (1-exp(-2 * theta * t)) for t in ts])
    stdev = 2 * sqrt(var)
    stdev = stdev[-1]
    upper = mu + stdev
    lower = mu - stdev
    plot(
        df2,
        type='candle',
        ax=axs,
        axtitle=f"Spread for {ticker2} / {ticker1}",
        hlines=dict(
            hlines=[mu, upper, lower],
            linestyle='-.',
            colors=['b', 'b', 'b']
        ),
        xrotation=0
    )
    show()


# query data for every ticker and parse data
def getPrices(tickers, years):
    data = pdr.get_data_yahoo(tickers, start=date.today(
    ) - timedelta(days=years * 365), end=date.today())
    prices = data["Adj Close"]
    return prices


def avg(x):
    filter = KalmanFilter(
        transition_matrices=[1],
        observation_matrices=[1],
        initial_state_mean=0,
        initial_state_covariance=1,
        observation_covariance=1,
        transition_covariance=.01
    )
    spread, _ = filter.filter(x.values)
    spread = Series(spread.flatten(), index=x.index)
    return spread


def regression(x, y):
    x = avg(x)
    y = avg(y)
    filter = KalmanFilter(
        n_dim_obs=1,
        n_dim_state=2,
        initial_state_mean=[0, 0],
        initial_state_covariance=ones((2, 2)),
        transition_matrices=eye(2),
        observation_matrices=expand_dims(
            vstack([[x],
                    [ones(len(x))]]).T,
            axis=1
        ),
        observation_covariance=2,
        transition_covariance=1e-3 / (1 - 1e-3) * eye(2)
    )
    spread, _ = filter.filter(y.values)
    return spread


if __name__ == '__main__':
    main()
