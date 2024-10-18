# Kalman Filter-Based Spread Trading Visualization

This Python program calculates and visualizes the spread between two securities, using a **Kalman Filter** to enhance the stationarity of the spread. The spread is then standardized using the **Ornstein-Uhlenbeck variance** to compute the upper and lower bands, which are displayed on a candlestick chart.

The program is useful for traders looking to assess the relationship between two securities and identify mean-reversion opportunities by visualizing how the spread oscillates within a defined range.

## Features

- **Kalman Filter**: Used for regression to calculate the hedge ratio between two securities, making the spread more stationary.
- **Ornstein-Uhlenbeck Process**: Applied to compute the variance and standard deviation of the spread, generating upper and lower Bollinger Bands for visualizing the spread.
- **Candlestick Chart**: Outputs a candlestick chart of the spread with upper, lower, and mean lines to assist in visualizing potential trading signals.

## How It Works

1. **Spread Calculation**: 
   - Retrieves historical price data for two tickers (e.g., `NQ=F` and `ES=F`).
   - Applies a Kalman Filter to calculate a dynamic hedge ratio between the two securities.
   - The spread is calculated as `Spread = Price2 + HedgeRatio * Price1`.

2. **Standardization**: 
   - The spread is standardized using the Ornstein-Uhlenbeck process to calculate the variance and standard deviation of the spread over time.
   - The program computes upper and lower Bollinger Bands based on the mean and variance of the spread.

3. **Visualization**:
   - A candlestick chart is generated with the standardized spread, upper, lower, and mean lines overlaid for easy visualization of mean-reversion opportunities.

## Requirements

Make sure you have the following Python libraries installed:
```
pip install numpy pandas pandas_datareader pykalman yfinance matplotlib mplfinance tqdm opencv-python
```

## Requirements

Make sure you have the following Python libraries installed:

- numpy
- pandas
- pandas_datareader
- pykalman
- yfinance
- matplotlib
- mplfinance
- tqdm
- opencv-python

You can install these libraries by running the following command:

`pip install numpy pandas pandas_datareader pykalman yfinance matplotlib mplfinance tqdm opencv-python`

## Usage

1. Clone this repository and navigate to the project folder:

`git clone https://github.com/hedge0/PyFinance-Projects.git`

`cd PyFinance-Projects/KalmanSpread`

2. Run the program:

`python spreads.py`

3. The program will output a candlestick chart of the spread between the two chosen securities, showing the following:
   - **Candles**: Represent the spread over time.
   - **Mean Line**: The average spread value.
   - **Upper and Lower Bollinger Bands**: Represent two standard deviations from the mean, calculated via the Ornstein-Uhlenbeck process.

## Example Chart

![Kalman Spread Candlestick Chart](https://github.com/hedge0/PyFinance-Projects/blob/main/KalmanSpread/images/spread.PNG?raw=true)

## Customization

- **Securities**: Modify the `ticker1` and `ticker2` variables in the `main()` function to analyze different securities. For example:

`ticker1 = "AAPL"`

`ticker2 = "MSFT"`

- **Time Period**: Adjust the number of years of historical data to retrieve by changing the `years` parameter.

## Potential Use Cases

- **Pairs Trading**: Identify arbitrage opportunities between two correlated securities based on their spread's oscillation around a mean.
- **Mean Reversion Strategies**: Detect when the spread is far from its mean and could potentially revert, providing trade signals.

## Considerations

- **Data Quality**: Ensure the securities you are comparing have a relationship that makes sense for a spread calculation (e.g., similar assets or indices).
- **Mean Reversion**: The Ornstein-Uhlenbeck process assumes mean reversion, so this approach works best for pairs that exhibit such behavior.

## License

This project is open-source and free to use.
