from sys import exit
from random import random
from numpy import mean, std
from collections import deque


class Kelly:

    def __init__(self, probability, risk, reward, runs):
        self.probability = self._check_float(probability)
        self.risk = self._check_float(risk)
        self.reward = self._check_float(reward)
        self.runs = self._check_int(runs)
        self.ratio = self.reward / self.risk
        self.kelly = self.probability - ((1 - self.probability) / self.ratio)
        self.results = None
        self.mean = None
        self.sigma = None
        self.walks = None

    # check that string can be converted to float
    def _check_float(self, val):
        try:
            float(val)
        except ValueError:
            exit("Not a Float")
        return float(val)

    # check that string can be converted to int
    def _check_int(self, val):
        try:
            int(val)
        except ValueError:
            exit("Not an Int")
        return int(val)

    # compute new value for random walk
    def _total_val(self, prev, val):
        if random() < self.probability:
            totalVal = (1 + self.reward) * (val * prev) + (1 - val) * prev
        else:
            totalVal = (1 - self.risk) * (val * prev) + (1 - val) * prev
        return totalVal

    # get percent of random walks that were profitable
    def _get_profitable_walks(self, results):
        return len(list(filter(lambda x: x > 1, results))) / len(results)

    # run simulation equal to number of random walks
    def run_monte_carlo(self, val, iterations):
        if val < 0:
            exit("Bet size is less than 0")
        results = []
        for i in range(iterations):
            randomWalk = deque()
            randomWalk.append(1)
            for i in range(1, self.runs + 1):
                randomWalk.append(self._total_val(randomWalk[i-1], val))
            results.append(randomWalk[-1])
        self.results = results
        self.mean = mean(results)
        self.sigma = std(results)
        self.walks = self._get_profitable_walks(results)

    # get probability
    def get_probability(self):
        return self.probability

    # get risk
    def get_risk(self):
        return self.risk

    # get reward
    def get_reward(self):
        return self.reward

    # get number of runs
    def get_runs(self):
        return self.runs

    # get ratio
    def get_ratio(self):
        return self.ratio

    # get kelly
    def get_kelly(self):
        return self.kelly

    # get mean
    def get_mean(self):
        return self.mean

    # get sigma
    def get_sigma(self):
        return self.sigma

    # get walks
    def get_walks(self):
        return self.walks
