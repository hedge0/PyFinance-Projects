from pykalman import KalmanFilter
from numpy import ones, eye, expand_dims, vstack, std, arange, array, exp, sqrt
from pandas import DataFrame, Series, to_datetime
from pandas_datareader import data as pdr
from datetime import date, timedelta
from mplfinance import figure, plot, show
import yfinance as yf
yf.pdr_override()

def main():
    """
    Main function to plot the spread between two tickers.
    """
    ticker1 = "NQ=F"
    ticker2 = "ES=F"
    years = 2
    plot_spread(ticker1, ticker2, years)


def plot_spread(ticker1, ticker2, years, dt=1, mu=0, theta=1):
    """
    Plots the stationary spread between two tickers using Kalman Filter regression.

    Args:
        ticker1 (str): The first ticker symbol.
        ticker2 (str): The second ticker symbol.
        years (int): Number of years of historical data to retrieve.
        dt (int): Time step for plotting.
        mu (float): Mean of the spread.
        theta (float): Mean-reversion speed for calculating variance.
    """
    fig, ax = create_figure()

    first_price = get_prices(ticker1, years)
    second_price = get_prices(ticker2, years)

    spread_data = compute_spread(first_price, second_price)

    df2 = prepare_candlestick_data(spread_data)

    upper, lower = calculate_bollinger_bands(spread_data, mu, theta, dt)

    plot_candlestick_chart(df2, ax, ticker1, ticker2, mu, upper, lower)
    show()


def create_figure():
    """
    Creates a figure for plotting with specific settings.
    
    Returns:
        matplotlib.figure.Figure: The figure for plotting.
        matplotlib.axes.Axes: The axis for the plot.
    """
    fig = figure(figsize=(15, 10))
    ax = fig.add_subplot(1, 1, 1, style='yahoo')
    return fig, ax


def get_prices(ticker, years):
    """
    Retrieves historical prices for a given ticker.

    Args:
        ticker (str): The ticker symbol.
        years (int): Number of years of data to retrieve.

    Returns:
        pandas.Series: Adjusted closing prices for the ticker.
    """
    start_date = date.today() - timedelta(days=years * 365)
    end_date = date.today()
    prices = pdr.get_data_yahoo(ticker, start=start_date, end=end_date)["Adj Close"]
    return prices


def compute_spread(first_price, second_price):
    """
    Computes the spread between two price series using Kalman Filter regression.

    Args:
        first_price (pandas.Series): Price series for the first asset.
        second_price (pandas.Series): Price series for the second asset.

    Returns:
        pandas.DataFrame: DataFrame containing spread and hedge ratio.
    """
    state_means = regression(first_price, second_price)
    hedge_ratio = -state_means[:, 0]

    df = DataFrame({
        'secondPrice': second_price,
        'firstPrice': first_price,
        'hr': hedge_ratio
    })

    df.index = to_datetime(df.index)
    df['spread'] = df.secondPrice + (df.firstPrice * df.hr)
    return df


def prepare_candlestick_data(df):
    """
    Prepares candlestick chart data from the spread data.

    Args:
        df (pandas.DataFrame): DataFrame containing spread data.

    Returns:
        pandas.DataFrame: Data formatted for candlestick chart plotting.
    """
    df2 = DataFrame({
        'Open': df['spread'].shift(periods=1),
        'High': df['spread'],
        'Low': df['spread'],
        'Close': df['spread'],
        'Volume': df['spread']
    })
    return df2[1:]  # Skip the first row due to the shift


def calculate_bollinger_bands(df, mu, theta, dt):
    """
    Calculates the upper and lower Bollinger Bands for the spread.

    Args:
        df (pandas.DataFrame): DataFrame containing spread data.
        mu (float): Mean of the spread.
        theta (float): Mean-reversion speed for variance.
        dt (int): Time step for the plot.

    Returns:
        tuple: The upper and lower Bollinger Bands.
    """
    sigma = std(df['spread'])
    ts = arange(0, len(df['spread'].values), dt)
    var = array([sigma ** 2 / (2 * theta) * (1 - exp(-2 * theta * t)) for t in ts])
    stdev = 2 * sqrt(var)[-1]
    upper = mu + stdev
    lower = mu - stdev
    return upper, lower


def plot_candlestick_chart(df, ax, ticker1, ticker2, mu, upper, lower):
    """
    Plots the candlestick chart with Bollinger Bands.

    Args:
        df (pandas.DataFrame): DataFrame containing candlestick data.
        ax (matplotlib.axes.Axes): The axis to plot on.
        ticker1 (str): The first ticker symbol.
        ticker2 (str): The second ticker symbol.
        mu (float): Mean of the spread.
        upper (float): Upper Bollinger Band.
        lower (float): Lower Bollinger Band.
    """
    plot(
        df,
        type='candle',
        ax=ax,
        axtitle=f"Spread for {ticker2} / {ticker1}",
        hlines=dict(
            hlines=[mu, upper, lower],
            linestyle='-.',
            colors=['b', 'b', 'b']
        ),
        xrotation=0
    )


def avg(x):
    """
    Applies a Kalman Filter to smooth the price series.

    Args:
        x (pandas.Series): Price series.

    Returns:
        pandas.Series: Smoothed price series.
    """
    kf = KalmanFilter(
        transition_matrices=[1],
        observation_matrices=[1],
        initial_state_mean=0,
        initial_state_covariance=1,
        observation_covariance=1,
        transition_covariance=0.01
    )
    smoothed, _ = kf.filter(x.values)
    return Series(smoothed.flatten(), index=x.index)


def regression(x, y):
    """
    Performs Kalman Filter regression on two price series.

    Args:
        x (pandas.Series): First price series.
        y (pandas.Series): Second price series.

    Returns:
        numpy.ndarray: State means from the Kalman Filter regression.
    """
    x_smoothed = avg(x)
    y_smoothed = avg(y)

    observation_matrices = expand_dims(vstack([x_smoothed, ones(len(x_smoothed))]).T, axis=1)

    kf = KalmanFilter(
        n_dim_obs=1,
        n_dim_state=2,
        initial_state_mean=[0, 0],
        initial_state_covariance=ones((2, 2)),
        transition_matrices=eye(2),
        observation_matrices=observation_matrices,
        observation_covariance=2,
        transition_covariance=1e-3 / (1 - 1e-3) * eye(2)
    )

    state_means, _ = kf.filter(y_smoothed.values)
    return state_means


if __name__ == '__main__':
    main()
