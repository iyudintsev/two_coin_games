from scipy.stats import bernoulli
from abc import abstractmethod


class Strategy:
    @abstractmethod
    def __call__(self, n, m):
        pass


class BernoulliStrategy(Strategy):
    def __init__(self, p):
        self.p = p

    def __call__(self, n, m):
        return bernoulli.rvs(self.p, 0)


class GreadyStrategy(Strategy):
    def __call__(self, n, m):
        if n == 0 and m == 0:
            return bernoulli.rvs(.5, 0)

        print(n, m, n / (n + m), n / (n + m) < .5)
        return n / (n + m) < .5


def strategy_factory(strategy):
    if strategy.startswith('bernoulli'):
        p = float(strategy.split("_")[1])
        return BernoulliStrategy(p)
    if strategy == 'gready':
        return GreadyStrategy()
    else:
        assert(False)
