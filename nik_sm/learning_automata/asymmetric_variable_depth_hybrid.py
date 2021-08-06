from matplotlib import pyplot as plt
import sys
import os

from asymmetric.asymmetric_arm_manager import *  # NOQA
from asymmetric.asymmetric_arm import *  # NOQA


class AsymmetricVariableDepthHybrid:
    def __init__(self, action_number, state_number_list, reward_rate, penalty_rate, max_state_number):
        self.__arm_number = action_number
        self.__init_state_number = state_number_list

        self.__reward_rate = reward_rate
        self.__penalty_rate = penalty_rate

        self.__chosen_arm = 0
        self.__arm_manager = AsymmetricArmManager(self.__arm_number)

        self.__arm_list = [AsymmetricArm(
            self.__init_state_number[i], self.__reward_rate, self.__penalty_rate, max_state_number, self.__arm_manager) for i in range(self.__arm_number)]

        self.__total_number_of_rewards = []
        self.__total_number_of_action_switching = []

        self.__arm_selection_status = [[]
                                       for _ in range(self.__arm_number)]

    # *****************************************************************************************
    @property
    def total_number_of_rewards(self):
        return self.__total_number_of_rewards

    # *****************************************************************************************
    @property
    def total_number_of_action_switching(self):
        return self.__total_number_of_action_switching

    # *****************************************************************************************
    @property
    def depth_vector(self):
        depth_vector = []
        for arm in self.__arm_list:
            depth_vector.append(arm.state_number)

        return depth_vector

    # *****************************************************************************************
    def get_action_selection_status(self, action_number):
        return self.__arm_selection_status[action_number]

    # *****************************************************************************************
    def choose_action(self, sub_action_list):
        self.__chosen_arm, switch = self.__arm_manager.chosen_arm(
            sub_action_list)

        if switch:
            self.__arm_list[self.__chosen_arm].set_depth_status(1)
            self.__arm_list[self.__chosen_arm].set_state_transition_counter(1)
            self.__arm_list[self.__chosen_arm].set_depth_transition_counter(0)

        return self.__chosen_arm

    # *****************************************************************************************
    def choose_random_action(self):
        self.__chosen_arm = self.__arm_manager.random_chosen_arm
        self.__arm_list[self.__chosen_arm].set_depth_status(1)

        return self.__chosen_arm

    # *****************************************************************************************
    def receive_environment_signal(self, beta):
        action_switch = self.__arm_list[self.__chosen_arm].receive_environment_signal(
            beta)

        if beta == 1:
            self.__total_number_of_rewards.append(
                0 + self.__total_number_of_rewards[-1] if len(self.__total_number_of_rewards) > 0 else 0)

            if action_switch:
                self.__total_number_of_action_switching.append(
                    1 + self.__total_number_of_action_switching[-1] if len(self.__total_number_of_action_switching) > 0 else 1)
            else:
                self.__total_number_of_action_switching.append(
                    0 + self.__total_number_of_action_switching[-1] if len(self.__total_number_of_action_switching) > 0 else 0)
        else:
            self.__total_number_of_rewards.append(
                1 + self.__total_number_of_rewards[-1] if len(self.__total_number_of_rewards) > 0 else 1)
            self.__total_number_of_action_switching.append(
                0 + self.__total_number_of_action_switching[-1] if len(self.__total_number_of_action_switching) > 0 else 0)

        return

    # *****************************************************************************************
    def visualization_calculations(self):
        for arm in range(self.__arm_number):
            if arm == self.__chosen_arm:
                self.__arm_selection_status[arm].append(
                    1 + self.__arm_selection_status[arm][-1] if len(self.__arm_selection_status[arm]) > 0 else 1)
            else:
                self.__arm_selection_status[arm].append(
                    0 + self.__arm_selection_status[arm][-1] if len(self.__arm_selection_status[arm]) > 0 else 0)
