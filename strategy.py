import math
import numpy as np
from scipy.stats import bernoulli
from abc import abstractmethod


class State:
    def __init__(self):
        self.reward_per_coin = [0, 0]
        self.nums = [0, 0]

    def update(self, result, reward):
        self.nums[result] += 1
        self.reward_per_coin[result] += reward

    def get_reward(self):
        return sum(self.reward_per_coin)


class Strategy:
    @abstractmethod
    def __call__(self, state: State):
        pass


class BernoulliStrategy(Strategy):
    def __init__(self, p):
        self.p = p

    def __call__(self, state: State):
        return bernoulli.rvs(self.p, 0)


class GreadyStrategy(Strategy):
    def __init__(self):
        self.prev_reward = 0
        self.reward_per_coin = [0, 0]
        self.prev_n = 0
        self.prev_m = 0
        self.beta = .99

    def compute_ucb1(self, state: State, target):
        s = sum(state.nums)
        k = state.nums[target]
        return state.reward_per_coin[target] / k + self.beta * math.sqrt(2 * math.log(s) / k)

    def __call__(self, state: State):
        if state.nums[0] == 0 or state.nums[1] == 0:
            return bernoulli.rvs(.5, 0)

        return np.argmax([self.compute_ucb1(state, 0), self.compute_ucb1(state, 1)])


def strategy_factory(strategy):
    if strategy.startswith('bernoulli'):
        p = float(strategy.split("_")[1])
        return BernoulliStrategy(p)
    if strategy == 'gready':
        return GreadyStrategy()
    else:
        assert(False)
