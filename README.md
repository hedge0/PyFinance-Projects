# PyFinance-Projects

A collection of my quantitative finance projects aimed at leveraging Python for advanced financial analysis and trading strategies. These projects encompass a variety of topics, including trading algorithms, statistical analysis, and financial data visualization, with a focus on practical, real-world applications in quantitative finance.

## Project Overview

This repository contains a diverse set of projects designed to help with quantitative finance research and trading automation. Each project focuses on specific aspects of financial markets, including risk management, strategy development, and performance optimization using Python. Below is a list of key projects included:

### 1. Kelly Criterion Bet Sizing Program
   - **Description**: A Goland implementation of the Kelly Criterion, helping users calculate the optimal betting size based on win probability, risk, and reward. It includes Monte Carlo simulations to visualize risk/reward scenarios.
   - **Key Features**:
     - Calculates optimal bet size using the Kelly Criterion.
     - Includes Monte Carlo simulation for scenario analysis.
     - Outputs risk/reward ratios and profitability estimations.

### 2. Kalman Filter-Based Spread Trading
   - **Description**: A program to create and visualize the spread between two correlated assets using Kalman Filter regression. The spread is standardized using Ornstein-Uhlenbeck variance and visualized as a candlestick chart to identify potential mean-reversion opportunities.
   - **Key Features**:
     - Applies a Kalman Filter for hedge ratio calculation.
     - Uses Ornstein-Uhlenbeck variance to standardize the spread.
     - Visualizes spreads on a candlestick chart with Bollinger Bands.

### 3. Candlestick Direction Prediction Using TensorFlow
   - **Description**: A machine learning project aimed at predicting the direction of the next candlestick (up or down) using image classification techniques. TensorFlow is used to train a model based on candlestick chart images categorized as "UP" or "DOWN".
   - **Key Features**:
     - Uses TensorFlow to predict the next candlestick’s direction.
     - Trains a neural network on labeled candlestick chart images.
     - Outputs model accuracy and loss after testing.

## Requirements

Each project in this repository has its own dependencies, which are outlined in the individual project folders. However, many of the projects use common Python libraries for data analysis, visualization, and machine learning. These include:
- `numpy`
- `pandas`
- `matplotlib`
- `yfinance`
- `tensorflow`
- `pykalman`
- `opencv-python`

Make sure to install the necessary dependencies before running any of the projects. You can generally do so using `pip`:

`pip install numpy pandas matplotlib yfinance tensorflow pykalman opencv-python`

## Contributing

Contributions to this collection are welcome! If you have any ideas, improvements, or additional finance-related projects you'd like to add, feel free to open an issue or submit a pull request.
