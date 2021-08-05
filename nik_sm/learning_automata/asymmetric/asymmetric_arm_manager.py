import random
from numpy.random import choice


class AsymmetricArmManager:
    def __init__(self, arm_number):
        self.__arm_number = arm_number

        self.__chosen_arm = 0

    # *****************************************************************************************
    def chosen_arm(self, sub_action_list):
        switch = self.__arm_switching_by_scaling(sub_action_list)

        return self.__chosen_arm, switch

    # *****************************************************************************************
    @property
    def random_chosen_arm(self):
        self.__chosen_arm = random.randint(0, self.__arm_number-1)

        return self.__chosen_arm

    # *****************************************************************************************
    def arm_switching_notification(self):
        self.__choose_new_arm_clockwise()

        return

    # *****************************************************************************************
    def __choose_new_arm_clockwise(self):
        if self.__chosen_arm < self.__arm_number - 1:
            self.__chosen_arm += 1
        else:
            self.__chosen_arm = 0

        return

    # *****************************************************************************************
    def __arm_switching_by_scaling(self, sub_action_list):
        for action in sub_action_list:
            if self.__chosen_arm == action:
                return False

        self.__choose_new_arm_clockwise()

        return True
