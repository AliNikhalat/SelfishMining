import random
from numpy.random import choice
from matplotlib import pyplot as plt

# import sys
# import os
# sys.path.insert(0, os.path.abspath(
#     os.path.join(os.path.dirname(__file__), '..')))

from learning_automata.variable_action_set import VariableActionSet  # NOQA


class SymmetricVariableDepthHybrid:
    def __init__(self, action_number, state_number, reward_rate, penalty_rate, max_state_number):
        self.fsla_action_number = action_number
        self.fsla_state_number = state_number

        self.fsla_chosen_action = 0
        self.fsla_chosen_action_depth_status = 0
        self.fsla_state_transition_counter = 0
        self.fsla_depth_transition_counter = 0
        self.fsla_min_state = 1
        self.fsla_max_state = max_state_number

        ''' 
            grow --> Action 0
            stop --> Action 1
            shrink --> Action 2
        '''
        self.variable_action_set_action_number = 3
        self.variable_action_set = VariableActionSet(
            self.variable_action_set_action_number, reward_rate, penalty_rate)
        self.variable_action_set_first_run = True

        self.total_number_of_rewards = []
        self.total_number_of_action_switching = []

        self.action_selection_status = [[]
                                        for _ in range(self.fsla_action_number)]

    # *****************************************************************************************
    def choose_action(self, sub_action_list):
        self.__action_switching_by_scaling(sub_action_list)

        return self.fsla_chosen_action

    # *****************************************************************************************
    def choose_random_action(self):
        # Choose random action for first running
        self.chosen_action = random.randint(0, self.fsla_action_number-1)
        self.fsla_chosen_action_depth_status = 1

        return self.fsla_chosen_action

    # *****************************************************************************************
    def receive_environment_signal(self, beta):
        if beta == 1:
            self.__punish_automata()
            self.total_number_of_rewards.append(
                0 + self.total_number_of_rewards[-1] if len(self.total_number_of_rewards) > 0 else 0)
        else:
            self.__suprise_automata()

            self.total_number_of_rewards.append(
                1 + self.total_number_of_rewards[-1] if len(self.total_number_of_rewards) > 0 else 1)
            self.total_number_of_action_switching.append(
                0 + self.total_number_of_action_switching[-1] if len(self.total_number_of_action_switching) > 0 else 0)
        return

    # *****************************************************************************************
    def visualization_calculations(self):
        for action in range(self.fsla_action_number):
            if action == self.fsla_chosen_action:
                self.action_selection_status[action].append(
                    1 + self.action_selection_status[action][-1] if len(self.action_selection_status[action]) > 0 else 1)
            else:
                self.action_selection_status[action].append(
                    0 + self.action_selection_status[action][-1] if len(self.action_selection_status[action]) > 0 else 0)

    # *****************************************************************************************
    @property
    def get_total_number_of_rewards(self):
        return self.total_number_of_rewards

    # *****************************************************************************************
    @property
    def get_total_number_of_action_switching(self):
        return self.total_number_of_action_switching

    # *****************************************************************************************
    def get_action_selection_status(self, action_number):
        return self.action_selection_status[action_number]

    # *****************************************************************************************
    def __suprise_automata(self):
        if self.fsla_chosen_action_depth_status < self.fsla_state_number:
            self.fsla_chosen_action_depth_status += 1

        self.fsla_state_transition_counter += 1
        if self.__is_fsla_on_depth():
            self.fsla_depth_transition_counter += 1

        return

    # *****************************************************************************************
    def __punish_automata(self):
        if self.fsla_chosen_action_depth_status > 1:
            self.fsla_chosen_action_depth_status -= 1

            self.fsla_state_transition_counter += 1

            self.total_number_of_action_switching.append(
                0 + self.total_number_of_action_switching[-1] if len(self.total_number_of_action_switching) > 0 else 0)
        else:
            if not self.variable_action_set_first_run:
                self.__evaluate_variable_action_set()
            else:
                self.variable_action_set_first_run = False

            self.__action_switching()

        return

    # *****************************************************************************************
    def __is_fsla_on_depth(self):
        return self.fsla_chosen_action_depth_status == self.fsla_state_number

    # *****************************************************************************************
    def __choose_new_action_clockwise(self):
        if self.fsla_chosen_action < self.fsla_action_number - 1:
            self.fsla_chosen_action += 1
        else:
            self.fsla_chosen_action = 0

        self.fsla_chosen_action_depth_status = 1

        return

    # *****************************************************************************************
    def __action_switching(self):
        self.__choose_new_action_clockwise()
        self.__update_fsla_depth()

        self.fsla_state_transition_counter = 1
        self.fsla_depth_transition_counter = 0

        self.total_number_of_action_switching.append(
            1 + self.total_number_of_action_switching[-1] if len(self.total_number_of_action_switching) > 0 else 1)

        return

    # *****************************************************************************************
    def __evaluate_variable_action_set(self):
        variable_action_set_beta = 1 - (self.fsla_depth_transition_counter / self.fsla_state_transition_counter)  # NOQA

        self.variable_action_set.receive_environment_signal(
            variable_action_set_beta)

        return

    # *****************************************************************************************
    def __update_fsla_depth(self):
        new_depth_decision = 0

        if self.fsla_state_number == self.fsla_max_state:
            new_depth_decision = self.variable_action_set.choose_action([1, 2])
        elif self.fsla_state_number == self.fsla_min_state:
            new_depth_decision = self.variable_action_set.choose_action([0, 1])
        else:
            new_depth_decision = self.variable_action_set.choose_action([0, 1, 2])  # NOQA

        if new_depth_decision == 0:
            self.fsla_state_number += 1  # Grow
        # elif new_depth_decision == 1:
        #     # Do Nothing --> Stop
        elif new_depth_decision == 2:
            self.fsla_state_number -= 1  # Shrink

        return

    # *****************************************************************************************
    def __action_switching_by_scaling(self, sub_action_list):
        for action in sub_action_list:
            if self.fsla_chosen_action == action:
                return

        self.__choose_new_action_clockwise()

        self.fsla_state_transition_counter = 1
        self.fsla_depth_transition_counter = 0

        return
