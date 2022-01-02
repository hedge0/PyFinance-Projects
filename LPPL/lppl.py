from lppls import lppls
import numpy as np
import pandas as pd
from pandas_datareader import data as pdr
from datetime import timedelta, date
from matplotlib import pyplot as plt
import yfinance as yf
yf.pdr_override()


def main():
    ticker = 'BTC-USD'
    endDate = date.today()
    startDate = endDate - timedelta(days=4 * 365)
    data = pdr.get_data_yahoo(ticker, start=startDate, end=endDate)
    time = [pd.Timestamp.toordinal(t1) for t1 in data.index]
    price = np.log(data['Adj Close'].values)
    observations = np.array([time, price])
    lppls_model = lppls.LPPLS(observations=observations)

    res = lppls_model.mp_compute_nested_fits(
        workers=8,
        window_size=120,
        smallest_window_size=30,
        outer_increment=1,
        inner_increment=5,
        max_searches=25
    )

    lppls_model.plot_confidence_indicators(res)
    plt.show()


if __name__ == '__main__':
    main()
