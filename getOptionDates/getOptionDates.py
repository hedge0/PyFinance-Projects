import numpy as np
import pandas as pd
from pandas_datareader import data as pdr
import datetime
from datetime import date
import yfinance as yf
yf.pdr_override()

today = date.today()
ticker = 'SPY'

data = yf.Ticker(ticker)
dates = data.options
print(dates)