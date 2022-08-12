# first strategy by using Sirer Aritcla published in 2014
import sys
import os
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

import random  # NOQA
from matplotlib import pyplot as plt  # NOQA


class SelfishMiningOne:
    def __init__(self, show_log=False):
        self._alpha = 0
        self._gamma = 0

        self.__show_log = show_log

        random.seed(None)

        self.__public_chain_length = 0
        self.__private_chain_length = 0
        self.__delta = 0

        self.__selfish_miners_win_block = 0
        self.__honest_miners_win_block = 0

        self.__selfish_miner_revenue = 0
        self.__honest_miner_revenue = 0

        self.__total_mined_block = 0
        self.__total_stale_block = 0

        self.__iteration_number = 0

    @property
    def alpha(self):
        return self._alpha

    @alpha.setter
    def alpha(self, value):
        if value < 0 or value > 0.5:
            raise Exception("invalid value for alpha!")

        self._alpha = value

        return

    @property
    def gamma(self):
        return self._gamma

    @gamma.setter
    def gamma(self, value):
        if value < 0 or value > 1:
            raise Exception("invalid value for gamma!")

        self._gamma = value

        return

    @property
    def revenue(self):
        return self.__selfish_miner_revenue

    @property
    def stale_block(self):
        return self.__total_stale_block

    def print_input_statistic(self):
        print('alpha is : {}'.format(self._alpha))
        print('gamma is : {}'.format(self._gamma))

        return

    def start_simulate(self, iteration):
        self.log('start simulating')

        self.__iteration_number = iteration

        for i in range(iteration):
            self.log("found a new block")

            random_number = random.random()

            self.calculating_delta()

            # Mining Process
            if random_number < self._alpha:
                self.start_selfish_mining()
            else:
                self.start_honest_mining()

        self.calculating_output()

        return

    def start_selfish_mining(self):
        self.log('starting selfish mining!')

        self.__private_chain_length += 1

        if self.__delta == 0 and self.__private_chain_length == 2:
            # print('1')
            self.__selfish_miners_win_block += 2
            self.__private_chain_length = 0
            self.__public_chain_length = 0

        return

    def start_honest_mining(self):
        self.log('starting honest mining!')

        self.__public_chain_length += 1

        if self.__delta == 0 and self.__private_chain_length == 0:
            # print('2')
            self.__honest_miners_win_block += 1
            self.__private_chain_length = 0
            self.__public_chain_length = 0

        elif self.__delta == 0 and self.__private_chain_length == 1:
            # print('3')
            gamma_random = random.random()

            if gamma_random < self.gamma:
                self.__selfish_miners_win_block += 1
                self.__honest_miners_win_block += 1
                self.__private_chain_length = 0
                self.__public_chain_length = 0
            else:
                self.__honest_miners_win_block += 2
                self.__private_chain_length = 0
                self.__public_chain_length = 0

        elif self.__delta == 1:
            # print('4')
            # nothing to do...another state define result of this state
            return

        elif self.__delta == 2:
            # print('5')
            self.__selfish_miners_win_block += self.__private_chain_length
            self.__public_chain_length = 0
            self.__private_chain_length = 0

        elif self.__delta > 2:
            # print('6')
            # nothing to do...another state define result of this state
            return

        return

    def calculating_delta(self):
        self.__delta = self.__private_chain_length - self.__public_chain_length
        self.log('delta is : {}'.format(self.__delta))

        return

    def calculating_output(self):
        self.__total_mined_block = self.__honest_miners_win_block + \
            self.__selfish_miners_win_block
        self.__total_stale_block = self.__iteration_number - self.__total_mined_block

        self.__honest_miner_revenue = float(
            self.__honest_miners_win_block / self.__total_mined_block) * 100
        self.__selfish_miner_revenue = float(
            self.__selfish_miners_win_block / self.__total_mined_block) * 100

        return

    def print_final_result(self):

        print('********************************************')

        self.print_input_statistic()

        print('honest miners win block is : {}'.format(
            self.__honest_miners_win_block))
        print('selfish miners win block is : {}'.format(
            self.__selfish_miners_win_block))

        print('total mined block is : {}'.format(self.__total_mined_block))
        print('total stale block is : {}'.format(self.__total_stale_block))

        print('honest miner revenue is : {}'.format(
            self.__honest_miner_revenue))
        print('selfish miner revenue is : {}'.format(
            self.__selfish_miner_revenue))

        print('honest miner expected reward is : {}'.format(
            (1 - self.alpha) * self.__iteration_number * 100 / self.__iteration_number))
        print('selfish miner expected reward is : {}'.format(
            (self.alpha) * self.__iteration_number * 100 / self.__iteration_number))

        print('********************************************')

        return

    def log(self, log_message):
        if self.__show_log:
            print(log_message)

        return

    def reset(self):
        random.seed(None)

        self.__public_chain_length = 0
        self.__private_chain_length = 0
        self.__delta = 0

        self.__selfish_miners_win_block = 0
        self.__honest_miners_win_block = 0

        self.__selfish_miner_revenue = 0
        self.__honest_miner_revenue = 0

        self.__total_mined_block = 0
        self.__total_stale_block = 0

        self.__iteration_number = 0

        return

    def visualize_data(self, iteration_number):
        alpha_values = [x / 100 for x in range(51) if x % 5 == 0]
        selfish_revenue_value_0 = []
        selfish_revenue_value_0_5 = []
        selfish_revenue_value_1 = []
        honest_revenue_value = []

        for alpha in alpha_values:
            self.alpha = alpha
            self.gamma = 0
            self.start_simulate(iteration_number)
            self.print_final_result()
            selfish_revenue_value_0.append(self.__selfish_miner_revenue)

            self.reset()

        for alpha in alpha_values:
            self.alpha = alpha
            self.gamma = 0.5
            self.start_simulate(iteration_number)
            self.print_final_result()
            selfish_revenue_value_0_5.append(self.__selfish_miner_revenue)

            self.reset()

        for alpha in alpha_values:
            self.alpha = alpha
            self.gamma = 1
            self.start_simulate(iteration_number)
            self.print_final_result()
            selfish_revenue_value_1.append(self.__selfish_miner_revenue)

            self.reset()

        for alpha in alpha_values:
            honest_revenue_value.append(alpha * 100)

        plt.plot(
            alpha_values, selfish_revenue_value_0, color='r', label='gamma = 0')
        plt.plot(
            alpha_values, selfish_revenue_value_0_5, color='y', label='gamma = 0.5')
        plt.plot(
            alpha_values, selfish_revenue_value_1, color='g', label='gamma = 1')

        plt.plot(alpha_values, honest_revenue_value,
                 color='k', label='honest mining')

        plt.title('Selfish Mining')
        plt.xlabel('Pool size')
        plt.ylabel('Relative Revenue')

        plt.legend(loc="upper left")

        plt.show()
