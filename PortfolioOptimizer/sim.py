from mpt import MPT

def main():
    tickers = ['MSFT', 'TSLA', 'AMZN', 'AAPL']
    sim = MPT(tickers, 2)
    sim.runSimulation(10000)
    print(sim.getPortfolio())


if __name__ == '__main__':
    main()