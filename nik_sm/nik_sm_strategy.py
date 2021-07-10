import sys
import os
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

import random  # NOQA
from matplotlib import pyplot as plt  # NOQA

# Nik Defense
from nik_sm.block_creation_status import BlockCreationStatus  # NOQA
from nik_sm.time_window import TimeWindow  # NOQA
from nik_sm.learning_automata.variable_action_set import VariableActionSet  # NOQA


class NikSelfishMining:
    def __init__(self, tow_number, min_tow_block_number, max_tow_block_number,
                 reward_rate, penalty_rate, min_k, max_k, show_log=False):
        self._alpha = 0
        self._gamma = 0

        self.weight_size = 10000

        self.__tow_number = tow_number
        self.__min_tow_block_number = min_tow_block_number
        self.__max_tow_block_number = max_tow_block_number

        self.time_window = TimeWindow(
            tow_number, min_tow_block_number, max_tow_block_number)

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

        self.__predicted_K = 2

        self.__private_chain_weight_list = [
            0 for _ in range(self.weight_size)]
        self.__public_chain_weight_list = [
            0 for _ in range(self.weight_size)]

        self.__private_chain_weight = 0
        self.__public_chain_weight = 0

        self.__current_block_tow = 1

        self.min_K = min_k
        self.max_K = max_k

        self.__weight_decision = False
        self.__weight_decision_number = 0

        self.__reward_rate = reward_rate
        self.__penalty_rate = penalty_rate

        self.vasla = VariableActionSet(
            3, self.__reward_rate, self.__penalty_rate)
        self.__first_la_decision = True

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
        # self.log('start simulating')

        self.__iteration_number = iteration

        for _ in range(iteration):
            # self.log("found a new block")

            self.calculating_delta()

            random_number = random.random()

            # Mining Process
            if random_number < self._alpha:
                self.calculating_weight(True)
                self.start_selfish_mining()
            else:
                self.calculating_weight(False)
                self.start_honest_mining()

            block_creation_response = self.time_window.create_a_block()
            if block_creation_response == BlockCreationStatus.EndTow:
                # self.chain_evaluation()
                # self.reset_tow()

                if self.__weight_decision == True:
                    self.__weight_decision_number += 1
                    self.__weight_decision = False

                self.__current_block_tow = 1
            elif block_creation_response == BlockCreationStatus.EndTimeWindow:
                self.time_window = TimeWindow(
                    self.__tow_number, self.__min_tow_block_number, self.__max_tow_block_number)
                # self.chain_evaluation()
                # self.reset_tow()

                self.learning_automata_decision()
                self.__first_la_decision = False

                self.__current_block_tow = 1
            else:
                self.__current_block_tow += 1

        self.calculating_output()

        return

    def start_selfish_mining(self):
        # self.log('starting selfish mining!')

        self.__private_chain_length += 1

        if self.__delta == 0 and self.__private_chain_length == 2:
            self.chain_evaluation()
            self.reset_attack()

        return

    def start_honest_mining(self):
        # self.log('starting honest mining!')

        self.__public_chain_length += 1

        if self.__delta == 0 and self.__private_chain_length == 0:
            self.chain_evaluation()
            self.reset_attack()

        elif self.__delta == 0 and self.__private_chain_length == 1:
            self.chain_evaluation()
            self.reset_attack()

        elif self.__delta == 1 or self.__delta == 2:
            self.chain_evaluation()
            self.reset_attack()

        elif self.__delta == self.__predicted_K + 1:
            self.chain_evaluation()
            self.reset_attack()

        elif self.__delta > self.__predicted_K + 1:
            pass

        return

    def calculating_delta(self):
        self.__delta = self.__private_chain_length - self.__public_chain_length
        # self.log('delta is : {}'.format(self.__delta))

        return

    def calculating_weight(self, is_private_block):
        if is_private_block:
            self.__private_chain_weight_list[self.__private_chain_length] = 1
            self.__public_chain_weight_list[self.__private_chain_length] = 0
        else:
            self.__private_chain_weight_list[self.__public_chain_length] = 0
            self.__public_chain_weight_list[self.__public_chain_length] = 1
            pass

        return

    def chain_evaluation(self):
        if self.__private_chain_length - self.__public_chain_length >= self.__predicted_K:
            # Decision based on Length
            self.__selfish_miners_win_block += self.__private_chain_length
        elif self.__public_chain_length - self.__private_chain_length >= self.__predicted_K:
            # Decision based on Length
            self.__honest_miners_win_block += self.__public_chain_length
        else:
            self.__weight_decision = True

            # Decision based on Wight
            self.__private_chain_weight = sum(self.__private_chain_weight_list)
            self.__public_chain_weight = sum(self.__public_chain_weight_list)

            if self.__private_chain_weight > self.__public_chain_weight:
                self.__selfish_miners_win_block += self.__private_chain_length
            elif self.__public_chain_weight > self.__private_chain_weight:
                self.__honest_miners_win_block += self.__public_chain_length
            else:
                random_number = random.random()
                if random_number < self.gamma:
                    self.__selfish_miners_win_block += self.__private_chain_length
                else:
                    self.__honest_miners_win_block += self.__public_chain_length

        return

    def learning_automata_decision(self):
        if not self.__first_la_decision:
            beta = 1 - (self.__weight_decision_number / self.__tow_number)
            self.vasla.receive_environment_signal(beta)

        self.__weight_decision_number = 0

        chosen_action = 0
        if self.__predicted_K == self.min_K:
            chosen_action = self.vasla.choose_action([0, 1])
        elif self.__predicted_K == self.max_K:
            chosen_action = self.vasla.choose_action([1, 2])
        else:
            chosen_action = self.vasla.choose_action([0, 1, 2])

        if chosen_action == 0:
            # Grow
            self.__predicted_K += 1
        elif chosen_action == 1:
            # Stop
            pass
        elif chosen_action == 2:
            # Shrink
            self.__predicted_K -= 1

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

        print('Nik honest miners win block is : {}'.format(
            self.__honest_miners_win_block))
        print('Nik selfish miners win block is : {}'.format(
            self.__selfish_miners_win_block))

        print('Nik total mined block is : {}'.format(self.__total_mined_block))
        print('Nik total stale block is : {}'.format(self.__total_stale_block))

        print('Nik honest miner revenue is : {}'.format(
            self.__honest_miner_revenue))
        print('Nik selfish miner revenue is : {}'.format(
            self.__selfish_miner_revenue))

        print('Nik honest miner expected reward is : {}'.format(
            (1 - self.alpha) * self.__iteration_number * 100 / self.__iteration_number))
        print('Nik selfish miner expected reward is : {}'.format(
            (self.alpha) * self.__iteration_number * 100 / self.__iteration_number))

        print('********************************************')

        return

    def log(self, log_message):
        if self.__show_log:
            print(log_message)

        return

    def reset_tow(self):
        self.__private_chain_weight_list = [
            0 for _ in range(self.weight_size)]
        self.__public_chain_weight_list = [
            0 for _ in range(self.weight_size)]

        self.__current_block_tow = 1

        self.__private_chain_weight = 0
        self.__public_chain_weight = 0

        self.__private_chain_length = 0
        self.__public_chain_length = 0

    def reset_attack(self):
        self.__private_chain_weight_list = [
            0 for _ in range(self.weight_size)]
        self.__public_chain_weight_list = [
            0 for _ in range(self.weight_size)]

        self.__private_chain_weight = 0
        self.__public_chain_weight = 0

        self.__private_chain_length = 0
        self.__public_chain_length = 0

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

        self.time_window = TimeWindow(
            self.__tow_number, self.__min_tow_block_number, self.__max_tow_block_number)

        self.__private_chain_weight_list = [
            0 for _ in range(self.weight_size)]
        self.__public_chain_weight_list = [
            0 for _ in range(self.weight_size)]

        self.__private_chain_weight = 0
        self.__public_chain_weight = 0

        self.__current_block_tow = 1

        self.__predicted_K = 2

        self.__weight_decision = False
        self.__weight_decision_number = 0

        self.vasla = VariableActionSet(
            3, self.__reward_rate, self.__penalty_rate)
        self.__first_la_decision = True

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

        plt.title('Nik Selfish Mining')
        plt.xlabel('Pool size')
        plt.ylabel('Relative Revenue')

        plt.legend(loc="upper left")

        plt.show()
