from pykalman import KalmanFilter
import numpy as np
import pandas as pd
from pandas_datareader import data as pdr
import datetime
from datetime import date
import mplfinance as mpf
import yfinance as yf
yf.pdr_override()


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
    spread = pd.Series(spread.flatten(), index=x.index)
    return spread


def regression(x, y):
    x = avg(x)
    y = avg(y)
    filter = KalmanFilter(
        n_dim_obs=1,
        n_dim_state=2,
        initial_state_mean=[0, 0],
        initial_state_covariance=np.ones((2, 2)),
        transition_matrices=np.eye(2),
        observation_matrices=np.expand_dims(
            np.vstack([[x],
                       [np.ones(len(x))]]).T,
            axis=1
        ),
        observation_covariance=2,
        transition_covariance=1e-3 / (1 - 1e-3) * np.eye(2)
    )
    spread, _ = filter.filter(y.values)
    return spread


def plotSpread(ticker1, ticker2, years):
    fig = mpf.figure(figsize=(15, 10))
    axs = fig.add_subplot(1, 1, 1, style='yahoo')

    endDate = date.today()
    startDate = endDate - datetime.timedelta(days=years * 365)
    data1 = pdr.get_data_yahoo(ticker1, start=startDate, end=endDate)
    data2 = pdr.get_data_yahoo(ticker2, start=startDate, end=endDate)
    firstPrice = data1['Adj Close']
    secondPrice = data2['Adj Close']
    df1 = pd.DataFrame({'secondPrice': secondPrice, 'firstPrice': firstPrice})
    df1.index = pd.to_datetime(df1.index)
    state_means = regression(firstPrice, secondPrice)
    df1['hr'] = - state_means[:, 0]
    df1['spread'] = df1.secondPrice + (df1.firstPrice * df1.hr)
    df2 = pd.DataFrame({'Open': df1['spread'].shift(periods=1), 'High': df1['spread'],
                       'Low': df1['spread'], 'Close': df1['spread'], 'Volume': df1['spread']})
    df2 = df2[1:]

    dt = 1
    mu = 0
    theta = 1

    sigma = np.std(df1['spread'])
    ts = np.arange(0, len(df1['spread'].values), dt)
    var = np.array([sigma**2 / (2 * theta) *
                   (1-np.exp(-2 * theta * t)) for t in ts])
    std = 2 * np.sqrt(var)
    std = std[-1]
    upper = mu + std
    lower = mu - std

    mpf.plot(
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
    mpf.show()


ticker1 = "NQ=F"
ticker2 = "ES=F"
years = 2

plotSpread(ticker1, ticker2, years)