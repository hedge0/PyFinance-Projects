from mpt import MPT

def main():
    tickers = ['MSFT', 'TSLA', 'AMZN', 'AAPL']
    sim = MPT(tickers, 2)
    sim.runSimulation(10000)
    print(f"Annualized Returns: {round(sim.getReturn() * 100, 2)}%")
    print(f"Annualized Volatility: {round(sim.getVolatility() * 100, 2)}%")
    print(f"Sharpe Ratio: {round(sim.getSharpe(), 2)}\n")
    portfolio = sim.getPortfolio()
    for ticker in portfolio:
        print(f"{ticker} requires {round(portfolio[ticker] * 100, 2)}% allocation")


if __name__ == '__main__':
    main()