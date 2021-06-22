import random
from numpy.random import choice
from matplotlib import pyplot as plt


class VariableActionSet:
    def __init__(self, action_number, reward_rate, penalty_rate):
        self.action_number = action_number
        self.action_probaility = [(1 / action_number)
                                  for i in range(self.action_number)]

        self.reward_rate = reward_rate
        self.penalty_rate = penalty_rate

        self.last_action = 0
        self.last_sub_action_list = None
        self.sub_action_probability = None
        self.sub_action_probability_sum = 0

        self.sum_probability = []
        self.visual_action_probability = [[]
                                          for _ in range(self.action_number)]

    # *****************************************************************************************
    def choose_action(self, sub_action_list):
        self.sub_action_probability_sum = 0
        self.sub_action_probability = [0 for i in range(self.action_number)]  # NOQA : init sub action probability
        self.last_sub_action_list = sub_action_list

        for action in sub_action_list:
            self.sub_action_probability_sum += self.action_probaility[action]

        for action in sub_action_list:
            self.sub_action_probability[action] = self.action_probaility[action] / \
                self.sub_action_probability_sum

        self.last_action = self.__roulette_wheel_selection(
            self.sub_action_probability)

        return self.last_action

    # *****************************************************************************************
    def receive_environment_signal(self, beta):
        self.__update_action_probability(beta)
        self.__rescale_action_probability_vector()

        return

        # *****************************************************************************************
    def visualization_calculations(self):
        self.sum_probability.append(sum(self.action_probaility))

        for action in range(self.action_number):
            self.visual_action_probability[action].append(
                self.action_probaility[action])

    # *****************************************************************************************
    def visualize_sum_probability_data(self, iteration_number):
        x_values = [i for i in range(iteration_number)]

        plt.title('Sum Probability')
        plt.xlabel('iteration')
        plt.ylabel('sum')

        plt.plot(x_values, self.sum_probability)
        plt.show()

        # *****************************************************************************************
    def visualize_action_probability_data(self, iteration_number):
        x_values = [i for i in range(iteration_number)]

        plt.plot(
            x_values, self.visual_action_probability[0], color='r', label='action 0')
        plt.plot(
            x_values, self.visual_action_probability[1], color='b', label='action 1')

        plt.title('Action Probability')
        plt.xlabel('iteration')
        plt.ylabel('probability')

        plt.legend(loc="upper left")

        plt.show()

    # *****************************************************************************************

    def __roulette_wheel_selection(self, probability_list):
        sum = 0
        random_number = random.uniform(0, 1)

        for index, probability in enumerate(probability_list):
            sum += probability

            if random_number <= sum:
                return index

        return probability_list.len() - 1

    # *****************************************************************************************
    def __update_action_probability(self, beta):
        num_of_available_action = sum(
            x != 0 for x in self.sub_action_probability)

        for action in range(len(self.sub_action_probability)):
            if action != self.last_action and self.sub_action_probability[action] != 0:
                self.sub_action_probability[action] = self.sub_action_probability[action] - self.reward_rate * (
                    1 - beta) * self.sub_action_probability[action] + self.penalty_rate * beta * ((1 / (num_of_available_action - 1)) - self.sub_action_probability[action])
            elif action == self.last_action and self.sub_action_probability[action] != 0:
                self.sub_action_probability[action] = self.sub_action_probability[action] + self.reward_rate * (1 - beta) * (
                    1 - self.sub_action_probability[action]) - self.penalty_rate * beta * self.sub_action_probability[action]
        return

    # *****************************************************************************************
    def __rescale_action_probability_vector(self):
        for action in range(len(self.sub_action_probability)):
            if self.sub_action_probability[action] != 0:
                self.action_probaility[action] = self.sub_action_probability[action] * \
                    self.sub_action_probability_sum

        return
