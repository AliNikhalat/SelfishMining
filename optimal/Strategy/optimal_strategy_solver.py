# optimal strategy solver
import numpy as np
from scipy.sparse import csr_matrix
import math
import mdptoolbox
import mdptoolbox.example

from action import Action
from fork import Fork


class OptimalSolver:
    def __init__(self, alpha, gamma, max_fork_len, show_log):
        self.alpha = alpha
        self.gamma = gamma
        self.max_fork_len = max_fork_len
        self.show_log = show_log

        self.state_number = (self.max_fork_len + 1) * \
            (self.max_fork_len + 1) * 3

        self.action_number = 4

        self._show_log('alpha is : {}'.format(self.alpha))
        self._show_log('gamma is : {}'.format(self.gamma))
        self._show_log('max_frok_len is : {}'.format(self.max_fork_len))
        self._show_log('state number is : {}'.format(self.state_number))

        self.probability = []
        self.honest_reward = []
        self.attacker_reward = []

        self.epsilon = 0.0001

    # ******************************************************************************
    def start_solving(self):
        self._init_matrices()

        # Adop Action Definition
        self.probability[Action.Adopt][:, self._convert_state_to_number(
            1, 0, Fork.Irrelevant)] = self.alpha
        self.probability[Action.Adopt][:, self._convert_state_to_number(
            0, 1, Fork.Irrelevant)] = 1 - self.alpha

        for i in range(self.state_number):
            state = self._convert_number_to_state(i)
            attacker_length = state[0]
            honest_length = state[1]
            fork = Fork(state[2])

            # Adop Action Definition
            self.honest_reward[Action.Adopt][i, self._convert_state_to_number(
                1, 0, Fork.Irrelevant)] = honest_length
            self.honest_reward[Action.Adopt][i, self._convert_state_to_number(
                0, 1, Fork.Irrelevant)] = honest_length

            # Override Action Definition
            if attacker_length > honest_length:
                self.probability[Action.Override][i, self._convert_state_to_number(
                    attacker_length - honest_length, 0, Fork.Irrelevant)] = self.alpha
                self.attacker_reward[Action.Override][i, self._convert_state_to_number(
                    attacker_length - honest_length, 0, Fork.Irrelevant)] = honest_length + 1
                self.probability[Action.Override][i, self._convert_state_to_number(
                    attacker_length - honest_length - 1, 1, Fork.Relevant)] = 1 - self.alpha
                self.attacker_reward[Action.Override][i, self._convert_state_to_number(
                    attacker_length - honest_length - 1, 1, Fork.Relevant)] = honest_length + 1
            else:
                self.probability[Action.Override][i, 1] = 1
                self.honest_reward[Action.Override][i, 1] = 10000

            # Wait Action Definition
            if fork != Fork.Active and attacker_length + 1 <= self.max_fork_len and honest_length + 1 <= self.max_fork_len:
                self.probability[Action.Wait][i, self._convert_state_to_number(
                    attacker_length + 1, honest_length, Fork.Irrelevant)] = self.alpha
                self.probability[Action.Wait][i, self._convert_state_to_number(
                    attacker_length, honest_length + 1, Fork.Relevant)] = 1 - self.alpha
            elif fork == Fork.Active and attacker_length > honest_length and honest_length > 0 and attacker_length + 1 <= self.max_fork_len and honest_length + 1 <= self.max_fork_len:
                self.probability[Action.Wait][i, self._convert_state_to_number(
                    attacker_length + 1, honest_length, Fork.Active)] = self.alpha
                self.probability[Action.Wait][i, self._convert_state_to_number(
                    attacker_length - honest_length, 1, Fork.Relevant)] = self.gamma * (1 - self.alpha)
                self.attacker_reward[Action.Wait][i, self._convert_state_to_number(
                    attacker_length - honest_length, 1, Fork.Relevant)] = honest_length
                self.probability[Action.Wait][i, self._convert_state_to_number(
                    attacker_length, honest_length + 1, Fork.Relevant)] = (1 - self.gamma) * (1 - self.alpha)
            else:
                self.probability[Action.Wait][i, 1] = 1
                self.honest_reward[Action.Wait][i, 1] = 10000

            # Match Action Definition
            if fork == Fork.Relevant and attacker_length >= honest_length and honest_length > 0 and attacker_length + 1 <= self.max_fork_len and honest_length + 1 <= self.max_fork_len:
                self.probability[Action.Match][i, self._convert_state_to_number(
                    attacker_length + 1, honest_length, Fork.Active)] = self.alpha
                self.probability[Action.Match][i, self._convert_state_to_number(
                    attacker_length - honest_length, 1, Fork.Relevant)] = self.gamma * (1 - self.alpha)
                self.attacker_reward[Action.Match][i, self._convert_state_to_number(
                    attacker_length - honest_length, 1, Fork.Relevant)] = honest_length
                self.probability[Action.Match][i, self._convert_state_to_number(
                    attacker_length, honest_length + 1, Fork.Relevant)] = (1 - self.gamma) * (1 - self.alpha)
            else:
                self.probability[Action.Match][i, 1] = 1
                self.honest_reward[Action.Match][i, 1] = 10000

        # self._show_log('********************************************')
        # self._show_log(self.attacker_reward[Action.Match])
        # self._show_log('********************************************')
        self._calculate_lower_bound()

    # ******************************************************************************
    def _init_matrices(self):
        self.probability = [csr_matrix((self.state_number, self.state_number), dtype=np.float32),
                            csr_matrix(
                                (self.state_number, self.state_number), dtype=np.float32),
                            csr_matrix(
                                (self.state_number, self.state_number), dtype=np.float32),
                            csr_matrix((self.state_number, self.state_number), dtype=np.float32)]

        self.honest_reward = [csr_matrix((self.state_number, self.state_number), dtype=np.float32),
                              csr_matrix(
                                  (self.state_number, self.state_number), dtype=np.float32),
                              csr_matrix(
                                  (self.state_number, self.state_number), dtype=np.float32),
                              csr_matrix((self.state_number, self.state_number), dtype=np.float32)]

        self.attacker_reward = [csr_matrix((self.state_number, self.state_number), dtype=np.float32),
                                csr_matrix(
                                (self.state_number, self.state_number), dtype=np.float32),
                                csr_matrix(
                                (self.state_number, self.state_number), dtype=np.float32),
                                csr_matrix((self.state_number, self.state_number), dtype=np.float32)]

        return

    # ******************************************************************************
    def _convert_state_to_number(self, attacker_length, honest_length, fork_state):
        return attacker_length * (self.max_fork_len + 1) * 3 + honest_length * 3 + fork_state

    # ******************************************************************************
    def _convert_number_to_state(self, state_number):
        fork = state_number % 3
        temp = math.floor(state_number / 3)
        honest_length = temp % (self.max_fork_len + 1)
        attacker_length = math.floor(temp / (self.max_fork_len + 1))

        return [attacker_length, honest_length, fork]

    # ******************************************************************************
    def _calculate_lower_bound(self):
        low_rou = 0
        high_rou = 1
        wrou = [None] * self.action_number

        lower_bound_policy = None
        lower_bound_reward = None

        while (high_rou - low_rou) > self.epsilon:
            rou = (high_rou + low_rou) / 2

            for i in range(self.action_number):
                wrou[i] = self.attacker_reward[i].multiply(
                    1-rou) - self.honest_reward[i].multiply(rou)

            value_iteration = mdptoolbox.mdp.RelativeValueIteration(
                self.probability, wrou, self.epsilon / 8)
            value_iteration.run()
            lower_bound_policy = value_iteration.policy
            lower_bound_reward = value_iteration.average_reward

            if lower_bound_reward > 0:
                low_rou = rou
            else:
                high_rou = rou

        print('lower bound rou is : {0}'.format(rou))

    # ******************************************************************************

    def _calculate_upper_bound(self):
        pass
    # ******************************************************************************

    def _show_log(self, log_message):
        if self.show_log == True:
            print(log_message)

        return
