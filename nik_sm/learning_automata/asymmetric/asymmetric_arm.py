import sys
import os
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

from variable_action_set import VariableActionSet  # NOQA


class AsymmetricArm:
    def __init__(self, state_number, reward_rate, penalty_rate, max_state_number, arm_manager):
        self.__fsla_state_number = state_number
        self.__fsla_depth_status = 1
        self.__fsla_state_transition_counter = 0
        self.__fsla_depth_transition_counter = 0
        self.__fsla_min_state = 1
        self.__fsla_max_state = max_state_number

        self.__reward_rate = reward_rate
        self.__penalty_rate = penalty_rate

        ''' 
            grow --> Action 0
            stop --> Action 1
            shrink --> Action 2
        '''
        self.__variable_action_set_action_number = 3
        self.__variable_action_set = VariableActionSet(
            self.__variable_action_set_action_number, self.__reward_rate, self.__penalty_rate)

        self.__arm_manager = arm_manager
        self.__first_action_switching = True

    # *****************************************************************************************
    def set_depth_status(self, value):
        self.__fsla_depth_status = value

    # *****************************************************************************************
    def set_state_transition_counter(self, value):
        self.__fsla_state_transition_counter = value

    # *****************************************************************************************
    def set_depth_transition_counter(self, value):
        self.__fsla_depth_transition_counter = value

    # *****************************************************************************************
    @property
    def state_number(self):
        return self.__fsla_state_number

    # *****************************************************************************************
    def receive_environment_signal(self, beta):
        if beta == 1:
            return self.__punish_automata()
        else:
            return self.__suprise_automata()

    # *****************************************************************************************
    def __suprise_automata(self):
        if self.__fsla_depth_status < self.__fsla_state_number:
            self.__fsla_depth_status += 1

        self.__fsla_state_transition_counter += 1

        if self.__is_fsla_on_depth():
            self.__fsla_depth_transition_counter += 1

        return False

    # *****************************************************************************************
    def __punish_automata(self):
        if self.__fsla_depth_status > 1:
            self.__fsla_depth_status -= 1

            self.__fsla_state_transition_counter += 1

            return False

        else:
            if not self.__first_action_switching:
                self.__evaluate_variable_action_set()
            else:
                self.__first_action_switching = False

            self.__update_fsla_depth()

            self.__fsla_depth_status = 1

            self.__fsla_state_transition_counter = 1
            self.__fsla_depth_transition_counter = 0

            self.__arm_manager.arm_switching_notification()

            return True

    # *****************************************************************************************
    def __is_fsla_on_depth(self):
        return self.__fsla_depth_status == self.__fsla_state_number

    # *****************************************************************************************
    def __evaluate_variable_action_set(self):
        variable_action_set_beta = 1 - (self.__fsla_depth_transition_counter / self.__fsla_state_transition_counter)  # NOQA

        self.__variable_action_set.receive_environment_signal(
            variable_action_set_beta)

        return

    # *****************************************************************************************
    def __update_fsla_depth(self):
        new_depth_decision = 0

        if self.__fsla_state_number == self.__fsla_max_state:
            new_depth_decision = self.__variable_action_set.choose_action([1, 2])  # NOQA
        elif self.__fsla_state_number == self.__fsla_min_state:
            new_depth_decision = self.__variable_action_set.choose_action([0, 1])  # NOQA
        else:
            new_depth_decision = self.__variable_action_set.choose_action([0, 1, 2])  # NOQA

        if new_depth_decision == 0:
            self.__fsla_state_number += 1  # Grow
        # elif new_depth_decision == 1:
        #     # Do Nothing --> Stop
        elif new_depth_decision == 2:
            self.__fsla_state_number -= 1  # Shrink

        return
