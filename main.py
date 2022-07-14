import argparse
from strategy import State, Strategy, strategy_factory


class Actor:
    def __init__(self, strategy: Strategy):
        self.strategy = strategy
        self.state = State()

    def get_reward(self):
        return self.state.get_reward()

    def generate(self):
        return self.strategy(self.state)

    def update(self, result, reward):
        self.state.update(result, reward)


class Environment():
    def __init__(self, steps, coin_values, penalty, gen_strategy: Strategy, agent_strategy: Strategy):
        self.steps = steps
        self.coin_values = coin_values
        self.penalty = penalty
        self.gen = Actor(gen_strategy)
        self.agent = Actor(agent_strategy)

    def run(self):
        for _ in range(self.steps):
            coin_gen = self.gen.generate()
            coin_agent = self.agent.generate()
            if coin_gen == coin_agent:
                value = self.coin_values[coin_gen]
                self.gen.update(coin_agent, -value)
                self.agent.update(coin_gen, value)
            else:
                self.gen.update(coin_agent, self.penalty)
                self.agent.update(coin_gen, -self.penalty)

    def get_gen_reward(self):
        return self.gen.get_reward()

    def get_agent_reward(self):
        return self.agent.get_reward()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-steps', dest='steps', type=int)
    parser.add_argument('-coin_value0', dest='coin_value0', type=int)
    parser.add_argument('-coin_value1', dest='coin_value1', type=int)
    parser.add_argument('-penalty', dest='penalty', type=int)
    parser.add_argument('-gen_strategy', dest='gen_strategy', type=str)
    parser.add_argument('-agent_strategy', dest='agent_strategy', type=str)
    args = parser.parse_args()
    gen_strategy = strategy_factory(args.gen_strategy)
    agent_strategy = strategy_factory(args.agent_strategy)
    env = Environment(args.steps, [args.coin_value0, args.coin_value1], args.penalty,
                      gen_strategy, agent_strategy)
    env.run()
    print("Gen reward: {}".format(env.get_gen_reward()))
    print("Agent reward: {}".format(env.get_agent_reward()))


if __name__ == "__main__":
    main()
